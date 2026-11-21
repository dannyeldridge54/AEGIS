# PREREG D1930 — first Loom pulse under rule 6h (7 nulls in a row), middle outwards (locked 21 Nov 2026 before running; repo at b9f60f39)
Helper: tools/loom/triangulate.py. Script: theory/tests/d1930_pulse_centre.py.
**Ring 0 (the centre): the shared rung step.**
- Iterated triangulation of the one-spurion fit-window edges (D1925 filters unchanged) around the median step 0.027, with brackets [0.0234, 0.027] and [0.027, 0.0311], resolution 1e-5, stopping after 7 nulls in a row.
- Then 3 naturalness readings inside the window (2,000 draws, seed 28+2).
- Report whether the window contains the median 0.027, u_d 0.02587, the lepton slip 0.0253 and the neutrino θ-step 0.0292.
- No PASS/FAIL. This is a measurement of an existing result, not a new postulate, so the flavour cap is untouched.
**Ring 1: α_s with a self-consistent AMSB spectrum** (gluino 3α₃(M₃)m₃/₂/4π, wino α₂m₃/₂/4π, scalars ∝ m₃/₂).
- Three readers: (a) two-loop weave_rg2; (b) one-loop analytic; (c) two-loop with the scalars held at 4.7e5 GeV.
- Fixed point in α_s with resolution 1e-5, stopping after 7 nulls.
- Run for S at ρ (m₃/₂ = 2.58e5) and S at i (7.6e5).
- Verdict per case: PASS if the converged centre is within 2σ of 0.1180 ± 0.0009, else FAIL. The spread is reported as the method floor.
**Validation:** reader (a) at the D1816 spectrum must give 0.1147 ± 5e-4; this is already shown in D1929.
