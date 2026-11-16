# PREREG D811: the non-multiplicative BHK remnant at τ = i, computed (accuracy queue item 5; Jl tick 50)
Locked before computing, 2026-11-16.
Setup: the covariant completion (paper Sec. chain; D647–D650, D684). The τ F-term is V_τ = m₃/₂²M_P² e^{L−L(i)} 4y²|∂_τL|², with L = −ln(2y|η|⁴). A BHK correction δK = C·E(τ,2) enters:
- (a) as e^{δK} multiplying everything (D689/D802: cannot move a zero of V);
- (b) through D_τW = W(∂_τ(K + ln W)) → ∂_τL + C∂_τE inside the modulus square;
- (c) through the metric K^{ττ̄}, at second order (a quadratic quantity times O(C)).
Compute g_C(τ) = 4y²|∂_τL + C∂_τE|² (piece b), with its Hessian at τ = i in x and y, for C = 0, 1e-6, 1e-4, 1e-2, 1. Fit the C-linear coefficient of g_xx.
Prediction (pre-stated): near i, ∂_τL ≈ ½(L_xx δx − i L_yy δy) and likewise for E, so g ≈ (L_xx + C E_xx)²δx² + (L_yy + C E_yy)²δy² ≥ 0. Every C keeps i a minimum of V_τ. The linear term 2C·L_xx·E_xx is POSITIVE (both second derivatives are negative along x: −0.298, −3.43; D801). D802's worry of negative curvature therefore does not arise at linear order.
Verdict: g_xx, g_yy ≥ 0 for all C, with a positive linear coefficient → C_crit = ∞ (no destabilisation); otherwise report C_crit.
