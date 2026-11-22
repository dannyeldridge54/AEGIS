# PREREG D1974 — tests OF the balancing method (Danny 18:04; locked 21 Nov 2026 before running; repo at cab2fc95)
Script: tools/loom/method_tests.py. Model: the D1972 resonance observables (n_s, α_s single stack, ln Y_B, quark u), with 4 knobs (m₃/₂, T_R, M_N, u). Each fit aims at the **data centre** (least squares).
- **T1, injection–recovery** (200 trials). PASS if coverage of the observables at 2σ is ≥ 0.90. Knob bias and scatter are reported.
- **T2, false-balance rate** (200 random data sets within ±5σ of the real centres). The method **is not evidence** if more than 0.20 of them "balance".
- **T3, real data.** Report dof = (data − knobs) and the hold-out predictions. A hold-out counts as a prediction only if |pull| ≤ 2 **and dof ≥ 1**.
