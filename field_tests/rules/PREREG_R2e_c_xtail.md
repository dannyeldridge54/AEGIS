# PREREG R2e-c — does holding R_eff fixed beyond x = 3e4 matter? (D1238 candidate i) — locked 2026-11-18, before code or run
Same code as R2e-b (r2e_b_gstar.omega, g_*(T) EOS, MS-bar α̂₂(2M), x to 1e8), at M = 2800 and 3000 GeV only.
- x grid extended: the 25 R2e-b points (3 to 3e4) plus 8 log points on (3e4, 1e5].
- R_eff is held fixed beyond 1e5.
- The upper limit is 1e5, not 1e6. The single-channel velocity grids start at v = 1e-3. At x = 1e5 the Maxwell weight below that is ≈ (1e-3·√(x/4))³ ≈ 0.4%, and it is reported. At 1e6 it would exceed 10%, which is not acceptable without grid changes.
Scored:
- T1: the R_eff values at the 25 shared x points must reproduce R2e-b's run within 1e-6, i.e. the same tables.
- Q: the relative change of Ω h² vs R2e-b (0.1048 at 2.8 TeV, 0.1195 at 3.0 TeV).
  - |ΔΩ/Ω| > 1% at either mass → candidate (i) MATTERS.
  - Otherwise it is RULED OUT as the main cause of the +4.4% L1 gap.
Reported:
- R_eff at x = 3e4 and 1e5;
- the implied M_th shift (log-slope estimate from R2e-b's Ω(M)).
