# PREREG JMF2 — JANUS-MF step 2: exact multi-field Mukhanov–Sasaki in Janus, validated against MultiModeCode's exact numbers
Locked 2026-11-17 before any JMF2 number. Equations [fetched, MMC paper arXiv 1410.0685]: mode equation (3.12)/(3.14) in e-folds
ψ_IJ'' + (1 − ε)ψ_IJ' + (k²/(a²H²) − 2 + ε)ψ_IJ + C_IL ψ_LJ = 0, mass matrix (3.11) C_IJ = V_IJ/H² + (φ'_I V_J + φ'_J V_I)/H² + (3 − ε)φ'_I φ'_J,
Bunch–Davies start (3.16–3.17; implemented with the exact de Sitter mode as in ms.py at k/aH = 1000), P_δφ^IJ = k³/(2π²a²) Σ_L ψ_IL ψ*_JL (3.19),
P_R = ω_I ω_J P_δφ^IJ/(2ε) (3.23), ω = φ'/|φ'|, evaluated at the end of inflation (ε = 1; the exact, post-conversion value). Tensors: single-field equation
h'' + (3 − ε)h' + (k/aH)²h = 0 with P_h = 8k³|h|²/(2π²) (ms.py convention). n_s, r at the pivot that exits 55 e-folds before ε = 1, n_s from a quadratic fit
of ln P_R over 9 points on ln k ∈ k* ± 0.4. Implementation: tools/janus_calc/mfms.py (new).
Test models = JMF1 (D1161): V = ½(m₁²φ₁² + m₂²φ₂²), m₁² = 1e-11, R = m₂/m₁ ∈ {1, 3, 9}, φ_init (12, 12).
Targets [MMC exact, D1161]: n_s = 0.963372, 0.945477, 0.927745; r = 0.14405, 0.14464, 0.14568.
Claims: C1 |n_s^Janus-MF − n_s^MMC| ≤ 2e-4 at all R (2e-4 allows for the differing start/finite-difference choices of the two codes); C2 |r/r_MMC − 1| ≤ 2e-3.
Both → JANUS-MF EXACT VALIDATED; else NOT. Also reported: improvement over Janus δN (D1161 errors 1.3e-4, 7.6e-4, 1.7e-3).
Results: field_tests/results/janus_jmf2.txt.
