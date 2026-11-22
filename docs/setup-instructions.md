# Reproduce the LTspice baseline

Use LTspice 24.0.12 for Windows to match the reference runs. Clone the repository, obtain the reference model, and keep all circuit files in `simulations/ff-timing/`. Run commands below from the repository root. [Model download and fingerprint](../models/README.md)

## Check the inverter first

Open `simulations/ff-timing/01_inverter_schematic.asc`, click **Run**, then choose **Plot Settings → Add Trace** and select `V(in)` and `V(out)`. **View → SPICE Error Log** shows the second-edge propagation delays. Compare against about 13.61 ps for falling output and 9.91 ps for rising output. A missing-include error points to the location, spelling or extension of the model file.

## Generate waveforms and measurements

```powershell
.\scripts\run-ltspice.ps1
```

For a different installation path, pass `-LTspice` followed by the full path to `LTspice.exe`. The script runs the device DC deck, both inverter representations, the functional flip-flop deck and the three setup sweeps. Its per-deck flags produce the ASCII or double-precision binary files expected by the supplied reader. Raw waveforms and logs appear beside their decks.

To regenerate the CSV and both PNGs, use Python 3.12 with the tested package versions. Inspect the output and use `git diff` before committing regenerated results.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r scripts/requirements.txt
.\.venv\Scripts\python scripts/analyze.py
.\.venv\Scripts\python scripts/plot_results.py
```

## Interpret the runs

| Input | Measurement |
| --- | --- |
| `00_device_dc.cir` | Sweep gate drive from 0 to 0.7 V and inspect NMOS and PMOS drain current magnitudes. |
| `01_inverter_16nm_BSIM4.cir` and schematic | Check inversion, second-edge propagation delays and 10–90% output transition times. |
| `02_flipflop_function.cir` | Inspect D, CLK and Q at six rising edges. Expected sequence is 0, 1, 1, 0, 0, 1. Check Q holds through intervening D changes. |
| `03_flipflop_setup.cir`, `04_flipflop_setup_refined.cir`, `05_flipflop_setup_fine.cir` | Sweep data lead at maximum timesteps of 0.25, 0.125 and 0.0625 ps. Compare delay growth and missing captures. |

Use the second rising clock crossing at 4.0025 ns. At 50% supply, data lead is clock time minus data time. Clock-to-Q is rising Q time minus clock time. The retained waveforms cover 3.4–4.79 ns, and the reader accounts for LTspice's time offset.

For the 5% criterion, average clock-to-Q at 200, 300 and 500 ps lead, multiply by 1.05, then interpolate between the two bracketing valid runs. A valid capture starts low, crosses upward once after the active clock, and settles above 0.63 V during the final 90 ps. LTspice can print zero when the Q crossing is missing. Use the waveform classification and leave the delay blank for that row. Plot internal nodes `V(md)` and `V(mbar)` to examine resolution near the boundary.
