# PREREG D1399 — audited SERAPIS-E box through the Janus relation, scored on ACT DR6 running

Locked 2026-11-19 (UTC) before computing (Danny: "Janus nodes derivation through our pipeline", JANUS tick 1).

Node: band_e_audited (POSTULATE, D1245): n_s 0.9717–0.9760, r 4.39–4.90e-4.
Relation: Paper 1 consistency relation (D669), tools/serapis_calc/relation.py alpha_s(n_s, r, p, kappa) with the
pipeline values p = 2√2 = 2.8284, kappa = 1 (as in the circuit and the studio L_bridge check).
Grid: n_s in 0.9717..0.9760 and r in 4.39e-4..4.90e-4, 41 × 41 points, corners included.

Data (fetched 2026-11-19 from ACT DR6 extended models, arXiv:2503.14454 §4.1, 68% CL):
  P-ACT-LB  dn_s/dlnk = 0.0062 ± 0.0052   (primary)
  P-ACT     dn_s/dlnk = 0.0060 ± 0.0055   (cross-check)
Report: alpha_s range over the box; pull (alpha_s − mean)/sigma for each data set; beta_s range too (no data test).

Rule (primary, P-ACT-LB): PASS if every box point has |pull| < 2; FAIL if any point has |pull| ≥ 2.
Resolving power, stated before computing: the box predicts |alpha_s| of order (1−n_s)²/2 ~ 4e-4, about 0.1σ of the data
error, so a PASS is "consistent, not yet tested"; the honest tier stays POSTULATE. A test with discriminating power needs
σ(alpha_s) ≲ 2e-4 (e.g. future CMB-S4/LiteBIRD-class plus LSS); record that requirement.
No reruns to chase results; fixes only via PREREG_D1399_DEVIATIONS.md written first.
