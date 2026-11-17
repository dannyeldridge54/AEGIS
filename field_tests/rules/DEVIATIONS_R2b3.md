# DEVIATIONS R2b3 — written before the rerun (2026-11-17)
D1: the first run crashed before printing any result. numpy 2.x removed np.trapz (AttributeError). No numbers were seen.
- Fix: use np.trapezoid, which is the same trapezoid rule. No change to the method, grids, fit or criteria.
- Also save the closed-side S grid to field_tests/results/r2b3_S_grid.npy, so a later crash does not force recomputing it.
