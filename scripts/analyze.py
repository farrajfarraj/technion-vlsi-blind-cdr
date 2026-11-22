"""Measure the LTspice raw files produced by the project run commands."""

import csv
import re
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "simulations" / "ff-timing"
SWEEPS = [
    ("03_flipflop_setup", 0.25),
    ("04_flipflop_setup_refined", 0.125),
    ("05_flipflop_setup_fine", 0.0625),
]


def read_raw(name):
    data = (ROOT / (name + ".raw")).read_bytes()
    encoding = "utf-16le" if data.startswith(b"T\x00") else "ascii"
    for marker, newline in [("Values:", "\r\n"), ("Values:", "\n"), ("Binary:", "\n"), ("Binary:", "\r\n")]:
        header, found, body = data.partition((marker + newline).encode(encoding))
        if found:
            break
    else:
        raise ValueError(f"Unrecognized raw format: {name}")
    header = header.decode(encoding).replace("\r\n", "\n")
    variables = [line.split()[1].lower() for line in header.split("Variables:\n")[1].splitlines()]
    count = int(re.search(r"No. Points:\s*(\d+)", header)[1])
    if marker == "Values:":
        array = np.fromstring(body.decode(encoding), sep=" ").reshape(count, len(variables) + 1)[:, 1:]
    elif "real double" in header:
        array = np.frombuffer(body, dtype="<f8").reshape(count, len(variables))
    else:
        raise ValueError(f"For {name}, rerun with -ascii or numdgt=15 as in docs/setup-instructions.md")
    # LTspice rebases transient time when .tran has a nonzero save-start.
    axis = np.abs(array[:, 0]) + float(re.search(r"Offset:\s*(\S+)", header)[1])
    cuts = np.flatnonzero(np.diff(axis) < 0) + 1
    runs = []
    for idx in np.split(np.arange(count), cuts):
        run = dict(zip(variables, array[idx].T))
        run[variables[0]] = axis[idx]
        runs.append(run)
    return runs


def crossings(run, signal, level=0.35, rising=True):
    v = run[signal]
    t = run["time"]
    above = v >= level
    edges = (~above[:-1] & above[1:]) if rising else (above[:-1] & ~above[1:])
    i = np.flatnonzero(edges)
    return t[i] + (level - v[i]) * (t[i + 1] - t[i]) / (v[i + 1] - v[i])


def devices_and_logic():
    dc, = read_raw("00_device_dc")
    for name, current in [("NMOS", -dc["i(vdn)"]), ("PMOS", dc["i(vdp)"])]:
        assert len(current) == 141 and np.all(np.diff(current) > 0)
        print(f"{name} |ID| off/on: {current[0]*1e9:.4f} nA, {current[-1]*1e6:.4f} uA")
    inv, = read_raw("01_inverter_16nm_BSIM4")
    schematic, = read_raw("01_inverter_schematic")
    for sig in ["time", "v(in)", "v(out)"]:
        np.testing.assert_allclose(inv[sig], schematic[sig], rtol=1e-7, atol=1e-18)
    for signal_rises in [True, False]:
        t_in = crossings(inv, "v(in)", rising=signal_rises)
        t_out = crossings(inv, "v(out)", rising=not signal_rises)
        delay = (t_out[1] - t_in[1]) * 1e12
        start, stop = (0.63, 0.07) if signal_rises else (0.07, 0.63)
        t_start = crossings(inv, "v(out)", start, not signal_rises)[1]
        t_stop = crossings(inv, "v(out)", stop, not signal_rises)[1]
        print(f"Output {'fall' if signal_rises else 'rise'}: delay {delay:.4f} ps, slew {(t_stop-t_start)*1e12:.4f} ps")
    for ns in [0.3, 0.8]:
        print(f"Inverter at {ns} ns: {np.interp(ns*1e-9, inv['time'], inv['v(out)']):.9f} V")
    func, = read_raw("02_flipflop_function")
    edges = crossings(func, "v(clk)")
    expected = np.array([0, 1, 1, 0, 0, 1])
    d = np.interp(edges, func["time"], func["v(d)"])
    np.testing.assert_equal(d > 0.35, expected)
    for i, edge in enumerate(edges):
        end = edges[i+1] if i+1 < len(edges) else func["time"][-1]
        q = func["v(q)"][(func["time"] >= edge+0.15e-9) & (func["time"] < end)]
        assert np.all(q > 0.63) if expected[i] else np.all(q < 0.07)
    print("Six captures and inter-edge holds verified.")
    return inv, func


def measure_sweep(name, maxstep):
    logbytes = (ROOT / (name + ".log")).read_bytes()
    log = logbytes.decode("utf-16" if b"\x00" in logbytes[:20] else "utf-8-sig")
    params = [float(s)*1e12 for s in re.findall(r"(?im)^\.step delta=(\S+)", log)]
    runs = read_raw(name)
    assert len(runs) == len(params) and params
    rows = []
    for nominal, run in zip(params, runs):
        tc, = crossings(run, "v(clk)")
        td, = crossings(run, "v(d)")
        delta = (tc - td)*1e12
        assert abs(tc*1e9-4.0025) < 0.0001 and abs(delta-nominal) < 0.001
        assert run["time"][-1] >= 4.7899e-9
        q = run["v(q)"]
        assert q[0] < 0.07
        tq = crossings(run, "v(q)")
        tail = q[run["time"] >= 4.7e-9]
        delay = None
        if len(tq) == 1 and tq[0] > tc and np.all(tail > 0.63) and not len(crossings(run, "v(q)", rising=False)):
            status = "captured"
            delay = (tq[0] - tc)*1e12
        elif not len(tq) and np.all(tail < 0.07):
            status = "no rising Q"
        else:
            status = "invalid capture"
        rows.append(dict(deck=name, maxstep_ps=maxstep, requested_ps=round(nominal, 6),
                         separation_ps=round(delta, 8), clk_to_q_ps=delay,
                         q_end_V=q[-1], status=status))
    return rows


def setup(rows):
    valid = [r for r in rows if r["status"] == "captured"]
    plateau = [r["clk_to_q_ps"] for r in valid if r["requested_ps"] in (200, 300, 500)]
    assert len(plateau) == 3
    nominal = np.mean(plateau)
    limit = 1.05*nominal
    ordered = sorted(valid, key=lambda r: r["separation_ps"])
    left, right = [(a, b) for a, b in zip(ordered, ordered[1:])
                   if a["clk_to_q_ps"] >= limit > b["clk_to_q_ps"]][0]
    x1, x2 = left["separation_ps"], right["separation_ps"]
    y1, y2 = left["clk_to_q_ps"], right["clk_to_q_ps"]
    return nominal, limit, x1+(limit-y1)*(x2-x1)/(y2-y1), (x1, x2)


if __name__ == "__main__":
    devices_and_logic()
    all_rows = []
    for deck, timestep in SWEEPS:
        rows = measure_sweep(deck, timestep)
        all_rows.extend(rows)
        print(deck, "nominal, limit, setup, bracket [ps]:", setup(rows))
    with (HERE.parent / "results" / "measurements" / "setup_results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)
