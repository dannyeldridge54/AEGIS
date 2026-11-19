# PREREG_BASINS — where does a SLOW field drain: i or ρ? (locked D1607, 2026-11-19 13:10 CT)
A slow modulus (e.g. the neutrino field), overdamped by Hubble friction, follows the gradient flow of its potential in the hyperbolic metric: ẋ = −2y²∂ₓV, ẏ = −2y²∂ᵧV, with V = V₀(1 + C(E − E_ρ)), V₀ = (4/9)y²|∇ln E(τ,3/2)|², C = 8e-7. Same spline table and validation as YFORK2 (y ∈ [0.05, 25]).
Start sets: (A) the line y = 3, x = 0 … ½ in 201 steps (the flow above y ≈ 2 is nearly vertical, so this maps entry x to exit); (B) 2000 points uniform in hyperbolic area over the fundamental domain |x| ≤ ½, |τ| ≥ 1, y ≤ 3 (seed 7).
Flow until |∇V| < 1e-10 or for a flow time of 1e4; reduce to the fundamental domain; classify i (|τ − i| < 0.1) / ρ (within 0.1 of e^{iπ/3} or e^{2πi/3}) / other.
Report: (A) the x range draining to i versus ρ; (B) the area fractions f_i and f_ρ.
Criterion: P-F3 is "dynamically natural" if f_i ≥ 0.25 (a random slow field has at least a 1-in-4 chance of tying off at i); otherwise "needs special initial conditions".
Script: field_tests/scripts/yfork/basins.py
