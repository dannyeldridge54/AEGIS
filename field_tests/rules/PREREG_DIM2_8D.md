# PREREG DIM2_8D — dimension ladder stage 2 (D = 8): species-gradient plateau along the T² shape U at fixed SL(3) moduli

Locked 2026-11-19 (11:03 CT) before computing. Dimension-ladder loop.
[literature] GRV arXiv:1001.2535 eq. (3.16): E⁽⁸⁾ = Ê^{SL(3)}_{[10];3/2} + 2Ê₁(U), Ê₁(U) = −π log(U₂|η(U)|⁴) (regularised).
Model: Λ₈ ∝ (E⁽⁸⁾)^{−1/6}; along U at fixed SL(3) moduli, E⁽⁸⁾ = A + 2Ê₁(U), A = the SL(3) piece (a constant on this slice).
  V₀(y) = (y∂_y ln(A + 2Ê₁(U)))² on Re U = ½ (y = U₂; large-y limit → 1 since Ê₁ ≈ (π²/3)y − π ln y), φ = ln y/√2, engine F, untilted.
Grid: A ∈ {0, 10, 30, 100}.
Derived before computing: y∂ ln(A + 2Ê₁) ≈ (2π²y/3 − 2π)/(A + 2π²y/3 − 2π ln y) = 1 + (2π ln y − 2π − A)/(2π²y/3) + … ⇒ approach ~ ln y/y
(k ≈ 1, the s = 1 lens); from ABOVE when A < 2π(ln y − 1) (no inflation into ρ, as N1 in D1554), from BELOW for large A (plateau, α-attractor-like).
Report: V₀ profile, untilted n_s, r per A or "no inflation into ρ". Expectation: A = 0 → no inflation (approach from above); A ≥ 30 →
plateau with r ≈ 1–2e-3 (k ≈ 1) — off the k = 2 rung.
No reruns to chase results; fixes only via PREREG_DIM2_8D_DEVIATIONS.md written first.
