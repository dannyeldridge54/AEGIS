# PREREG L8b — non-degenerate: Planck 2018 distance priors (CHW, as L8) + DESI DR2 BAO (as L3/L4), flat ΛCDM
Locked 2026-11-17 before any L8b number. Fixes L8's flaw (D1047): 3 params (h, ω_b, ω_c) vs 3 + 13 data. z* = Hu–Sugiyama with
g₁ = 0.0783 (the authors' code, as L8's claim option). BAO: tools/janus_lt/desi.chi2 with r_d from Janus-LT's own z_d (Recomb, as L4).
Claims: (C1) χ²_min/(16 − 3) ≤ 2 (fit acceptable); (C2) robustness of the CMB compression used in D1042: fitted h within 0.005 of
L4's ΛCDM h = 0.6842 (BAO + DESI-compressed CMB). Both pass → ROBUST, else report which failed.
Results: field_tests/results/janus_lt_l8b.txt.
