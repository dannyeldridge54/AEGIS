# PREREG D1976 — the method tests re-pulsed on three axes in tandem (Danny 18:08; locked 21 Nov 2026 before running; repo at 0aac586e)
Script: tools/loom/method_tests_3axis.py.
**Setup:** three knobs (S: T_R; T: m₃/₂; U: u), with M_N tied to its derived value. Six data: n_s, α_s, ln Y_B, u, plus the wino bound and the gravitino box as one-sided data. That gives dof = 3.
**Each test is pulsed:** three seeds per pulse, repeated until the mean moves less than 0.01 for 7 pulses in a row.
**Bars (the same as D1974):**
- T1 coverage ≥ 0.90;
- T2 false-balance ≤ 0.20;
- T3 reports χ²/dof and the hold-outs.
Expectation: fewer knobs and more data should raise T1 and lower T2.
