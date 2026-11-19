# PREREG D1454 — band_e running from the derived ρ model vs D1421 (A1-anchored) and D693's frozen window

Locked 2026-11-19 (UTC) before computing (JANUS tick 50, node band_e).
Model: ρ second-order offset model (D1442–D1444; solve from d1449/vac_grid.py, dps 30).
Grid: 3×3 n_s {0.969, 0.972, 0.975} × r {4.55, 4.835, 5.12}e-4 — r span as D1421 used (4.55–5.12e-4; like-with-like), n_s band 0.969–0.975.
D1421: α_s −9.4202e-4 … −1.06004e-3 (r-only, k = 1.0352); D693 frozen window −(9.4–10.6)e-4; ACT P-ACT-LB 0.0062 ± 0.0052, P-ACT 0.0060 ± 0.0055.
Rule: D1421 SUPERSEDED if either α_s edge moves > 0.5 %; also report whether the derived range sits inside D693's window ± 0.2e-4
(D1421's consistency criterion) and the ACT pulls (PASS if all |pull| < 2). The n_s dependence at fixed r (absent from D1421's
r-only formula) is reported as max/min α_s spread across n_s at each r.
No reruns; fixes only via PREREG_D1454_DEVIATIONS.md first.
