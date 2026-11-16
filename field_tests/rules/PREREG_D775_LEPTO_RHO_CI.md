# PREREG D775: actual CP asymmetry for SERAPIS-E's 2⊕1 heavy-ν sector at ρ (P1: explicit random phases)
Locked 2026-11-16 before computing. Script: theory/modular/lepto_rho_ci_d775.py. Output: field_tests/results/lepto_rho_ci_d775.txt.
Spectrum: from D725/D731. A degenerate pair M_p (exact at ρ) and a single state M_s.
- c = 0.3: pair 0.212·M_H, single M_H.
- c = 1: pair 0.707·M_H, single M_H.
- c = 3: single 0.471·M_H, pair M_H.
Cases (M_H, T_R) as in D731: (0.3, 1e12, 3.175e8), (1, 1e12, 4.287e8), (3, 1e12, 9.459e8), (0.3, 1e13, 3.033e9), (1, 1e13, 2.543e9).
Yukawas: Casas–Ibarra, Y = i·U*·√m·R·√D/v (v = 174 GeV), with the D745 PMNS (NO, δ = 230°), m₁ ∈ {1e-4, 1e-3} eV, and R = R₁₂R₁₃R₂₃ over the D745 27³ complex grid (P1).
- Inside the degenerate pair, rotate to Re H₁₂ = 0 (D745 alignment), so the pair's mutual term vanishes (Im[(H₁₂)²] = 0).
ε (unflavoured, Covi–Roulet–Vissani): ε_i = −(1/8π)·Σ_{j≠i, M_j ≠ M_i} Im[(H_ij)²]/H_ii·[f(x) + g(x)], with x = M_j²/M_i², f = √x[1 − (1 + x)ln((1 + x)/x)], g = √x/(1 − x).
Yield (D731 conventions): Y_B(species) = (8/23)(3/4)(T_R/m_φ)·2·|ε̄_species|, with m_φ = 2.2e13; for the pair ε̄ is the mean of its two members. Decays of the heavy single state are counted only where D731 did (M < m_φ/2).
Report: per case and m₁, the pass fraction Y_B ≥ 8.75e-11 and max |ε| versus D731's ε_DI.
K4: for c = 0.3 (hierarchical, x = 22 for the pair), max over the grid of |ε̄_pair| must lie in [0.3, 1.3]·ε_DI(M_pair).
Decision:
- PASS per case if the pass fraction ≥ 10%.
- lepto_rho: computed (estimate → computed) if every M_H = 1e12 case passes.
