# PREREG D1404 — frozen SERAPIS-E band (band_e) re-checked against end-2025 data, with α_s = −2r (D1399–D1400)

Locked 2026-11-19 (UTC) before computing (JANUS tick 4, node band_e; frozen band — this is a re-check, the band is not changed).
Band: n_s 0.970–0.975, r 4.55–5.12e-4 (map title). α_s from the Janus relation at κ = 1, p = 2.8284: α_s = −p²r/4.
Data (fetched 2026-11-19):
  arXiv:2512.10613 (Planck+SPT+ACT+BICEP/Keck): n_s = 0.9682 ± 0.0032 (CMB); 0.9728 ± 0.0029 (CMB + DESI BAO); r < 0.034 (95%).
  arXiv:2503.14454 §4.1 (ACT DR6, 68%): dn_s/dlnk = 0.0062 ± 0.0052 (P-ACT-LB).
Rules (primary data set CMB + DESI, the combination AEGIS bands are scored on):
  R1 n_s: PASS if some n_s in the band has |pull| < 2 vs CMB + DESI; report the fraction of the band inside 2σ for CMB + DESI and
      for CMB alone (a band edge beyond 2σ of CMB alone is reported as tension, not a fail).
  R2 r: PASS if r_max < 0.034.
  R3 α_s: PASS if every band point has |pull| < 2 vs P-ACT-LB.
  Band verdict: PASS if R1–R3 all pass. Correlations between n_s and r ignored (assumed); stated.
No reruns to chase results; fixes only via PREREG_D1404_DEVIATIONS.md written first.
