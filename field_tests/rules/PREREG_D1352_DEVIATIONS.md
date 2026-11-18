# D1352 deviations (written before any further computation)

D1 (2026-11-18): the locked check "3α=1 r within 1e-3 relative of 12α/N*²" FAILED as written (2.0% off).
Cause: the tolerance was mis-set — 12α/N² is only the leading large-N term; its next correction is O(1/N)
(≈2% at N=55), so 1e-3 could never pass. The main results are NOT rerun or changed.
Replacement check (added, not a rerun): the T-model has an exact closed form,
  sinh²y_e = 4/(3α), cosh y* = cosh y_e + 4N/(3α), r = 64/(3α sinh²y*), y = 2φ/√(6α),
  n_s from η likewise; the numerics must match it within 1e-3 relative on r and 1e-4 on n_s for all six configs.
