# PREREG D700: a 1/E plateau from Casimir energy + area-modulus elimination (SERAPIS-C)
Locked 2026-11-15 before computing. Script theory/modular/casimir_plateau_d700.py.
Mechanism (argument, stated before computing): a 6D field on T² (area A, shape U) has Casimir energy ρ6 ∝ ±E(U,3)/A³ (Epstein series, Σ'(m,n)); in 4D Einstein frame V4 ∝ ρ6/A, so V_Cas = +b E(U,3)/A⁴ (fermion-dominated sign). A net codimension-2 (3-brane) tension T < 0 gives V_T = −|T|/A². Eliminating A (∂_A V = 0): A² = 2bE/|T|, V_min = −T²/(4bE(U,3)). With a constant uplift tuned to vanish at E's minimum: V = V0[1 − E(ρ,3)/E(τ,3)].
Checks in code: (1) E(τ,3) Fourier series vs lattice sum at i and ½+2i (agree to 1e-4); (2) E(τ,3) minimal at ρ (vs i, ρ+0.05, ρ+0.05i).
Model SERAPIS-C: V/V0 = [1 − E(ρ,3)/E(τ,3)]·(1 + C Ê2), Ê2 = E(τ,2) − E(ρ,2) (BHK tilt, D689); along Re τ = ½; first-order slow roll (D691 obs()).
Grid: C ∈ {0, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5}, N* ∈ {48.4, 49.9} (heavy-vacuum bracket assumed; vacuum m²/H² reported). Report y*, n_s, r, α_s; interpolate C at n_s = 0.970.
Viability rule (as D691): n_s 0.965–0.975 reachable, y* ≤ 25, |α_s| ≤ 0.009, r inside caps (≤ 8.3e-4); compare with SERAPIS-E and the frozen strip (D679).
