"""Render the measured LTspice data with ReportLab charts."""

import numpy as np
import pypdfium2 as pdfium
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
from reportlab.lib.colors import HexColor

from analyze import HERE, SWEEPS, devices_and_logic, measure_sweep, setup


INK, MUTED, GRID = "#192f42", "#465d70", "#dce4ea"
BLUE, ORANGE, TEAL, RED = "#11679c", "#be5c12", "#007e74", "#9f3945"


def label(d, x, y, text, size=11, color=INK, bold=False, align="start"):
    d.add(String(x, y, text, fontName="Helvetica-Bold" if bold else "Helvetica",
                 fontSize=size, fillColor=HexColor(color), textAnchor=align))


def canvas(w, h):
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=HexColor("#ffffff"), strokeColor=None))
    return d


def line(d, x1, y1, x2, y2, color, dashed=False):
    d.add(Line(x1, y1, x2, y2, strokeColor=HexColor(color), strokeWidth=1,
               strokeDashArray=[4, 3] if dashed else None))


def chart(d, box, xlim, ylim, series):
    x, y, w, h = box
    chart = LinePlot()
    chart.x, chart.y, chart.width, chart.height = box
    chart.data = [coords for coords, _ in series]
    for i, (_, col) in enumerate(series):
        chart.lines[i].strokeColor = HexColor(col)
        chart.lines[i].strokeWidth = 1.5
    for axis, bounds in [(chart.xValueAxis, xlim), (chart.yValueAxis, ylim)]:
        axis.valueMin, axis.valueMax, axis.valueStep = bounds
        axis.forceZero = False
        axis.labels.fontName = "Helvetica"
        axis.labels.fontSize = 9
        axis.labels.fillColor = HexColor(MUTED)
        axis.strokeColor = HexColor(MUTED)
    chart.xValueAxis.joinAxisMode = "bottom"
    chart.yValueAxis.joinAxisMode = "left"
    chart.yValueAxis.visibleGrid = True
    chart.yValueAxis.gridStrokeColor = HexColor(GRID)
    chart.yValueAxis.gridStrokeWidth = 0.5
    d.add(chart)
    def pixel(xx, yy):
        return (x+(xx-xlim[0])*w/(xlim[1]-xlim[0]), y+(yy-ylim[0])*h/(ylim[1]-ylim[0]))
    return pixel


def save_png(d, name):
    pdf = pdfium.PdfDocument(renderPDF.drawToString(d))
    page = pdf[0]
    page.render(scale=2).to_pil().save(HERE.parent / "results" / "figures" / name)
    page.close()
    pdf.close()


def inverter(inv):
    d = canvas(760, 308)
    label(d, 48, 270, "Inverter transient", 22, bold=True)
    label(d, 48, 247, "16 nm predictive bulk CMOS   /   0.7 V supply   /   1 fF load   /   27 °C", color=MUTED)
    for i, (text, color) in enumerate([("Input", ORANGE), ("Output", BLUE)]):
        x = 570+i*70
        line(d, x, 270, x+15, 270, color)
        label(d, x+19, 267, text, 10)
    # The pulse transitions and settled rails are both visible over four cycles.
    signals = [(list(zip(inv["time"]*1e9, inv[sig])), col) for sig, col in [("v(in)", ORANGE), ("v(out)", BLUE)]]
    chart(d, (60, 54, 662, 148), (0, 4, 0.5), (-0.1, 0.8, 0.1), signals)
    label(d, 60, 215, "Voltage (V)", 10)
    label(d, 391, 17, "Time (ns)", 11, align="middle")
    save_png(d, "inverter.png")


def setup_figure(all_rows):
    fine = [r for r in all_rows if r["maxstep_ps"] == SWEEPS[-1][1]]
    nominal, limit, setup_time, _ = setup(fine)
    # The finest available run represents each requested separation in the plot.
    by_x = {r["requested_ps"]: r for r in all_rows}
    rows = sorted(by_x.values(), key=lambda r: r["separation_ps"])
    d = canvas(838, 548)
    label(d, 46, 508, "Rising-data setup time", 24, bold=True)
    label(d, 46, 484, "Transmission-gate D flip-flop   /   0.7 V   /   1 fF   /   27 °C", color=MUTED)
    label(d, 46, 452, f"Nominal  {nominal:.3f} ps", 12, TEAL, True)
    label(d, 240, 452, f"105% limit  {limit:.3f} ps", 12, ORANGE, True)
    label(d, 463, 452, f"Setup at 5% growth  {setup_time:.2f} ps", 12, BLUE, True)
    panels = [
        ((62, 280, 712, 118), (-25, 525, 50), (10, 100, 15), "Full sweep"),
        ((62, 83, 320, 118), (4, 16, 2), (10, 100, 15), "Capture boundary"),
        ((455, 83, 320, 118), (11, 13, 0.25), (19.2, 20, 0.2), "5% crossing"),
    ]
    for (x, y, w, h), xlim, ylim, title in panels:
        visible = [r for r in rows if xlim[0] <= r["separation_ps"] <= xlim[1]]
        valid = [(r["separation_ps"], r["clk_to_q_ps"]) for r in visible if r["status"] == "captured"]
        px = chart(d, (x, y, w, h), xlim, ylim, [(valid, BLUE)])
        for ref, col in [(nominal, TEAL), (limit, ORANGE)]:
            if ylim[0] <= ref <= ylim[1]:
                line(d, *px(xlim[0], ref), *px(xlim[1], ref), col, True)
        for vx, vy in valid:
            d.add(Circle(*px(vx, vy), 1.9, fillColor=HexColor(BLUE), strokeColor=None))
        for r in visible:
            if r["status"] != "captured":
                xx = px(r["separation_ps"], ylim[0])[0]
                line(d, xx, y+1, xx, y+8, RED)
        if title == "5% crossing":
            line(d, *px(setup_time, ylim[0]), *px(setup_time, limit), BLUE, True)
            d.add(Circle(*px(setup_time, limit), 3.4, fillColor=HexColor("#ffffff"), strokeColor=HexColor(BLUE)))
        label(d, x, y+h+12, title + "   /   clock-to-Q (ps)", 11, bold=True)
        label(d, x+w/2, y-31, "Clock minus data at 50% VDD (ps)", 10, align="middle")
    label(d, 46, 15, "Dots show captures. Red ticks along the axis mark missing Q transitions. Each separation uses its finest timestep.", 10, MUTED)
    save_png(d, "setup.png")


if __name__ == "__main__":
    inv, _ = devices_and_logic()
    inverter(inv)
    setup_figure([r for name, dt in SWEEPS for r in measure_sweep(name, dt)])
