# PREREG NA11 — node audit: serapis_e, bhk_tilt, stuck_d3 (core arithmetic of the SERAPIS-E potential)
Locked before computing. Tools: tools/serapis_calc/eisenstein.E_paper, plus an independent direct lattice sum (mpmath, |m|,|n| ≤ L, tail-corrected by comparing L = 200, 400).
1. E(ρ,2) = 5.7833593 and E(i,2) = 6.0268 (D689, D692): direct lattice sum Σ'_{m,n} y²/|m+nτ|⁴ — PASS if both agree with E_paper to 1e-6 relative and with the quoted values to the quoted digits.
2. ρ is the minimum of E(τ,2) and the Hessian there is isotropic (D689: "isotropically quadratic"): ∂²E/∂x² = ∂²E/∂y² at ρ within 1e-6 relative, mixed term ≈ 0, both > 0.
3. Plateau approach (D691): E(½+iy,2) → 2ζ(4) y² (leading); PASS if E/(2ζ(4)y²) → 1 within 1e-3 at y = 30 (subleading πζ(3)/y-type term allowed).
4. bhk_tilt: C = 15 N_eff/(64π⁶ Im S Im ρ). PASS if every row of D696's table reproduces C ∈ [1.0, 1.3]e-6 at its quoted Im S·Im ρ endpoints (±1 % from rounding).
5. stuck_d3 tadpole: 3N + N0 + N_flux = 16 for every D696 row; N_eff = N − N0.
Results: field_tests/results/na11_serapis_e_core.txt.
