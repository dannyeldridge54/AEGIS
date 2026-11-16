# PREREG D732: gravitino → wino dark matter at the SERAPIS-E (ρ) reheating temperature
Locked 2026-11-16 before computing. Script: theory/modular/gravitino_wino_d732.py. Output: field_tests/results/gravitino_wino_d732.txt.
## Inputs (fixed now; literature formulas, stated)
- Thermal gravitino yield, light gauginos: Y_3/2 ≈ 1.9e-12 (T_R/1e10 GeV) (Bolz–Brandenburg–Buchmüller hep-ph/0012052 form, gluino term negligible since m_g̃ ≪ m3/2). T_R ∈ {3.2e8, 3.0e9} GeV (D725).
- m3/2 ∈ {2.5e5, 1.1e6} GeV (D651 window); Γ_3/2 = (193/384π) m3/2³/M_P² (all MSSM channels); T_dec from H(T_dec) = Γ with g* = 10.75 (state the g* used).
- Each gravitino → one wino. Re-annihilation cap: Y_w ≤ Y_ann = H/(s⟨σv⟩) at T_dec, ⟨σv⟩_wino = 3e-24 cm³/s × (1 TeV/M2)² (s-wave, Sommerfeld not included: conservative for the cap).
- Ω_w h² (non-thermal) = 2.74e8 (M2/GeV) Y_w; thermal wino Ω h² ≈ 0.12 (M2/2.9 TeV)². M2 ∈ {0.66, 1.0, 1.85} TeV (D713 window).
## Decision rule (written before running)
- PASS if Ω_thermal + Ω_nonthermal ≤ 0.12 + 2σ (0.124) for some M2 in the window at each T_R; report the allowed M2 range.
- FAIL if no M2 passes at T_R = 3e9; state the rescue (lower T_R branch, or a lighter wino).
- Fixes only via D732_DEVIATIONS.md.
