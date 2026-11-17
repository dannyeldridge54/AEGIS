# PREREG L1 — TorsionΛ D715 audit redone with Janus-LT first-principles pieces (replaces fitting formulas)
Locked 2026-11-17 before any L1 number.
D715 computed Planck-2018 compressed (R, l_A) for TorsionΛ (E² = Ω_r(1+z)⁴ + Ω_m(1+β)(1+z)³ + λ) using the Hu–Sugiyama
z* fit and ω_γ = 2.47e-5. L1 recomputes the same cases with: Janus-LT background (Cosmo; β enters as ω_c,eff =
(ω_b + ω_c)(1+β) − ω_b at fixed ω_b, which is D715's degeneracy Ω_m(1+β), Neff = 3.044 massless), ω_γ from T_CMB,
z* from Janus-LT's own recombination as τ(z*) = 1 with τ = ∫ x_e n_H σ_T c/[H(1+z)] dz (Recomb gains tau()/z_star()),
r_s(z*) by the L0b integral, R = √(Ω_m,eff) H0 D_M(z*)/c, l_A = π D_M(z*)/r_s(z*).
Cases (as D715): (a′) ΛCDM Ω_m = 0.3153, h = 0.6736; (b) β = 0.192, H0 = 72.95 with λ renormalised (D715 case c).
Validation step V: for (a′), compare z*, r_s(z*), D_M(z*) with CAMB 2.0.5 derived zstar, rstar, DAstar×(1+z*) (YHe 0.24,
ω_b 0.02237): pass if |Δz*/z*| ≤ 2e-3 and |Δl_A/l_A| ≤ 1e-3. Then report (R, l_A) and σ-distances to Planck
(R = 1.7502 ± 0.0046, l_A = 301.471 ± 0.090) for (a′) and (b), and whether D715's verdict for (b) (fails Planck) changes.
