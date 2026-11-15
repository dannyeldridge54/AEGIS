# PREREG D720: SERAPIS-E reheating temperature from its decay channels at τ = ρ
Locked 2026-11-15 before computing. Script: theory/modular/tr_rho_d720.py. Output: field_tests/results/tr_rho_d720.txt.

## Question
D692 set T_R ≈ 1e6–1e8 GeV by scaling the τ = i estimate as m_φ^{3/2}. Replace that by the documented channel formulas (D589/D597/D601) evaluated at the SERAPIS-E vacuum τ = ρ with m_φ = 2.2e13 GeV, then feed T_R to the D719 matching equation.

## Inputs (fixed now)
1. Sterility check at ρ (computed): the gradient of the invariant physical mass y^k|Y|² (Γ2 weight-2 doublet, k = 2) at ρ must vanish (< 1e-8 relative), as at i (D589a). If it does NOT vanish, diagonal channels are open and the result is reported as INCOMPLETE (diagonal width not modelled) — no further fitting.
2. Off-diagonal coupling κ(ρ): same construction as D597 (A(Y), Takagi-normalised eigenvectors, κ = |(UᵀA(Y′)U)₁₂|/|s|) at τ = ρ = e^{2πi/3}, Γ2 doublet from D597's E2 combination. If the doublet's two eigenvalues are exactly degenerate at ρ, record it (then ΔM must come from elsewhere, as D664 found at i).
3. Width: Γ = c m³/(8π M_P²), c = (M/m)²(1 − 4M²/m²)^{3/2} λ², λ = √2 κ (ΔM/2M) (D597 formula). Grid: m = 2.2e13 GeV; M/m ∈ {0.1, 0.2, 0.33, 0.45}; ΔM/M ∈ {1e-3, 1e-2, 0.1, 0.3}. g* = 106.75 (MSSM-like 228.75 recorded too). T_R = (90/(π² g*))^{1/4} √(Γ M_P).
4. Sfermion/SM channels: D601 scaling (∝ m_soft⁴/(M_P² m)), stated as subdominant if below the N channel; not re-derived.
5. N* from the D719 code at the central and edge T_R values.

## Decision rule (written before running)
- Primary band = M/m ∈ [0.2, 0.45], ΔM/M ∈ [1e-2, 0.3] (generic non-degenerate splitting, as D601).
- CONSISTENT with D692 if the primary T_R band overlaps 1e6–1e8 GeV; report the N* band it implies and whether n_s stays inside the frozen 0.970–0.975 (lock D693) at C = 1.15e-6.
- INCONSISTENT if the primary band lies wholly outside 1e6–1e8 → correction note, no retuning of frozen bands; record the implied n_s shift.
- NULL if κ(ρ) cannot be computed (e.g. doublet undefined at ρ).
- Fixes only via D720_DEVIATIONS.md written before any rerun.

## Labels
computed / estimate / literature on every number.
