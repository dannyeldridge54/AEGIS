# DEVIATIONS for PREREG_D1658_G9D_FUTURE_D1636 (written before the rerun)
D1 (coding, 2026-11-19 ~23:37Z). Run 1 (kept: D1658_G9d_future_d1636_run1_FAILED_interp.json): np.interp was given the w₀ grid REVERSED (decreasing), which numpy does not support; every "matched" amp collapsed to the grid edge 0.03 (w₀ −0.999 instead of −0.86…−0.93). The w₀ grid itself is monotonic increasing in amp (seen: −0.999 → −0.46). The same-u runs are unaffected and are reported from run 1 as well.
Fix: np.interp(w0t, w0s[ok], grid[ok]) (increasing order). Nothing else changes; one rerun.
