# PREREG DIM1_9D — dimension ladder stage 1 (D = 9): the species-gradient plateau along τ at fixed circle modulus ν₁

Locked 2026-11-19 (11:00 CT) before computing. Dimension-ladder loop.
[literature] Green–Russo–Vanhove arXiv:1001.2535 eq. (3.7): E⁽⁹⁾_(0,0) = ν₁^{−3/7}E_{3/2}(Ω) + 4ζ(2)ν₁^{4/7}, ν₁ = (r_B/ℓ₁₀)^{−2};
Laplace equation (Δ⁽⁹⁾ − 6/7)E⁽⁹⁾ = 0. E_{3/2} = Σ' y^{3/2}/|m + nΩ|³ (= 2ζ(3)y^{3/2} + 4ζ(2)y^{−1/2} + …, our normalisation).
Model: species scale Λ₉ ∝ (E⁽⁹⁾)^{−1/7}; at fixed ν₁ the τ-dependence is through E_{3/2} + c, c = 4ζ(2)ν₁.
  V₀(y) = (y∂_y ln(E_{3/2} + c) / 1.5)² on Re τ = ½ (normalised → 1 at large y; V₀(ρ) = 0), φ = ln y/√2, engine F, T_R 8.94e8, untilted.
Grid: ν₁ ∈ {0 (10D limit), 0.1, 1, 10} ⇒ c ∈ {0, 0.658, 6.58, 65.8}.
Derived before computing: ln(E + c) = ln E + ln(1 + c/E) ⇒ y∂ ln(E + c) = (y∂ ln E)·E/(E + c) ⇒ V₀ ≈ (1 − 7.30y^{−2})(1 − 2c/(2ζ(3)y^{3/2})):
for c > 0 the y^{−3/2} piece dominates at large y ⇒ approach exponent k = 3/2 (not 2) — the 9D lens leaves the inflation rung unless ν₁ → 0.
Report: fitted k (y 20–200), untilted n_s, r; compare with the k = 3/2 pure-power chart row (UCHART k = 1.5: 0.9608 / 6.9e-4).
Expectation: ν₁ = 0 reproduces 10D (0.96006 / 4.04e-4); ν₁ ≥ 1 gives r ≈ 6–7e-4 (k ≈ 1.5) ⇒ off the band rung.
No reruns to chase results; fixes only via PREREG_DIM1_9D_DEVIATIONS.md written first.
