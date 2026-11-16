# PREREG D778: which Dirac-weight assignments restore a realistic light-neutrino spectrum at ρ?
Locked 2026-11-16 before computing. Script: theory/modular/rho_weights_d778.py. Output: field_tests/results/rho_weights_d778.txt.
Weights (D724 convention, W-weight 0): k_N = k_N3 = −1, so M_R is fixed at weight 2 (the D777 form; no other weight-2 Γ₂ form exists). The Dirac terms of a lepton multiplet L_x have form weight w_x = 1 − k_Lx − k_H, the same for its couplings to N_d and N₃.
Non-zero Γ₂ forms at ρ (D739; E4(ρ) = 0, E6(ρ) ≠ 0):
- doublets: w = 2: Y ∝ (1, i); w = 4: Y₄ = (2Y₁Y₂, Y₁² − Y₂²) ∝ (i, 1); w = 8: E6·Y ∝ Y; w = 6: none (E4·Y = 0, chain = 0);
- singlets: w = 0: 1; w = 6: E6; w = 2, 4, 8: none (or 0 at ρ).
M_D blocks:
- L_d–N_d: α·A(Y_w) for doublet weights, α·𝟙 for singlet weights (0, 6);
- L_d–N₃: β·Y_w (doublet weights only, else 0);
- L₃–N_d: γ·Y_wᵀ (doublet weights only);
- L₃–N₃: δ (w₃ ∈ {0, 6} only).
Scan (w_d, w₃) ∈ {0, 2, 4, 6, 8}²; α = 1; β, γ, δ ∈ {0.2, 1, 5} × {0, 2π/3, 4π/3}, using only those allowed by the weights; c ∈ {0.6, 1, 3}.
Classify as D777 (NO and IO ratios ±10% of 0.0297); normalise c₃² − a² = 2.5e-3 eV².
K4: (2, 2) reproduces D777 (0 NO, 0 IO).
Report per (w_d, w₃): the NO and IO counts and the minimum Σm_ν(NO).
Decision: RESTORED if some assignment has NO points with Σm_ν ≤ 0.064 eV. Name the minimal one (fewest weights ≠ 2).
