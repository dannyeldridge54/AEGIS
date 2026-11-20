# PREREG_Q9_KLZ — BIG LOOP Q9: recompute the ADM mass from chemical equilibrium (locked D1676, 2026-11-20 00:30 UTC)
Setup: SM, N_g = 3, one Higgs doublet, T ≫ T_EW (sphalerons on, Yukawas in equilibrium, gauge μ = 0). Plus a singlet X with portal X²LH, so 2μ_X + μ_l + μ_h = 0 (L_X = −½ per X).
Equations: μ_u = μ_q + μ_h, μ_d = μ_q − μ_h, μ_e = μ_l − μ_h; sphaleron 3μ_q + μ_l = 0; hypercharge Y = 0. Asymmetries are ∝ gμ, with a factor 2 for bosons.
B = N_g(6μ_q + 3μ_u + 3μ_d)/3. n_X ∝ g_X μ_X (×2 if boson). Cases: X a Dirac fermion (g = 2) or a complex scalar (g = 1, boson factor 2).
m_X = (Ω_c/Ω_b) m_p · B/n_X, with Ω_c/Ω_b = 5.364. In the simple treatment B is frozen at T_EW and X at T_D (both taken from the T ≫ T_EW solution).
Pass: m_X ∈ [3, 15] GeV for at least one case, consistent with the KLZ quote of 5–11 GeV. Otherwise report the discrepancy.
Script: field_tests/scripts/q9/run.py
