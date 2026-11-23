# D2143 DEVIATIONS
## DEV-1 (2026-11-22). Crash at the b pull (written before any result was read; only the traceback was seen)
At u_i = 0.157 with b = ±0.025, the coupled solver fails (it collapses). The best-fit u_i at b = +0.025 is 0.068 (D2134a).
**Fix:** each b pull uses its own D2134 best-fit point (ω_b, ω_c, V_L, u_i at that b). The clock change is then measured between best fits.
A guard is added: if the solver still returns None, the row reads "solver failed" and no number is reported.
