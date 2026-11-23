# D2143 DEVIATIONS
## DEV-1 (2026-11-22). Crash at the b pull (written before any result was read; only the traceback was seen)
At u_i = 0.157 with b = ±0.025, the coupled solver fails (it collapses). The best-fit u_i at b = +0.025 is 0.068 (D2134a).
**Fix:** each b pull uses its own D2134 best-fit point (ω_b, ω_c, V_L, u_i at that b). The clock change is then measured between best fits.
A guard is added: if the solver still returns None, the row reads "solver failed" and no number is reported.

## DEV-2 (2026-11-22, referee R43-1…3; written before the rerun)
- **Common protocol for every late-clock row:** hold ω_b and ω_c at the b = 0 fit. Re-solve V_L so the CMB acoustic scale ℓ_A = π D_M(z\*)/r_s equals its b = 0 value (the data anchor). Only the pulled knob changes.
- The first run did not do this. V_L was held fixed, so H0 floated. That holds for both the u_i row and the b row, so the referee's statement that the u_i row was already anchored is not true of the code.
- The best-fit ages at each b are reported separately, as "data-constrained age at each b".
- **Wording change:** "thrust" is renamed **"curvature (even response)"**. The claims "clearest case of Danny's thrust" and "postulate partly right" are withdrawn: curvature appears at any extremum, so it cannot validate the postulate. The N4/N8 "mirror" is equal and opposite **by construction**.
