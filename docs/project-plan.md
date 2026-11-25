# Project plan

The next milestone is a ten-DFF sampling experiment in LTspice. The archived single-DFF sweep is the reference for comparing the bank's capture behavior. Its 11.94 ps rising-data setup result applies to the predictive 16 nm bulk BSIM4 model and recorded testbench conditions. [Baseline measurements](../results/measurements/setup_results.csv)

1. **Qualify the 16 nm model.** Run NMOS and PMOS I–V checks in LTspice and record the card fingerprint, geometry, bias conditions and warnings. Confirm whether the predictive bulk model satisfies the intended technology scope. Check access to a licensed 16 nm lab SPICE model or a nearby-node reference in parallel. [Model provenance](../models/README.md)
2. **Rerun the DFF and build the bank.** Reproduce the single-DFF capture and setup experiments. Use the working CMOS master/slave DFF ten times with a shared data signal and staggered taps from one master clock. [Reproduction instructions](setup-instructions.md)
3. **Measure the capture boundary.** Sweep the common clock offset at fine resolution with fixed tap spacing. For each tap, record its clock crossing, clock-to-Q delay and capture status. Inspect internal latch nodes for delayed resolution. Leave delay empty when Q has no crossing within the observation window.
4. **Evaluate clock selection.** Study device variation and circuit noise separately. Use the observed capture behavior to choose a sampling phase, then compare bit error rate (BER) before and after selection on matched inputs. The final clock interface and numeric BER target are open.

## Provisional schedule

| Planning window | Deliverable |
| --- | --- |
| 20–27 Nov 2026 | Task 3 model I–V checks and lab access inquiry |
| 27 Nov–4 Dec | DFF rerun and ten-tap bench |
| 4–11 Dec | Fine sweep and per-tap results |
| 11–18 Dec | Midterm demonstration of the bank and measured delay behavior |
| After midterm | Variation, noise, sampling-phase selection and BER comparison |
| Around 12 Feb 2027 | Final report and demonstration |

These are planning estimates. Confirm the course deadlines separately. For the DFF circuit and timing reference, see Baker, *CMOS Circuit Design, Layout, and Simulation*, 3rd ed., Chapter 13, pp. 386–388. [Author's table of contents](https://cmosedu.com/cmos1/TOC_3RD.pdf)
