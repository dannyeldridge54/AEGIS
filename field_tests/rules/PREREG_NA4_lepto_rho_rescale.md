# PREREG NA4 — node audit phase 4: lepto_rho under NA3's corrected T_R and m_φ
Locked before computing. Inputs: D731 yield form Y_B = (8/23)(3/4)(T_R/m_φ)·2ε (theory/modular/lepto_rho_d731.py), D775 ε results (CI grid; ε does not depend on T_R or m_φ),
D986 κ = 0.9391, NA3 rows (field_tests/results/na3_reheat_rho.txt: D725 T_R vs n = 1 T_R with m_φ = 3.17e13).
## Test
Rescale factor per case f = (T_R,new/T_R,D725)·(2.2e13/3.17e13). Branching among channels changes only through kinematics; the 2-N-per-φ-decay convention is kept (stated assumption).
1. c = 0.3, M_H = 1e12 (D775/D986: Y_B,max = 7.1e-11 after κ, ×1.22 short): report Y_B,max·f; PASS-to-pass if ≥ Y_obs = 8.75e-11.
2. Every D775 case: report f and M/T_R,new. D986's κ = 0.9391 assumed M/T_R ≥ 500 (instantaneous decay, no washout). Flag any case with M/T_R,new < 500 (κ needs recomputing), and any < 10 (thermal N production, D731's own validity cut).
3. Y_obs check: Y_B = η/7.04 with η = 273.9e-10·ω_b (standard), ω_b = 0.02237 (Planck 2018): must lie within 1% of 8.75e-11.
Status-only result (estimate, post-hoc): the frozen predictions do not include leptogenesis numbers. Results: field_tests/results/na4_lepto_rho_rescale.txt.
