# PREREG D793: exact observables of the self-diluted ρ history (D792)
Locked 2026-11-16 before computing. Script: theory/modular/selfdil_exact_d793.py (the D781 code with the T₂ list changed; nothing else). Output: field_tests/results/selfdil_exact_d793.txt.
Runs: C ∈ {1.0, 1.15, 1.3}e-6 × T₂ ∈ {3e2 (K4), 150, 330, 1100} GeV.
K4: T₂ = 3e2 reproduces D781 (C = 1.15e-6: N* 45.12, n_s 0.9683, r 5.371e-4).
Side checks (arithmetic in the script):
- the wino freeze-out T_f = M₂/20 < T₂ for M₂ ≤ 1.85 TeV (T_f ≤ 92.5 GeV) for each T₂;
- the thermal gravitino yield 1.9e-12·T₂/1e10;
- BBN: T₂ ≫ 5 MeV.
Report the n_s and r ranges over the grid. Post-hoc row values = min–max over C ∈ [1.0, 1.3]e-6 and T₂ ∈ [150, 1100].
