# PREREG CROSS — interweave the two inflation lenses: shape from one dimension, tilt from the other

Locked 2026-11-19 (10:35 CT) before computing. Danny 09:59 ("interweave the calculations together … flip-flop through different
calculations") + D1554 (only the k = 2 pair carries inflation: 10D R⁴ E(τ,3/2) gradient ↔ 8D E(τ,2) ratio).
Combinations (engine F, T_R 8.94e8, lens code of PREREG_LENS):
  X1: 10D shape (G32) × (1 + C·(E(τ,2) − E₂ρ))        — tilt from the 8D object
  X2: 8D shape (R2, λ₈ = 0.063298) × (1 + C·(E(τ,3/2) − E₃/₂ρ)) — tilt from the 10D object
C grid: 10^{k/4}, k = −40 … −16 (25 points, quarter-decade) to bracket n_s 0.9706.
Report: C band, r and α_s at n_s 0.9706, and compare with the same-lens tilts (D1554: G32+E_{3/2} r 5.43e-4; R2+E₂ r 5.25e-4).
Expectation stated now: r at fixed n_s is set by the TILT object (D1529 ordering: faster tilt ⇒ lower r): X1 (y² tilt) ≈ 5.25e-4 like R2;
X2 (y^{3/2} tilt) ≈ 5.43e-4 like G32 — i.e. the shape lens is invisible, the tilt lens decides r.
No reruns to chase results; fixes only via PREREG_CROSS_DEVIATIONS.md written first.
