# PREREG D784: the SERAPIS-E wino after the Z₃ late reheating (T₂ = 1e5–1e7 GeV)
Locked 2026-11-16 before computing. Script: theory/modular/wino_late_d784.py. Output: field_tests/results/wino_late_d784.txt.
History (D780–D783): the inflaton decays to heavy N (not a thermal bath). The thermal bath forms at T₂ when the N decay. Gravitinos made before T₂ need a bath, so there are none; and any are diluted anyway.
Gravitinos: Y₃/₂ = 1.9e-12·T₂/1e10 (D732 formula) for T₂ ∈ {1e5, 1e6, 1e7}. Their winos: Ω_nth = 2.74e8·M₂·Y₃/₂ (D732).
Winos re-thermalise and freeze out normally if T₂ > T_f ≈ M₂/20, so Ω_th = 0.12(M₂/2.9 TeV)² (D732 convention).
Gamma rays: the D735 method, f_max(M) = √(L/σ_line), L = 4e-28(M/TeV)² (HESS 2018 Einasto), σ_line = 1.6e-27 + ½·1.1e-26.
Collider floor 0.67 TeV (ATLAS 2603.08315).
Report: the window [0.67, M_max], where f = Ω_total/0.12 ≤ f_max. Also check against 2507.15934's stated exclusion (≥ 1.85 TeV for thermal sub-fractions).
K4: T₂ = 3.2e8 with the D732 non-thermal formula reproduces D732's Ω_total at M₂ = 0.66 TeV (0.017).
Decision:
- The window is CHANGED if [0.67, M_max] differs from D735's 0.67–0.80 TeV by > 0.1 TeV at either end.
- Update the paper row.
