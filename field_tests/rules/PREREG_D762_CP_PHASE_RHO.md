# PREREG D762: probability that the ρ-branch leptogenesis phase is large enough, under postulate P1
Locked 2026-11-16 before computing. Script: theory/modular/cp_phase_rho_d762.py. Output: field_tests/results/cp_phase_rho_d762.txt.
Inputs: the D731 table of required sin δ_min (0.56, 0.12, ≤0.01, ≤0.01, 0.12, 0.09, ≤0.01, 0.08, 0.04; "≤0.01" taken as 0.01).
Method: under P1 (δ uniform), P(|sin δ| ≥ s) = 1 − (2/π) arcsin(s). Report it for each case, then the minimum, the median and the fraction of cases with P ≥ 0.9.
Regression check (K4): s = 0 → P = 1; s = 1 → P = 0; s = 1/√2 → P = 0.5.
Decision:
- NATURAL if the median P ≥ 0.8 and the minimum P ≥ 0.5.
- MARGINAL if the minimum P < 0.5 but the median P ≥ 0.8.
- TUNED otherwise.
With gCP imposed the result is ε = 0 by the theorem (no computation needed); it is recorded alongside.
