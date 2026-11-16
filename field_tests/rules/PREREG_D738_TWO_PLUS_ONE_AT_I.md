# PREREG D738: the consistent 2 ⊕ 1 (W2, b = 0) heavy-neutrino sector at τ = i — spectrum, splitting ΔM/M, inflaton couplings, T_R
Locked 2026-11-16 before computing. Script: theory/modular/two_plus_one_i_d738.py. Output: field_tests/results/two_plus_one_i_d738.txt.
Purpose: D728 assumed the 2⊕1 splitting ΔM/M ≈ 0.08–0.5 (D690, made before D727). Check it with the D725 method at i.
## Method (fixed now)
- M_phys = (2y)·[[A(Y), cY],[cYᵀ, 0]], c ∈ {0.3, 1, 3}, at τ = i; degeneracy-safe Takagi (D725); P = Uᴴ ∂_y M U* along the imaginary axis.
- Report singular values, the ΔM/M between the two lightest states, |P_ab| (all pairs), and linear splitting rates for any degenerate block (cone check, D726).
- Canonical normalisation at i as D589/D597: λ_ab = √2·|P_ab|/s_ref per unit mass, so Yukawa g_ab = λ_ab·M_ref/M_P with M_ref fixed by setting the decaying light state to M/m ∈ {0.2, 0.33, 0.45}, m = 1.9e11 GeV. Widths: identical pair g²m(1−4x²)^{3/2}/16π (scalar part) or the pseudoscalar form g²m(1−4x²)^{1/2}/16π (use the larger, state it); distinct pair as D725. Only kinematically open channels.
- Then Y_B with the D728 formula for the lightest pair's ΔM/M.
## Decision rule
- CONSISTENT with D728 if ΔM/M lies in D728's passing range for that M/m and Y_B ≥ 8.75e-11. Otherwise a correction note to D728.
- Fixes only via D738_DEVIATIONS.md.
