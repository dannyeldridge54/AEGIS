# PREREG D577: SERAPIS-KL plateau + species-scale mass term (Casas–Ibáñez "moduli self-fixing" form), locked before computing

Motivation:
- D574: the SERAPIS-KL vacuum is massless.
- D575: an ε·I₁ mass term also tilts the plateau.
- Casas & Ibáñez (arXiv:2507.05345, eq. 4.6) give a positive-definite one-loop term δV ∝ g^{ττ̄}|∂Λ_sp/Λ_sp|² whose minima sit at the desert points.
- Using Λ_sp ∝ N^{-1/2} with N = −6 ln(2y|η|⁴) + Ñ₀, and ∂_τ ln(y|η|⁴) = (πi/6)Ĝ₂ (derived), gives V_CI = y²|Ĝ₂|²/N², up to a constant.
- Ĝ₂ has a simple zero at i (D555), so this term should be QUADRATIC at i: massive.

Model (post-hoc; scored only on future data):
- V/V₀ = I²/(I² + 1) + κ·V_CI, with p = 2 and I from D545. α = 1/3 kinetic term.

Scan, all reported, none selected: κ ∈ {1e-3, 1e-2, 1e-1}; Ñ₀ ∈ {25, 100}; N* ∈ {52, 55.6}.

Report for each:
- the vacuum slope exponent at i (expected 2) and m/H_inf;
- y_end, y*, home-safe (y* ≤ 25), n_s, r;
- the shift in n_s relative to κ = 0 (pure HS-Kairos, recomputed by the same code).

Checks:
- Ĝ₂(i) = 0 to 1e-12.
- The analytic identity ∂_τ ln(y|η|⁴) = (πi/6)Ĝ₂, checked numerically at τ = 0.3 + 1.2i to 1e-6.

Verdict rule: the mass and the tilt are DECOUPLED if some κ gives a slope of 2 at i AND |Δn_s| < 0.002 versus κ = 0 for both Ñ₀ values. Otherwise the Ñ₀ dependence (D559) returns. Fixes go in PREREG_D577_DEVIATIONS.md, written first.
