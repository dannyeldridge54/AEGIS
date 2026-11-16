# PREREG D834 (K.3): τ = i vacuum mass from the anti-D3 term
Locked before computing, 2026-11-16.
V_add = −2κB(τ) with B from D831 (same functions, stacks (5, 2), O3 weight 4 per point), placements z_a = 0 and z_a = ½.
Compute at τ = i (finite differences, h = 1e-3 and 1e-4, mpmath dps 30): gradient (B_x, B_y) and Hessian B_xx, B_yy, B_xy.
Canonical field (K = −ln Im τ family, φ = ln y/√2, χ = x/(√2 y)): at an extremum with y = 1, d²V/dφ² = 2V_yy, d²V/dχ² = 2V_xx.
m²/H² = 3·(−2)(κ/V0)·2B_aa (H² = V0/3, M_P = 1), at κ/V0 = 2.07e-4 (D833 bound at y* = 14.0).
Verdict rules: (1) τ = i is an extremum of B for a placement iff |∇B| < 1e-6 at both h; (2) it gives a MINIMUM of V_add iff both eigenvalues of −B's Hessian are > 0; (3) "sufficient" iff the smaller m²/H² ≥ 2e-3 (D795/D826).
Prediction (pre-stated): z_a = 0 placement is SL(2,Z)-invariant, so i is an extremum; since V(ρ) < V(i) (D831), i is a SADDLE or MAXIMUM of V_add along the ρ direction, so verdict (2) fails. z_a = ½ breaks SL(2,Z) and i may not be an extremum.
