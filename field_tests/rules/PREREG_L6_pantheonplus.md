# PREREG L6 — Janus-LT reproduces the Pantheon+ SN-only flat-ΛCDM Ω_m
Locked 2026-11-17 before any L6 number. Data: PantheonPlusSH0ES/DataRelease (GitHub, main), 4_DISTANCES_AND_COVAR:
1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8  data/sn/Pantheon+SH0ES.dat
abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc  data/sn/Pantheon+SH0ES_STAT+SYS.cov
(cov not committed — 33 MB, gitignored; hashes above pin it.)
Target [literature, fetched abstract of arXiv 2202.04077]: flat ΛCDM, SNe Ia alone, Ω_M = 0.334 ± 0.018.
Method: residual r_i = m_b_corr_i − 5 log10[(1+zHEL_i) D_M(zHD_i)/10 pc]; full STAT+SYS covariance on the selected rows; M
marginalised analytically (χ² = a − b²/e + ln(e/2π), a = rᵀC⁻¹r, b = 1ᵀC⁻¹r, e = 1ᵀC⁻¹1). D_M from janus_lt Cosmo (h = 0.7 — degenerate
with M; ω_b = 0.0224; ω_c = Ω_m h² − ω_b; mν = 0; radiation included — a ≤ 1e-4 effect on Ω_m), tabulated on a fine z grid.
Ω_m scanned 0.20–0.45, step 0.0005; best fit and ±1σ from Δχ² = 1.
Selections (the paper's text does not state the SN-only cut; both are reported): (a) zHD > 0.01 [my choice — common Hubble-flow cut],
(b) all 1701 rows. Claim: (a) best-fit Ω_m within 0.5σ (0.009) of 0.334 → REPRODUCED; else NOT REPRODUCED. (b) reported only.
Results: field_tests/results/janus_lt_l6_pantheon.txt.
