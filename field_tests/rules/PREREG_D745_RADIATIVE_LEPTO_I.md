# PREREG D745: radiative resonant leptogenesis at τ = i, non-thermal (inflaton decay)
Locked 2026-11-16 before computing. Script: theory/modular/radlepto_d745.py. Output: field_tests/results/radlepto_d745.txt.
## Inputs (fixed now)
- Heavy spectrum at Λ: N doublet exactly degenerate, M = 0.33 m_φ = 6.27e10 GeV (m_φ = 1.9e11, D727). N₃ = 10 M, no tree-level mass mixing with the doublet.
- Dirac Yukawas by Casas–Ibarra: m_D = i U* √m R √D, Y = m_D/v_u. Normal ordering; Δm²₂₁ = 7.42e-5, Δm²₃₁ = 2.5e-3 eV²; PMNS angles 33.4°, 8.6°, 49° and δ = 230° (fixed values, labelled literature/from memory); m₁ ∈ {1e-4, 1e-3, 5e-3} eV. R = complex orthogonal R₁₂(z₁)R₁₃(z₂)R₂₃(z₃) on a fixed grid: Re z ∈ {0.3, 0.9, 1.5}, Im z ∈ {−0.5, 0, 0.5} for each angle (729 R's). v_u = 174 sinβ GeV.
- Alignment at Λ: rotate the degenerate pair (O(2)) so that Re H₁₂ = 0, H = Y†Y (hep-ph/0507092).
- CP asymmetry (literature formula, hep-ph/0507092): ε_j ≃ (3y_τ²/32π)·Im H₂₁·Re[Y₃₁*Y₃₂]/[H_jj(H₂₂ − H₁₁)], j = 1, 2, with D_j = 1 (check |δ_N| > Γ_N/M, report the fraction where it fails). MSSM y_τ = m_τ/(v cosβ), m_τ = 1.777 GeV, tanβ ∈ {5, 10, 20}.
- Non-thermal yield: Y_B = (8/23)(3/4)(T_R/m_φ)(|ε₁| + |ε₂|)·sign. T_R = 2.9e6 GeV (D727 at M/m = 0.33). Upper estimate with maximal sign alignment.
## Decision rule (written before running)
- Report the fraction of the R grid with Y_B ≥ 8.75e-11 for each (m₁, tanβ).
- PASS if the fraction is ≥ 10% for some tanβ ≤ 10 (natural). MARGINAL if 1–10%. FAIL if < 1% everywhere.
- Caveats to state: an analytic leading-order formula, not a full RGE solution; alignment basis chosen at Λ.
- Fixes only via D745_DEVIATIONS.md.
