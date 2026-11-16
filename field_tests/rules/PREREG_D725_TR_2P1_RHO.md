# PREREG D725: T_R for the consistent 2 ⊕ 1 (W2, b = 0) heavy-neutrino sector at ρ
Locked 2026-11-16 before computing. Script: theory/modular/tr_2p1_d725.py. Output: field_tests/results/tr_2p1_d725.txt.
## Method (fixed now)
- Physical mass matrix M_phys(τ) = (2y)·M(τ), M = [[A(Y), cY],[cYᵀ, 0]] (all entries weight 2, so one Kähler factor; D724 weights k_N = k_N3 = −1). c ∈ {0.3, 1, 3}.
- At ρ: Takagi via SVD (singular vectors). The heavy state is non-degenerate. For the degenerate pair, take any orthonormal basis of its singular subspace; degenerate perturbation theory: P = Uᴴ ∂_y M_phys U* (direction along Re τ = ½). The 2×2 block P_LL's Takagi singular values give the linear splitting rates g_±; P_HL gives heavy–light couplings. Check: g_± equals lim (M_±(ρ+iδ) − M_L(ρ))/δ for δ = 1e-4, 1e-5 to 1%, and P_HH equals the stationary value (≈ 0 to 1e-6 relative); otherwise NULL.
- Yukawas: g = (coupling/M_heavy,model)·M_heavy·y√(2/3)/M_P. Widths: identical Majorana pair Γ = g² m (1 − 4x²)^{3/2}/(16π); distinct pair Γ = g² m λ^{1/2}(1 − (x_i+x_j)²)/(8π) (λ the Källén function in units of m²). m = 2.2e13 GeV, M_heavy ∈ {1e12, 1e13, 5e13} GeV; only channels with M_i + M_j < m.
- T_R = (90/(π²·106.75))^{1/4}√(Γ_tot M_P). N* (D719 code) at min and max T_R if any channel is open.
- If no linear channel is open: report the D601-type estimate and the BBN check T_R > 5 MeV.
## Decision rule
- Report the T_R band; CONSISTENT with D692 if it overlaps 1e6–1e8 GeV, else correction note (frozen bands not retuned), with n_s and r and whether they stay in the D693 bands.
- Dark radiation: the light states must decay to SM (seesaw y_D ≈ √(m_ν M_L)/v ≳ 3e-4 per D723) — report y_D at M_L.
- Fixes only via D725_DEVIATIONS.md.
