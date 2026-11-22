# D2102 DEVIATIONS (written before rerunning B3)

**The flaw (a code bug):** B3 used a fixed K = 25/6 (from D2097, where Re z_vis = 6) for every model. The coupling rule is α_x⁻¹(M_s) = K·Re z_x with **K fixed by each model's own fit**, i.e. K = the fitted overall normalisation. For the run-1 hits (Re z_vis = 2), K ≈ 24.3/2, so rings with Re z = 2 are as weak as the visible sector, and the run-1 "exotic-safe" label is invalid.

**Run-1 record:**
- B3: 20 PS points, 16 "safe", 2 hits (Re z = 2, 2, 2 at χ = (1/3, 1, 2) and (1, 1/3, 2), α_s = 0.1167). **Void.**
- B1, B2 and B4 are unaffected.

**Fix:** rerun B3 with K and M_s taken per model from the D2083 fit (the same formulas as seed_v4_ps.predict); models with no physical fit are skipped for confinement. The rule is otherwise unchanged.
