# PREREG D597: minimal Γ₂ ≅ S₃ toy for inflaton → N₁N₂ (off-diagonal) at τ = i, with resonant leptogenesis (locked before computing)

Heavy neutrinos: an S₃ doublet N = (N₁, N₂), M_N = M₀·1 + Λ·A(Y), with A(Y) = [[y₂, y₁], [y₁, −y₂]].
- Y = (y₁, y₂) is the weight-2 Γ₂ doublet, computed from the q-series of E₂ at τ/2 and (τ+1)/2: y₁ = −(1/48)[E₂(τ/2) + E₂((τ+1)/2) − 8E₂(2τ)] and y₂ = −(√3/48)[E₂(τ/2) − E₂((τ+1)/2)].
- Check the expansions: y₁ → 1/8 + 3q, y₂ → √3 q^{1/2}.

At τ = i:
- s = √(y₁² + y₂²); splitting ΔM = 2Λ|s|, so ΔM/M ≈ 2Λ|s|/M₀.
- Eigenvectors U of A(Y(i)). Off-diagonal coupling (UᵀA(Y′)U)₁₂, with Y′ = dY/dτ numerically.
- κ = |(UᵀA(Y′)U)₁₂|/|s|, so λ₁₂ = √2·κ·(ΔM/2M) (canonical φ = δτ/√2). The Kähler normalisation is a scalar and does not affect off-diagonal terms.

Decay and reheating:
- Γ(φ → N₁N₂) = c·m³/(8πM_P²), with c = (M/m)²(1 − 4M²/m²)^{3/2}λ₁₂² (distinct final particles).
- m = 1.9e11 GeV, M = m/3, Br = 1. T_RH as in D578.

Resonant CP asymmetry (two N's, maximal phase):
- ε_eff = x/(1 + x²), with x = ΔM/Γ_N.
- Γ_N/M = m_ν M/(8πv²), with m_ν = 0.05 eV and v = 174 GeV.
- Y_B = (8/23)(3/4)(T_RH/m)·2·ε_eff. Washout is neglected (T_RH ≪ M).

Scan ΔM/M ∈ {1e-8 … 1e-1}, 15 log-spaced points.
Report: κ, T_RH, ε_eff and Y_B per point; max Y_B; and whether any point has Y_B ≥ 8.75e-11 AND T_RH ≥ 150 GeV (sphalerons active).

Verdict:
- VIABLE if some ΔM passes.
- Otherwise NOT VIABLE in this minimal toy; the tension is that the off-diagonal coupling ∝ ΔM while the resonance needs a small ΔM.
Fixes go in PREREG_D597_DEVIATIONS.md, written first.
