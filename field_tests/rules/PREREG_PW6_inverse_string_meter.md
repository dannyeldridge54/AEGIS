# PREREG PW6 — web postulate 6: the inverse string meter (future n_s → Im S·Im ρ at the leptogenesis T_R)
Locked 2026-11-18 04:35Z before computing. Pattern: PW2 (point, T_R fixed by leptogenesis c = 1, M_H = 1e12) + PW5 (n_s measures C ∝ 1/(Im S·Im ρ)).
Inputs: SERAPIS-E, T_R = 7.389e8 GeV, g* = 228.75 (A1), N_eff = 4, C = 15·4/(64π⁶·P) with P = Im S·Im ρ; benchmark P = 780.1 ↔ C = 1.25e-6 (n_s 0.974393).
Compute, for target n_s ∈ {0.970, 0.972, 0.974, 0.976, 0.978}:
 (1) linear inverse from PW5's measured response: P_lin = 780.1·exp(−(n_s − 0.974393)/0.011711);
 (2) exact inverse: secant on ln C with pipeline.predict_fast (U2: Janus N* + U1b exact MS) to |Δn_s| ≤ 2e-6; report P_exact, C, N*, r, α_s.
Pre-stated expectation: |P_lin/P_exact − 1| ≤ 3 % for n_s 0.972–0.976 (PASS), and the "natural" range P = 560–975 (SERAPIS-E paper) maps to n_s ≈ 0.972–0.978.
Reading: PASS ⇒ node inverse_meter (status postulate) with the table; FAIL ⇒ record the nonlinearity, linear meter flagged.
Script: field_tests/scripts/pw6.py. Results: field_tests/results/pw6_inverse_meter.txt.
