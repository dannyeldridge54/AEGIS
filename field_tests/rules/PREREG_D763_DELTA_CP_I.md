# PREREG D763: τ = i radiative leptogenesis (D745 set-up) versus the CP sources
Locked 2026-11-16 before computing. Script: theory/modular/delta_cp_i_d763.py. Output: field_tests/results/delta_cp_i_d763.txt.
Setup: the D745 code unchanged (NO, m₁ = 1e-3 eV, tanβ = 10, T_R = 2.9e6, M = 6.3e10, N₃ = 10M, alignment Re H₁₂ = 0). Majorana phases set to 0.
Runs:
- (A) Complex R (the D745 27³ grid), δ_CP ∈ {0°, 90°, 180°, 230°, 270°}: pass fraction and max Y_B.
- (B) Real R (all three angles on a 12-point grid in [0, π), 1728 points), the same δ_CP list.
Regression (K4):
- (A) at δ = 230° must reproduce D745 (68%, max 4.6e-9).
- (B) at δ = 0 must give ε = 0 (max Y_B < 1e-20).
Decision:
- If (A)'s pass fraction varies by < 10 percentage points across δ: P1 (high-energy phases) gives NO δ_CP prediction.
- If (B) passes only for |sin δ| above some threshold: report that threshold as the "low-energy-CP-only" prediction.
- Either way, record that gCP at τ = i would force δ ∈ {0, π}, R real and ε = 0.
