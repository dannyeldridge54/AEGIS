# PREREG D2069: the IMR α_Y step with the radii fixed by v4 (locked before computing)
**Referee pre-check (formula):** under T-duality along one direction of each torus, the IIA complex structure χ = R₂/R₁ maps to the inverse IIB Kähler area, χ = 1/A_IIB (R₂ → 1/R₂).
- So χ is fixed by v4's **Kähler** areas, not by v4's frozen complex structure (this corrects the tick-12 prompt's guess).
- Isotropic visible 4-cycle σ_vis = 20.15 = A₁A₂ with A₁ = A₂, so A = √20.15 = 4.489 and χ = 0.2228. Use the same χ on torus 3 (isotropic assumption, stated).

**Compute:** D2068 with χᵢ = 0.2228 fixed; parameters (β¹, β², ρ) ∈ {(½, 1, ⅓), (1, 1, 1), (½, ½, ⅓)}; base n_a², n_d² ∈ {1, 2}; steps Δn_d² = ±1 if n_c¹ stays an integer, else ±2.

**Verdict:**
- **PASS(fixed radii)** if some (parameter set, base, step) gives |z| ≤ 2. Report how many of the combinations do (look-elsewhere).
- Otherwise FAIL.
