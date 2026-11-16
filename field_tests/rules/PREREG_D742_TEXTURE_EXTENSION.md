# PREREG D742: smallest extension of the τ = i Weinberg texture that gives normal ordering with Σm_ν ≤ 0.064 eV
Locked 2026-11-16 before computing. Script: theory/modular/texture_ext_d742.py. Output: field_tests/results/texture_ext_d742.txt.
## Textures (fixed now; τ = i, Y = D597 weight-2 doublet, Y4 = (2Y₁Y₂, Y₁² − Y₂²))
(a) [[A(Y), bY],[bYᵀ, d]]: the 3-3 entry d from a singlet form. Weight bookkeeping (k_L = 1 for the doublet, singlet weight k_s free): d needs a level-1 or level-2 singlet of weight 2k_s − 2 + 2 (Weinberg with η^{-2}, D654a). E4(i) ≠ 0, E6(i) = 0, so d is allowed for weights ≡ 0 (mod 4) at i (stated, not derived here).
(b) [[A(Y) + c·A(Y4), bY],[bYᵀ, 0]]: a second doublet form in the 2-2 block.
(c) both: [[A(Y) + c·A(Y4), bY],[bYᵀ, d]].
Scan: |b|, |c|, |d| on log grids 0.01–100 (40 points each), phases in 8 steps (fixed grid, no random draws). (c) uses 25-point log grids and 6 phases.
## Outputs and rule
For each texture: the fraction of grid points with R = Δ_small/Δ_large within ±10% of 0.0297 AND NO AND Σm_ν ≤ 0.064 eV (scale so that Δ_large = 2.5e-3 eV²). Report the best Σm_ν and m_lightest/m_heaviest of those points.
- RESOLVED if any texture has such points. The minimal one is preferred. Tuning = that fraction.
- NOT RESOLVED otherwise → correction note; the frozen value stays frozen.
- Fixes only via D742_DEVIATIONS.md.
