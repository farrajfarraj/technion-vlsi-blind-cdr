# Initial issue backlog

These seven issue descriptions are ready for GitHub. All require an action or a review by the project team. The reference values come from the 16 nm predictive bulk CMOS baseline.

## Record independent inverter reproduction

**Milestone:** Baseline reproduction

The students have already reproduced inverter operation locally. Record the simulator version, model hash, 0.7 V supply, 1 fF load and 27 °C setting from a student run. Attach the measured second-edge tPHL and tPLH or a sanitized excerpt. Compare against 13.61 ps and 9.91 ps and document any difference before closing.

## Reproduce the flip-flop functionality test

**Milestone:** Baseline reproduction

From a fresh checkout, run `02_flipflop_function.cir`. Record D and Q at the six active edges and inspect Q between edges. Attach a plot or table showing the expected sequence 0, 1, 1, 0, 0, 1, or document the first mismatch. Identify the student who ran the test.

## Reproduce setup time at 5% clock-to-Q growth

**Milestone:** Baseline reproduction

Run decks 03, 04 and 05, then regenerate the CSV. Report the early-data plateau, the 105% threshold, the two valid points bracketing the limit and interpolated setup. Compare with 18.63 ps nominal and 11.94 ps setup. Preserve missing-capture status and document differences between timesteps.

## Investigate delayed resolution near the capture boundary

**Milestone:** Characterization follow-up

Examine D, CLK, Q, MD and MBAR for the 5.7 ps and 5.8 ps cases. Document the observation window, the final state and how long resolution takes. Check sensitivity to timestep and distinguish deterministic behavior from evidence needed to estimate a failure probability.

## Document the transmission-gate flip-flop architecture

**Milestone:** Characterization follow-up

Trace the input and feedback paths in `dff_core.inc` for each clock phase. Add a schematic or annotated diagram showing the complementary clock, master and slave nodes, and Q. Have the partner cross-check the signal polarity against the six-edge waveform.

## Confirm the academic model choice with the instructor

**Milestone:** Baseline reproduction

Ask whether the public CROW 16 nm predictive bulk BSIM4 model is suitable for the timing experiment. Record the decision and its scope in the progress log in your own words. Keep private correspondence outside Git.

## Scope setup and hold characterization extensions

**Milestone:** Characterization follow-up

Propose a hold experiment and a falling-data setup experiment. Specify which clock/data events to pair, initialization, sweep range, settling window and valid capture criteria. Have the partner review the plan before implementing a new bench.
