# PREREG DILATON32 — DEVIATIONS (written before any rerun)

## D1 (2026-11-19 03:32 CT)
A0 and B0 crashed (ms.spectra: bg.Nend is None) before printing any row — no result seen; A1/A2 were stopped before finishing
(same start rule). Cause: starting at the deepest grid point (y ≈ 2976), the slower E(τ,3/2) plateau gives more than the
Background's Nmax = 400 e-folds, so inflation never ends inside the integration. Fix: choose the start point by bisection on
the grid index so that the background gives N_end ∈ [100, 200] (target 140) — enough for N* ≈ 50 plus the spectra margin —
for each run separately. Model, forms, C values, band and rule unchanged.
