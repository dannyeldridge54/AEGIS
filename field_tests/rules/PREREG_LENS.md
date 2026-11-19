# PREREG LENS — the lens ladder: one equation per dimensional "lens", its plateau shape and its inflation rates

Locked 2026-11-19 (10:12 CT) before computing. Danny 10:00: "the equation is going to change at every lens at the dimensional level to the
shape that it's taking. So every shape is going to have an equation that fits its inflation rates." Follows D1552 (10D ↔ 8D duality).
Lenses (each with its automorphic object F(τ) and its equation; all along Re τ = ½, φ = ln y/√2, normalised V₀ → 1 at large y, V₀(ρ) = 0):
  G32 — 10D R⁴, species gradient:      F = E(τ,3/2),  V₀ = (y∂_y ln F / (3/2))²                 (approach y^{−2})
  G52 — 10D D⁴R⁴, species gradient:    F = E(τ,5/2),  V₀ = (y∂_y ln F / (5/2))²                 (approach y^{−4})
  R2  — 8D T² lattice, ratio:          F = E(τ,2),    V₀ = e/(e+1), e = λ₈(F − F_ρ), λ₈ = 0.063298 (D1552)   (approach y^{−2})
  N1  — 8D/4D one-loop free energy (Casas–Ibáñez, s = 1): F = N = −6 ln(2y|η(τ)|⁴), V₀ = (y∂_y ln N)²   (approach ~ ln y / y)
Tilt per lens: V = V₀·(1 + C·(X − X_ρ)) with X = the lens's own F (for N1: X = N). C scanned on a log grid C = 10^{k/2}, k = −20 … −4
(17 points) to bracket n_s 0.9706 without a second pass.
Report per lens: approach exponent fitted on y ∈ [20, 200] (from 1 − V₀); untilted n_s, r, α_s, N*; the C interval in band and r, α_s at
n_s = 0.9706 (interpolated) if bracketed; rows that fail (no end, N* math errors, tilt-dominated) are INVALID and reported, not rerun.
Engine F (D1521/D1532/D1542: exact to ≤ 1e-5 in n_s), T_R 8.94e8, D1 start rule, 5-point stencil (h = 1e-3) for log-derivatives.
Expectation stated now: G32 and R2 identical untilted (D1552); G52 untilted n_s ≈ 0.960 with r ≈ 1e-4 (k = 4, flatter); N1 r ≈ 1.5–2e-3
(k ≈ 1, α-attractor-like) and n_s ≈ 0.960–0.965 untilted.
No reruns to chase results; fixes only via PREREG_LENS_DEVIATIONS.md written first.
