# PREREG D739: which Γ2 weight-k doublets can lift the massless heavy neutrino at τ = ρ?
Locked 2026-11-16 before computing. Script: theory/modular/doublet_weights_d739.py. Output: field_tests/results/doublet_weights_d739.txt.
Context: D720 (weight-2 doublet nilpotent at ρ, null vector n = (1, −i)), D724 (weight-2 mixing lifts it; weight-4 cannot). Literature: 2512.24804 (Γ2 ≅ S3) studies τ = i∞ and i only and leaves ω open.
## Method (fixed now)
Build doublets by repeated 2⊗2→2 products with the weight-2 doublet Y (D597 forms, same contraction as D724's Y4): Y_{k+2} = (Y₂X₁ + Y₁X₂, Y₁X₁ − Y₂X₂) for X = Y_k, k = 2…12. At ρ, for each k report |Y_k|, the overlap |nᵀY_k|/|Y_k| (lifts N2 iff ≠ 0), and the 3×3 rank of [[A(Y), cY_k],[cY_kᵀ, b]] for c = 1, b ∈ {0, 1}.
## Decision rule
- Report the pattern in k (expected from the residual Z3: period 3 in k/2). If the pattern holds through k = 12: state the rule "only doublets of weight k ≡ 2 (mod 6) lift N2 at ρ" as computed for this product chain (not proven for every weight-k doublet basis).
- If the pattern breaks: report it as found.
- Fixes only via D739_DEVIATIONS.md.
