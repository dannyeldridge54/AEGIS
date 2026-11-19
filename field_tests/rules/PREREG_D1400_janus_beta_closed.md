# PREREG D1400 — Janus relation at κ = 1: closed form of β_s, checked numerically and scored on Planck 2018

Locked 2026-11-19 (UTC) before computing (JANUS tick 2, node janus).

Claim to test (derived by hand from tools/serapis_calc/relation.py, D669, at κ = 1):
  (1−κx)(1+κ²x) + (1+x)(1−κ³x) → 2(1−x)(1+x), so β_s = −(1−n_s)³(1+x)²/(2(1−x)²) = (1−n_s)·α_s = −(p²r/4)(1−n_s).
Numerical check: evaluate the code's beta_s on a 41×41 grid over the SERAPIS-E audited box (n_s 0.9717–0.9760,
r 4.39–4.90e-4) and at the SERAPIS point (n_s 0.9745, r 4.8e-4), p = 2.8284, κ = 1.
  Rule A: closed form exact — PASS if max |code/closed − 1| < 1e-10 on the grid; else FAIL (and the hand algebra is wrong).
Data (fetched 2026-11-19, Planck 2018 X, arXiv:1807.06211, ΛCDM+running+running-of-running, TT,TE,EE+lowE+lensing,
68%, k* = 0.05 Mpc⁻¹): n_s 0.9625 ± 0.0048, dn_s/dlnk 0.002 ± 0.010, d²n_s/dlnk² 0.010 ± 0.013.
  Rule B: PASS if the box's (α_s, β_s) have marginal |pull| < 2 for both; correlations between the two runnings are not
  available here and are ignored (assumed) — stated as a limitation.
Stated before computing: β_s ≈ −2.5e-5, ~0.002σ of the Planck error, so B can only show consistency.
Also report the hierarchy α_s/(n_s−1) and β_s/α_s at the SERAPIS point.
No reruns to chase results; fixes only via PREREG_D1400_DEVIATIONS.md written first.
