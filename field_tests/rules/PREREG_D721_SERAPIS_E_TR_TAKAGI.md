# PREREG D721: SERAPIS-E T_R at τ = ρ with a Takagi decomposition
Locked 2026-11-16 before computing. Script: theory/modular/tr_takagi_d721.py. Output: field_tests/results/tr_takagi_d721.txt.
Context: D720 was NULL because the D597 eigen-method divides by s = √(Y₁²+Y₂²) = 0 at ρ (A(Y) nilpotent, singular values 0.2241, 0).

## Method (fixed now)
1. Takagi: A = Uᵀ-diagonalised via SVD, A = W Σ Vᴴ; for complex symmetric A use U = W·diag(phase) with UᴴA U* = Σ (verify residual < 1e-10). At ρ: M1 = Σ₁, M2 = Σ₂ ≈ 0.
2. Coupling: inflaton direction along Re τ = ½ (dτ = i dy). Off-diagonal ∂A in the Takagi basis, a12 = |(Uᴴ ∂_y A(Y) U*)₁₂|. The Kähler factor (2y)^{k/2} multiplies A as a whole and contributes only diagonal terms in this basis (checked numerically: report its off-diagonal size). Canonical field for K = −3 ln(2y): dφ = √(3/2) dy / y (M_P units). Yukawa g12 = M1 · (a12/Σ₁) · y√(2/3) / M_P.
3. Width (scalar → two distinct Majorana fermions, M2 = 0): Γ = g12² m (1 − x²)² /(8π), x = M1/m. m = 2.2e13 GeV; x ∈ {0.1, 0.2, 0.33, 0.45, 0.9}; g* = 106.75. T_R = (90/(π²g*))^{1/4} √(Γ M_P).
4. N* via the D719 code at the min and max T_R of x ∈ {0.2, 0.33, 0.45}.
5. Neutrino-data check (reasoning, labelled): rank of M_N with the doublet alone, and with a third singlet N3 (2 ⊕ 1, D664); what a massless N means for the seesaw.

## Decision rule (written before running)
- NULL if a12 = 0 to 1e-10 relative (channel closed at linear order) or Takagi residual > 1e-10.
- Otherwise report the T_R band (x 0.2–0.45). CONSISTENT with D692 if it overlaps 1e6–1e8 GeV; otherwise a correction note (no retuning of frozen bands), with the implied N* and n_s at C = 1.15e-6 and whether n_s stays inside 0.970–0.975.
- Fixes only via D721_DEVIATIONS.md written before any rerun.
