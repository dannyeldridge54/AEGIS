# PREREG_D1663_G14_LIGHT_ELEMENTS — sourced light-element scorecard (Janus genesis G14; locked 2026-11-19 ~23:50Z before any number)
Sources [literature, read this tick]: Y_p = 0.2458 ± 0.0013 (LBT Y_p Project, arXiv:2601.22239); 10⁵ D/H = 2.527 ± 0.030 (Cooke+ 2018, arXiv:1710.11129); full-precision code PRIMAT: Y_p 0.24709 ± 0.00017, 10⁵ D/H 2.459 ± 0.036 (arXiv:1909.12046, Table I; its "observations" row lists Y_p 0.2449 ± 0.0040 and 10¹⁰ Li/H 1.58 ± 0.31).
Toolkit values (read-only, other chat): field_tests/results/GENESIS_MATTER/rd1.json "v5" (Y_p, D/H, Li after the Coulomb correction, D1651).
Compute: pulls of the toolkit vs observation (observational σ only), toolkit − PRIMAT (code offset), and PRIMAT vs observation (to show what a full code itself gets).
Also check the two unsourced numbers flagged in D1660/D1662: D1633's "observed 0.245 ± 0.003" against the sourced values; D1651's "full codes ≈ 0.247" against PRIMAT 0.24709.
Reading (locked): the toolkit is "textbook-grade" if |toolkit − PRIMAT| ≤ 0.003 in Y_p and ≤ 10 % in D/H; the flagged numbers are "confirmed" if within the quoted uncertainties of the sourced values. No new physics verdicts.
Script: field_tests/scripts/janus_g/g14_light_elements.py → field_tests/results/D1663_G14_light_elements.json
