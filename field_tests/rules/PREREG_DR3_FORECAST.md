# PREREG_DR3_FORECAST — where DESI DR3 can separate the Weave thread from CPL and from ΛsCDM (locked D1707, 2026-11-20 01:42 UTC)
Using the BAO + SN + CMB best fits of D1694/D1695 (thread, CPL, ΛsCDM, ΛCDM), compute D_M/r_d and D_H/r_d at the DESI DR2 redshifts (0.51, 0.706, 0.934, 1.321, 1.484, 2.33), plus D_V/r_d at 0.295.
Report each model's percent difference from ΛCDM at each point, and the thread − CPL and thread − ΛsCDM differences, compared with the DR2 1σ error at that point (from the DR2 covariance diagonal). A difference above ~1.5 × the DR2 σ marks a bin where DR3 (≈ √2 smaller errors, assumed) can discriminate at ~2σ.
Output: a falsification table (prediction, not a fit). Script: field_tests/scripts/realdata/dr3.py
