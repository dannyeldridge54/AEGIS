# DEVIATIONS for PREREG_D773
D1 (run 1 stopped before part (2) printed anything: 7⁸ ≈ 5.8e6 sympy solves is infeasible). Part (2) is replaced by an exact reduction plus a fast numerical check over the SAME grid. Decision rule unchanged.
Reduction: P = F_p − S·H_p = A + B·t₂ + C·t₃ + D·t₂t₃, with A..D affine in S and integer coefficients.
- ∂_{t₂}P = ∂_{t₃}P = 0 ⇒ t₃ = −B/D, t₂ = −C/D (D ≠ 0).
- Then P = Q(S)/D with Q = AD − BC, quadratic in S with integer coefficients.
- At a stationary point in t, W = 0 and ∂_S W = 0 ⇔ Q(S₀) = 0 = Q′(S₀): a double root of a real quadratic, hence S₀ REAL (Im S = 0, inadmissible).
- D ≡ 0: B(S) = C(S) = 0 gives real S, or no relation at all.
The numeric check enumerates the grid with numpy: for each flux vector, find S₀ from Q's double root (or the D = 0 case) and count admissible solutions with Im S, Im t₂, Im t₃ all > 0.
