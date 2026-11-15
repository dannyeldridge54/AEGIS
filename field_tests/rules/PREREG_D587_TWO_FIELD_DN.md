# PREREG D587: two-field δN check of D582 (axion Re τ) for two-term SERAPIS, locked before computing

Model: V = I²/(I² + 1) + ε I₁ with ε = 1e-4 (D575/D581). Field-space metric G_ab = δ_ab/(2y²) (K = −ln(2y), α = 1/3, M_P = 1).
j from the q-series j = 1/q + 744 + 196884q + 21493760q² + 864299970q³ (valid for y ≥ 1.5; inflation ends at y ≈ 2.8).

Equations (e-folds): φ″ + Γ(φ′, φ′) + (3 − ε_H)(φ′ + G⁻¹∇V/V) = 0, with ε_H = ½Gφ′φ′. Christoffels: Γ^x_xy = −1/y, Γ^y_xx = 1/y, Γ^y_yy = −1/y.

Runs:
- Start at y₀ = y*(N* = 50) taken from the single-field D575 code (recomputed), on the slow-roll attractor (velocity from the slow-roll formula).
- Offsets x₀ ∈ {0, 1e-4, 1e-3, 1e-2, 3e-2}. Integrate to ε_H = 1 and record N(x₀).

Report:
- ΔN(x₀) = N(x₀) − N(0), and N_xx from a fit ΔN = ½N_xx x₀² over the points with |ΔN| above numerical noise.
- δN_iso = ½|N_xx|δx², with δx = √2·y₀·H/(2π) and H from D581 (H/M_P = 2.2e-6). Compare to ζ = 4.6e-5 (√A_s).
- Also check that x stays within 1% of x₀ at the end (frozen axion).
- Self-check: N(0) must agree with the single-field N* within 0.5 e-fold.

Verdict: D582 is CONFIRMED if δN_iso/ζ < 1e-3; otherwise D582 is revised. Fixes go in PREREG_D587_DEVIATIONS.md, written first.
