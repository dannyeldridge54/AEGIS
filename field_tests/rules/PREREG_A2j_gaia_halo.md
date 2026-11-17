# PREREG A2j — 1 TeV wino vs H.E.S.S. IGS for the Gaia DR3 v_esc halo (Djl D) — locked 2026-11-17
Halo (quoted, arXiv:2402.00108 abstract): NFW with M200c = 0.55e12 M_⊙ and c200c = 13.9 (central values; ±0.15e12 and +6.2/−4.3 reported).
ρ_crit from astropy (H0 = 67.66); r200 = (3M/(4π·200ρ_c))^{1/3}; r_s = r200/c. ρ(R0) is evaluated at R0 = 8.178 kpc (the IGS convention; labelled assumption on the paper's R0).
J in the IGS annuli (0.5°–3.0°, D1126 method) vs the IGS benchmark. Line σv at 1 TeV with the NLL band (D1124), LO and NLO, limit 2.3e-28.
Also reported: the ±1σ M200 variants (0.40e12, 0.70e12) at fixed c, and c = 9.6 and 20.1 at fixed M.
Verdict vs f = 0.26: PASS, FAIL, or BAND-DEPENDENT, for the central halo; the variants are reported.
Script theory/wiring/a2j_gaia_halo.py (written after this lock).
