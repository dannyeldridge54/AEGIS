# PREREG D1407 — audited SERAPIS-E box (band_e_audited) n_s scored on end-2025 CMB and CMB + DESI

Locked 2026-11-19 (UTC) before computing (JANUS tick 6, node band_e_audited; D1399 scored its running, this scores its n_s and r).
Box: n_s 0.9717–0.9760, r 4.39–4.90e-4 (D1245). Data on file (arXiv:2512.10613, fetched 2026-11-19): n_s 0.9682 ± 0.0032 (CMB),
0.9728 ± 0.0029 (CMB + DESI), r < 0.034 (95%).
  R1 (primary, CMB + DESI): PASS if the whole box has |pull| < 2; PARTIAL if only part does (report the fraction); FAIL if none.
  R2 (CMB alone): same three outcomes, reported alongside (the BAO-dependence seen in D1402/D1404).
  R3 r: PASS if r_max < 0.034.
Postulate verdict = R1 and R3 (the AEGIS bands are scored on CMB + DESI); R2 reported. 1001-point n_s grid.
No reruns to chase results; fixes only via PREREG_D1407_DEVIATIONS.md written first.
