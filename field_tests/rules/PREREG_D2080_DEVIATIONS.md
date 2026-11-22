# D2080 DEVIATIONS (written before any rerun, 22 Nov 2026)

**The flaw (a solver bug, not a result):** the first run accepted 'SUSY solutions' in which every χᵢ went to 0 or to ~1e8. Those are limit points (radii degenerate), where the residual goes to 0 only asymptotically. They are not finite-radius geometries.

**The fix (this tightens the filter; nothing is loosened):** the SUSY filter now also requires every χᵢ ∈ [1e-3, 1e3] at the solution, with the residual still < 1e-8. The calibration still has to pass unchanged. The first run's output is kept in this note as its record.

**Run-1 record:**
- calibration PASS, χ = (0.1821, 0.5462, 0.3642);
- k = 1: 5 'survivors' and k = 2: 12, all with χ at the boundary.
