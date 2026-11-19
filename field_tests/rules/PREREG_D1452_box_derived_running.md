# PREREG D1452 — band_e_audited running from the derived ρ model vs ACT (supersedes D1433?)

Locked 2026-11-19 (UTC) before computing (JANUS tick 48, node band_e_audited).
Model: ρ second-order offset model (D1442–D1444; solve(obs) from field_tests/scripts/d1449/vac_grid.py, dps 30).
Grid: 3×3 over the audited box's bounding rectangle n_s {0.97166, 0.97381, 0.97596} × r {4.389, 4.643, 4.897}e-4
(the rectangle is wider than the 6-corner box; stated). Data [literature] ACT DR6 2503.14454 §4.1, 68 %: P-ACT 0.0060 ± 0.0055,
P-ACT-LB 0.0062 ± 0.0052. Pull = (α_s − central)/σ.
Compare with D1433 (A1-anchored): P-ACT −1.256 … −1.275σ, P-ACT-LB −1.367 … −1.387σ.
Rule: D1433 is SUPERSEDED (numbers replaced in the node notes) if the derived pull range edges differ from D1433's by > 0.1σ;
otherwise D1433 is CONFIRMED by the derived model. Also report min/max α_s.
No reruns; fixes only via PREREG_D1452_DEVIATIONS.md first.
