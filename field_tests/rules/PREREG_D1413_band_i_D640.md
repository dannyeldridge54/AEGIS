# PREREG D1413 — band_i running re-scored with the D640 offset-corrected relation (D1412) instead of leading order (D1402a)

Locked 2026-11-19 (UTC) before computing (JANUS tick 11; ladder flag band_i: recheck after D1412).
Method: D640 inversion (script of D1412, unchanged: field_tests/scripts/d1412/tau_i_offset.py functions eqs/a640, c = ln1728/2π)
at the four band corners (n_s 0.970/0.975 × r 4.8e-4/5.7e-4) and a 21×21 grid; require residual < 1e-12 and 0 < x, report I*, x.
Score vs ACT DR6 P-ACT-LB 0.0062 ± 0.0052 (arXiv:2503.14454). Rule: PASS if all |pull| < 2 (as D1402).
Also report: shift vs D1402a's LO numbers, and whether any grid point needs ε = 4x/I*³ outside NA12's 1.30–1.50e-4 (informational).
Then clear the band_i flag citing this note. No reruns to chase results; fixes only via PREREG_D1413_DEVIATIONS.md.
