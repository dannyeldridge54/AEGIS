# PREREG_D1641_G1B_RHO_CURVATURE — why V''/V∞ = 1/4 at ρ (Janus genesis G1b; locked 2026-11-19 ~22:30Z before the numerical check)
Claim derived on paper BEFORE any new number (D1637 gave only the D = 10 value 0.25):
1. f ≡ (2/3) y∂_y ln E(τ,3/2); V = V∞ f²[1 + C(E − E(ρ))]. At ρ: f = 0 (∂_y E = 0), so V''(φ) = 2V∞ (df/dφ)², with d/dφ = b·y d/dy, b = √(D−2)/2.
2. ρ is an order-3 elliptic fixed point of SL(2,Z); the Hessian of a modular-invariant function there must be invariant under a 120° rotation in the hyperbolic plane ⇒ isotropic: ∂_x²E = ∂_y²E at ρ.
3. Laplace eigen-equation y²(∂_x² + ∂_y²)E = s(s−1)E = (3/4)E ⇒ y²∂_y²E = (3/8)E at ρ.
4. y d/dy (y∂_yE/E) at ρ = (y∂_yE + y²∂_y²E)/E = 3/8 ⇒ y df/dy = 1/4 ⇒ df/dφ = b/4.
5. ⇒ V''/V∞ = 2b²/16 = b²/8 = (D − 2)/32, and m²/H∞² = 3(D − 2)/32 (H∞² = V∞/3M_P²). D = 10: 1/4 (matches D1637), m/H∞ = 0.866.
Prediction (locked): numerical V''/V∞ at ρ from p3s.V (C = 8e-7 and C = 0) equals (D−2)/32 for D = 10, 6, 4 (0.25, 0.125, 0.0625), and ∂_x²E = ∂_y²E at ρ numerically.
Pass rule: PASS if every case agrees to relative 1e-8; else FAIL (step 2 or 3 wrong). Tilt factor 1 + C(E − E(ρ)) = 1 at ρ, so C must not matter.
Script: field_tests/scripts/janus_g/g1b_rho_curvature.py → field_tests/results/D1641_G1b_rho_curvature.json
