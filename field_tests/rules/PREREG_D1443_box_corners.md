# PREREG D1443 — does D1442's second-order offset model hold at the audited box's extreme corners?

Locked 2026-11-19 (UTC) before computing (JANUS tick 39, node janus).
Exact MS references (field_tests/results/a1_mssm_gstar.txt, MSSM rows, D1262):
 K1: C 1.0e-6, T_R 1.653e10 — n_s 0.972710, r 4.38906e-4, α_s −9.1099e-4 (lowest |α_s|, outside frozen band)
 K2: C 1.3e-6, T_R 5.455e8 — n_s 0.974828, r 4.89722e-4, α_s −1.0144e-3 (highest |α_s|)
Method: identical to D1442 (field_tests/scripts/d1442/second_order.py: same model, formulas, solve) except mpmath dps 30 (was 40; time cap)
and initial guesses C_r = the corner's C, y* 14.6. Solve (C_r, y*) at second order to the corner's (n_s, r); predict α_s.
Implementation check: solved C_r must land within 10 % of the corner's C (same model family), else "no result" for that corner.
Rule: PASS if max |α_pred/α_exact − 1| < 0.5 % over K1, K2; FAIL otherwise. Remaining four corners: next tick if this passes.
No reruns to chase results; fixes only via PREREG_D1443_DEVIATIONS.md first.
