# PREREG D1444 — D1442's second-order offset model at the four remaining audited-box corners

Locked 2026-11-19 (UTC) before computing (JANUS tick 40, node janus).
Exact MS references (field_tests/results/a1_mssm_gstar.txt, MSSM rows, D1262):
 K3: C 1.0e-6,  T_R 5.455e8 — n_s 0.971663, r 4.52911e-4, α_s −9.4017e-4
 K4: C 1.15e-6, T_R 5.455e8 — n_s 0.973232, r 4.70877e-4, α_s −9.7704e-4
 K5: C 1.15e-6, T_R 1.653e10 — n_s 0.974320, r 4.57135e-4, α_s −9.4741e-4
 K6: C 1.3e-6,  T_R 1.653e10 — n_s 0.975959, r 4.76299e-4, α_s −9.8543e-4
Method identical to D1443 (field_tests/scripts/d1443/corners.py; dps 30; guesses C_r = corner C, y* 14.6; impl check |C_r/C − 1| < 10 %).
Rule: PASS if max |α_pred/α_exact − 1| < 0.5 % over K3–K6; FAIL otherwise. Together with D1442/D1443 this completes all 7 exact points.
No reruns to chase results; fixes only via PREREG_D1444_DEVIATIONS.md first.
