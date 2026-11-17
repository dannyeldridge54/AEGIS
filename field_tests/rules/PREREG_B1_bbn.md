# PREREG B1 — first-minutes triangle: BBN wrapper + SERAPIS light elements (Djl B) — locked 2026-11-17
Code (written after this lock): tools/janus_astro/bbn.py (thin wrapper on camb.bbn.BBN_table_interpolator), theory/wiring/b1_bbn.py.
Referees: CAMB 1.5.9 tables PRIMAT_Yp_DH_ErrorMC_2021.dat (PRIMAT, τn 879.4 s, MC errors) and PArthENoPE_880.2_standard.dat (τn 880.2 s, no errors).
Sourced inputs:
- ω_b = 0.02242 ± 0.00014 (Planck 2018 VI Table 2, TT,TE,EE+lowE+lensing+BAO). SERAPIS: ΔN_eff = 0 (D725: 2⊕1 sector, no dark radiation).
- D/H obs: 10⁵(D/H)_P = 2.527 ± 0.030 (Cooke, Pettini & Steidel 2018, ApJ 855, 102).
- Y_p obs: 0.2453 ± 0.0034 (Aver et al. 2021, arXiv:2010.04180).
Tests (scored):
- T1 lossless: wrapper Y_p, D/H equal camb interpolator outputs exactly (|Δ| = 0) at 5 (ω_b, ΔN) points.
- T2 referee agreement: |Y_p(PRIMAT) − Y_p(PArthENoPE)| ≤ 1.0e-3 at ω_b = 0.02242, ΔN ∈ {0, 0.5, 1}.
Reported (not scored):
- D/H PRIMAT vs PArthENoPE relative difference (known nuclear-rate dependent).
- R1 SERAPIS pulls: pull = (pred − obs)/sqrt(σ_obs² + σ_th² + (∂pred/∂ω_b·σ_ωb)²) for Y_p and D/H, each table (σ_th = PRIMAT MC columns; 0 for PArthENoPE). Labels: |pull| < 2 CONSISTENT, 2–3 TENSION, > 3 EXCLUDED.
- R2 BBN-only ΔN_eff 95% range (PRIMAT, ω_b fixed at Planck, Δχ² < 3.84 from Y_p + D/H), and whether SERAPIS ΔN = 0 is inside.
- R3 decay time: t = 1/(2H), H = sqrt(π² g*/90) T²/M̄_P, g* = 106.75, M̄_P = 2.435e18 GeV, ħ = 6.582119569e-25 GeV s; t at T = 1e5, 1e6 GeV vs t_BBN ~ 1 s.
B1 VALIDATED iff T1 and T2 pass. Fixes only via DEVIATIONS before any rerun.
