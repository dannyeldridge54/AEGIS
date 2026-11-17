# PREREG R2b3 — resonance-averaged threshold continuity (Gailitis–Damburg) — locked 2026-11-17, before any run
Closed side: S(x) = sΓs† with s = wino_s_nlo(M=2000, v, nlo=False), Γ = [[2,√2],[√2,3]], v = 2√(x·2δm/M). Same setup as r2b2_rydberg.py.
- Variable: n_eff = sqrt(0.0917/(1−x)).
- One full Rydberg period: n_eff ∈ [6.036, 7.036], centred on the D1159 peak at 6.536.
- Energy average: ⟨S⟩ = ∫S (dx/dn) dn / (x(7.036) − x(6.036)), with dx/dn = 2·0.0917/n³ and the trapezoid rule on a uniform n_eff grid.
- Grids: N = 1001 and N = 2001 points. Converged iff they agree within 5%. If not converged, the verdict is INCONCLUSIVE (no third grid without a DEVIATIONS note).
Open side: S at x = 1.01, 1.02, 1.05, 1.1, 1.2 (two_channel_open row 0, tails = (0, ALPHA), Vfun as in r2b2_threshold.py).
- Fit a quadratic in (x − 1). S₊ = the fit at x = 1.
Score: PASS iff |⟨S⟩/S₊ − 1| ≤ 0.20 (on the N = 2001 grid, given convergence).
