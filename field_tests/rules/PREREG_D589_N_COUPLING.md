# PREREG D589: a microscopic inflaton → N₁N₁ coupling, and whether it gives enough T_RH for leptogenesis (locked before computing)

Coupling: L ⊃ −½M(φ)NN with M = M₁f(τ), so the coupling is g = M₁λ/M_P, with λ = d ln M/dφ (canonical φ = δτ/√2 at τ = i, α = 1/3).
Width (scalar → Majorana pair): Γ = (g²/16π)·m·(1 − 4M₁²/m²)^{3/2}.
D518 convention: c_eff = Γ/(m³/(8πM_P²)) = ½(M₁/m)²(1 − 4M₁²/m²)^{3/2}λ².

Check, fixed now:
- λ for E₄: d ln E₄/dτ = (πi/3)(E₂ − E₆/E₄), which at i is (πi/3)E₂(i) = i (since E₂(i) = 3/π). So |λ| = √2·1 = 1.414.
- Verify E₂(i) = 3/π numerically to 1e-10.

Scan: λ ∈ {1, √2, 3, 6.6, 10}; M₁/m ∈ {1/3, 0.316}; C1 model (ε = 1e-4), m = 1.9e11 GeV.
- T_RH from Γ_tot = Γ_NN (Br = 1, the best case for Y_B).
- Y_B,max from D579 (Davidson–Ibarra bound, hierarchical N).
- Report the λ needed for Y_B ≥ 8.75e-11.

Verdict:
- If the natural λ (≈ 1–1.4, from E₄) fails, non-thermal leptogenesis with hierarchical N is NOT natural. The model then needs resonant enhancement (quasi-degenerate N₁, N₂; Ding et al. use this) or |λ| ≳ the computed threshold.
- Note: the linear δτ·NN coupling must also be allowed by the residual S-symmetry at i (N weight assignment). That is flagged, not computed here.
