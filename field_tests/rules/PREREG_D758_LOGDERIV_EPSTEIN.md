# PREREG D758: a species-type plateau built from the Epstein series, V ∝ G^{ττ̄}|∂_τ ln E(τ,2)|²
Locked 2026-11-16 before computing. Script: theory/modular/logderiv_epstein_d758.py. Output: field_tests/results/logderiv_epstein_d758.txt.
Origin (outward; literature construction): arXiv:2407.12081 builds V = μ²M_P²·G^{ττ̄}(∂Λ/Λ)(∂̄Λ/Λ) from the species scale Λ, using ln|η| (s = 1). Basu 0708.2950 (D707) gives an 8D D⁴R⁴ coefficient c(U) = A − B·E(U,2). In the limit A ≪ B·E the species log-derivative is that of E(U,2), giving V ∝ G^{ττ̄}|∂ ln E(τ,2)|². This is NOT the D707–D709 route (those used Λ or 1/E directly); it uses the log-derivative.
## Computation (fixed now)
G^{ττ̄} = 4y² (K = −ln 2y, α = 1; also α = 1/3, G^{ττ̄} = 4y²/3, i.e. a rescaled kinetic term, stated). Along Re τ = ½ from ρ.
1. Check V(ρ) = V(i) = 0 (stationary).
2. The large-y approach exponent: fit V/V_∞ = 1 − c·y^{−p}.
3. Slow roll with the canonical field φ = ln(y)/√(2α) … (state it): n_s, r at N* = 48, 50, 52. Compare with the frozen SERAPIS bands and the plain-attractor ceiling (D752: n_s ≤ 0.9677).
Decision: report as a new plateau CANDIDATE with a literature-motivated origin. CANDIDATE if n_s and r land inside or near any frozen band; otherwise record its location (a new rung of the D700 ladder). Post-hoc; nothing frozen changes.
