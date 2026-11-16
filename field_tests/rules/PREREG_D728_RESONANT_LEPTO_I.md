# PREREG D728: non-thermal (resonant) leptogenesis from φ → N₁N₂ at τ = i with the unsuppressed (D727) decay
Locked 2026-11-16 before computing. Script: theory/modular/lepto_i_d728.py. Output: field_tests/results/lepto_i_d728.txt.
## Inputs (fixed now; D597 conventions except the corrected T_R)
- m = 1.9e11 GeV; M/m ∈ {0.1, 0.2, 0.33, 0.45}; m_ν = 0.05 eV; v = 174 GeV; g* = 106.75.
- Γ_N = m_ν M²/(8π v²); x = ΔM/Γ_N; ε = x/(1+x²) (D597 regulator, max ½).
- T_R from D727 (λ = √2·1.2635, pseudoscalar width), INDEPENDENT of ΔM.
- Y_B = (8/23)(3/4)(T_R/m)·2ε (each decay gives two N; maximal CP phase; Br(NN) = 1; washout neglected for T_R ≪ M — checked and reported as T_R/M).
- Scan ΔM/M = 1e-8 … 0.5 (log grid, 16 points), plus the D690 2⊕1 range ΔM/M = 0.08–0.5 explicitly.
- Cross-check against the hierarchical Davidson–Ibarra bound ε_DI = 3 M m_ν/(16π v²): report ε/ε_DI (values ≫ M/ΔM·ε_DI flag the formula's validity).
## Decision rule (written before running)
- PASS if some point has Y_B ≥ 8.75e-11 with T_R ≥ 150 GeV; state the allowed ΔM/M range.
- NATURAL PASS if the D690 2⊕1 range (ΔM/M 0.08–0.5) passes.
- FAIL otherwise. This updates the D597 verdict (NOT VIABLE) and the paper's "leptogenesis from inflaton decay fails" paragraph.
- Fixes only via D728_DEVIATIONS.md.
