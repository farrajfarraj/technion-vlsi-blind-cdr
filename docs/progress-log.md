# Progress log

## 2026-11-22 · Flip-flop characterization baseline

- **Inverter startup.** A clean extraction of the starter ZIP failed because it omitted `16nm_HP.pm`. Supplying the original model alongside the same deck allowed LTspice to run. The original failing session's log was unavailable. The students report a successful local inverter reproduction.
- **Inverter evidence.** At 0.300 ns, the prior waveform had a low input and 0.699899 V output. At 0.800 ns, it had a high input and 0.000272 V output. Second-edge propagation delays were 13.6055 ps falling and 9.9144 ps rising. [LTspice measurement log](../results/evidence/01_inverter_16nm_BSIM4.txt)
- **Prior implementation runs.** Device drain-current magnitudes increased across all 141 gate-bias points. The D flip-flop captured six expected bits and held state between edges. The fine setup sweep measured 18.63446 ps nominal clock-to-Q and bracketed the 105% threshold at 11.93–11.94 ps separation. [Fine-sweep LTspice log](../results/evidence/05_flipflop_setup_fine.txt) · [Waveform-checked CSV](../results/measurements/setup_results.csv)
- **Capture boundary.** The fine sweep found delayed capture at 5.8 ps and a missed rising output at 5.7 ps. At 5.8 ps the master nodes were near half supply at 4.045 ns and had settled by 4.15 ns. The study covers deterministic trajectories at one operating point.
- **Student review.** Independent student reruns of flip-flop functionality, nominal delay and setup extraction remain open. Instructor confirmation of the model's suitability also remains open.
- **Repository checkout check.** During repository setup, Codex ran all seven inputs in LTspice 24.0.12 from the reorganized directory. All 62 capture classifications agreed with the archived results. The largest absolute clock-to-Q difference was below 0.000001 ps, and both PNGs matched byte for byte. The committed CSV retains the archived measurements.

For future entries, record the date, contributor, source commit or pull request, simulator version, device model hash, conditions, observed result and who independently reproduced it.
