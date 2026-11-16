# PREREG D769: P3's axion test, a two-field SERAPIS-E background
Locked 2026-11-16 before computing. Script: theory/modular/axion_two_field_d769.py. Output: field_tests/results/axion_two_field_d769.txt.
Model: K = −ln(Im τ) in D692 units, so L_kin = (ẋ² + ẏ²)/(4y²) (y = e^{√2φ} on x = ½). V = [1 − E_r/E(x, y)]·(1 + C(E − E_r)), C = 1.15e-6, with E(x, y) = D692's Ese (30 Bessel terms) and E_r = E(ρ).
Equations in e-folds, metric G = 1/(2y²) (conformally flat):
- x'' − (2/y)x'y' + (3 − ε)(x' + 2y²V_x/V) = 0
- y'' + (x'² − y'²)/y + (3 − ε)(y' + 2y²V_y/V) = 0
- ε = (x'² + y'²)/(4y²)
- End at ε = 1. Start y = 25 at slow-roll velocity (y′ = −2y²V_y/V, x′ = 0).
Runs: x₀ ∈ {0.5, 0.49, 0.45, 0.4, 0.3, 0.1}.
Report: N_total(x₀), x and y at the end, ∂N/∂x₀ by central difference at 0.45 and 0.3 (using ±0.01), and ∂²N/∂x₀² at ½.
K4: the x₀ = ½ run must match the single-field D692 background's N_total within 0.05 (D692's solver also starts at y = 25).
ζ_axion = |∂N/∂x₀|·δx with δx = √2·y*·H/(2π), H = 2.3e-6, y* = 14.3.
Decision:
- PASS if ζ_axion ≤ 1e-6 for x₀ ∈ [0.3, 0.7] (≤ 2% of 5e-5) and every run ends in the ρ valley (|x_end − ½| < 0.05 or an image).
- Otherwise FAIL (P3 needs an axion mass during inflation, i.e. a new term).
