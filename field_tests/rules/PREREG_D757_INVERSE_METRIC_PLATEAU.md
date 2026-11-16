# PREREG D757: does the BHK loop term in the inverse Kähler metric produce a plateau?
Locked 2026-11-16 before computing. Script: theory/modular/inverse_metric_d757.py. Output: field_tests/results/inverse_metric_d757.txt.
Model (fixed now): K = −ln(2y) + c′E(U,2), c′ > 0; W = W₀ constant; the other moduli are assumed no-scale (they cancel −3|W|² exactly), so V/(|W₀|²e^{K₀}) = e^{c′E}·[K^{UŪ}|K_U|² − 1]·(1/2y) normalisation dropped. Along Re U = ½.
Checks:
1. Δ_hyp E(τ,2) = 2E numerically at τ = ½ + i{1, 2, 5} (finite differences).
2. K_{UŪ} = (1 + 2c′E)/(4y²) > 0 (no ghost) for c′ > 0.
3. The shape of V(y) for c′ ∈ {1e-4, 1e-3, 1e-2}, y ∈ [1, 30]: is there a region where V approaches a constant (plateau) while c′E ≪ 1 (perturbative)? Report c′E at the would-be plateau.
Decision: PLATEAU ROUTE if a plateau exists with c′E ≤ 0.3. NO (non-perturbative) if a plateau needs c′E ≳ 1; then the loop term can only TILT (SERAPIS-E's role), not make the plateau.
