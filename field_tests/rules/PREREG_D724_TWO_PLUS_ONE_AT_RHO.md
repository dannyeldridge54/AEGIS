# PREREG D724: does a 2 ⊕ 1 heavy-neutrino sector give N2 a mass at τ = ρ?
Locked 2026-11-16 before computing. Script: theory/modular/two_plus_one_d724.py. Output: field_tests/results/two_plus_one_d724.txt.
## Model (fixed now)
N = (N1, N2) Γ2 ≅ S3 doublet, N3 singlet. Majorana mass matrix (overall scale Λ):
M = [[A(Y2)  , c·Yw ], [c·Ywᵀ, b]], A(Y) = [[Y₂, Y₁],[Y₁, −Y₂]] (D597), Y2 = weight-2 doublet;
mixing doublet Yw = weight-2 doublet Y2 (case W2) or weight-4 doublet from 2⊗2→2, Y4 = (2Y₁Y₂, Y₁² − Y₂²) (case W4).
b ∈ {0, 0.3, 1, 3}; c ∈ {0.3, 1, 3}. Singlet-form factors folded into b and c (constant O(1)).
## Outputs
1. Takagi singular values at ρ (residual check < 1e-10); rank; smallest/largest ratio R.
2. For R > 0: minimum R over the scan, and whether M_light = R·M_heavy ≳ 1e8 GeV for M_heavy = 1e12–1e13 GeV (needs R ≳ 1e-5 – 1e-4).
3. Holomorphic off-diagonal couplings |(Uᴴ ∂_y M U*)_ij| (i<j) at ρ, for the record (Kähler corrections for mixed weights not modelled; label estimate).
## Decision rule (written before running)
- RESCUE POSSIBLE if some case has rank 3 at ρ with R ≳ 1e-4 for O(1) b, c.
- KILL EXTENDS if every case is rank 2 at ρ (symmetry-forced zero).
- MIXED if only one of W2/W4 works: report which.
- Fixes only via D724_DEVIATIONS.md.
