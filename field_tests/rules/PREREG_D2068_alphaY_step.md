# PREREG D2068: the size of the α_Y step from one lepton-stack wrapping step in the IMR model, mapped to α_s (locked before computing)
**Formulas:**
- 1/α_x = K·V_x, with V_x = Π_i √(n_i² + m_i² χ_i²) (D6 volume, R₁ᵢ = 1, χᵢ = R₂ᵢ/R₁ᵢ).
- 1/α_Y = (1/6)/α_a + (1/2)/α_c + (1/2)/α_d (IMR, U(N) normalisation).
- K is set so that 1/α_a = 27.94 at the base point (v4's α_G).

**Parameters:** β¹ = 1/2, β² = 1, ρ = 1/3, ε = 1. Then n_c¹ = n_a² + n_d², which is an integer for Δn_d² = ±1. Base n_a², n_d² ∈ {1, 2}.

**Step:** n_d² → n_d² ± 1, with n_c¹ following. Compute δ(1/α_Y), then α_s = 1/(1/0.1142 + 0.714·0.6·δ(1/α_Y)) (v4 base; GUT normalisation assumed).

**Draws:** χᵢ log-uniform in [0.2, 5], 20,000 draws × 4 bases × 2 signs.

**Report:** the fraction with |z_PDG| ≤ 2, and the median |δ(1/α_Y)|.

**Verdict:**
- **NATURAL** if the fraction is ≥ 0.2;
- **POSSIBLE** if it is 0.05–0.2;
- **UNNATURAL** if it is below 0.05.
