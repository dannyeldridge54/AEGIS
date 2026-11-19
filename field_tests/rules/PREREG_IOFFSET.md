# PREREG_IOFFSET — can a matter-sector term pull the flavour modulus slightly off i? (locked D1612, 2026-11-19 14:40 CT)
Fact used (symmetry argument, also checked numerically): any smooth SL(2,Z)-invariant function is stationary at i, because S fixes i and acts as −1 on its tangent space. So an offset from i can only arise if i becomes a saddle or maximum of the total potential and the minima move to nearby generic points.
Model (POSTULATE, one-parameter): V_f(τ) = V₀(τ) − κ·F(τ), with V₀ the Zhinü factor (V∞ = 1) and F(τ) = y^{1/2}|η(τ)|² / [y^{1/2}|η|²](i), the simplest non-constant invariant built from η.
Compute: (a) the Hessians of V₀ and F at i (finite differences, h = 1e-4); (b) the critical κ_c where the smallest Hessian eigenvalue of V_f at i crosses 0; (c) for κ/κ_c ∈ {1.01, 1.1, 1.5, 2, 4} the location of the minimum near i (Nelder–Mead from i + 0.01(1+i)), with |u| = |(τ − i)/(τ + i)| and whether τ_min is off the CP lines (x ≠ 0 and |τ| ≠ 1).
Report: the scaling |u|(κ) and whether a CP-violating (generic) minimum ever appears. No pass rule; descriptive. Next steps depend on whether a generic minimum appears.
Script: field_tests/scripts/ioffset/run.py
