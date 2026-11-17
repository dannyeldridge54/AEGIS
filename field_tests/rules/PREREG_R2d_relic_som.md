# PREREG R2d — LO Sommerfeld wino thermal mass from the Boltzmann equation — locked 2026-11-17, before any code or run
Inputs:
- R_eff(x; M) from r2c_b_alls.run (unchanged code). x on 25 log points in [3, 3e4], n = 40 grids (convergence was 3.8e-5 in R2c-b).
- Re-check n = 80 at M = 2800 for x ∈ {25, 3e3, 3e4}; required within 1%.
- σ_eff(x) = R_eff(x)·σ_Born, with σ_Born = relic.sigma_eff_born(M, a2 = sommerfeld_nlo.ALPHA2)[0].
- R_eff is interpolated linearly in log x. For x < 3, R(3) is used.
- Boltzmann: a copy of relic.omega_h2 with lam → lam·R_eff(x) (Radau, rtol 1e-8), constant g_* = 106.75 and g_eff = 6 as in R1, integrated to x_end = 3e4. Sensitivity reported for x_end = 1e4.
- Mass grid M ∈ {2.5, 2.7, 2.8, 2.9, 3.1, 3.3} TeV. Ω h²(M) is interpolated in log–log. M_th is where Ω h² = 0.1205.
Scored:
- S1: M_th ∈ [2.6, 3.1] TeV. That is Hisano's 2.7–3.0 TeV band widened by ±0.1 for constant g_*, unrun α₂ and the Ω h² definition.
- S2: Y(Sommerfeld)/Y(Born) at M = 2.8 TeV ∈ [0.40, 0.60] (Hisano Fig. 2 left: ≈ 50%).
- S3: Born consistency: the same code with R_eff ≡ 1 must reproduce the R1b Born mass of 2.531 TeV within 0.5%.
No tuning. Any fix goes in DEVIATIONS before a rerun.
