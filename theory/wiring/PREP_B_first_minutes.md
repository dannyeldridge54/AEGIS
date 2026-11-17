# PREP (B) First-minutes triangle — sourcing log (Djl loop, 17 Nov 2026)
Goal: wire Chronos Clock (T_R) and Hyperion (ω_b, N_eff) into Big Bang nucleosynthesis; test the ρ branch's late decays.

## Referee found offline (tick 2, 13:04 UTC)
- CAMB 1.5.9 (installed) ships BBN tables and interpolators (camb.bbn: BBN_table_interpolator, BBN_fitting_parthenope, get_predictor):
  PRIMAT_Yp_DH_Error.dat, PRIMAT_Yp_DH_ErrorMC_2021.dat, PArthENoPE_880.2_standard.dat, PArthENoPE_880.2_marcucci.dat.
  Two independent BBN codes' tabulated Y_p and D/H vs (ω_b, ΔN_eff) — the referee pair for this string (PRyMordial not on pip).
- Literature pointers (search 17 Nov): CAMB BBN docs (camb.readthedocs.io/en/latest/bbn.html); hadronic late-decay limits: Kawasaki, Kohri, Moroi (astro-ph/0402490, astro-ph/0408426), Kawasaki et al. 2018 (arXiv:1709.01211).

## Quick estimate (not locked; to be confirmed in the D-note)
The ρ branch's heavy Dirac states decay via string-scale operators at T₂ ≳ 1e5–1e6 GeV (D780–D783). In radiation domination t = 1/(2H), H = √(π² g*/90) T²/M_P (g* = 106.75): t(1e5 GeV) ≈ 2.4e-17 s, t(1e6 GeV) ≈ 2.4e-19 s — 16+ orders of magnitude before BBN (t ~ 1–1e3 s, where the hadronic/EM limits of 1709.01211 apply). So late-decay BBN limits do not reach these states [estimate]; the BBN test of the ρ branch reduces to its ΔN_eff and ω_b, which go through the CAMB BBN tables.

## Next for (B)
Lock PREREG_B1: (i) Hyperion's own BBN wrapper vs the PRIMAT and PArthENoPE tables (two referees agree to their stated level); (ii) SERAPIS branches' (ω_b from the CMB fit, ΔN_eff = 0 + dark-radiation budget D723/D725) → Y_p, D/H vs sourced observations (D/H: Cooke et al. 2018; Y_p: Aver et al. 2021 — to be fetched); (iii) the decay-time estimate above made formal.
