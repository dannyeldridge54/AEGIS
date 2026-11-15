# PREREG D571: four catalogue discovery hunts (locked before any download or computation)

Date: 2026-11-15. Scope: AEGIS Cosmos Atlas. These hunts are catalogue cross-matches. They are not Twist/SERAPIS tests and make no cosmology claim.
Honest-label rule: an object that is "not in catalogue X" is a **follow-up candidate**. It is not a discovery unless a dedicated literature/SIMBAD search, run afterwards and per object, also finds nothing.

## H1: Gaia DR3 quasar candidates lacking a spectrum
- Source: gaiadr3.qso_candidates joined to gaiadr3.gaia_source (AIP TAP mirror; fallback GAVO Heidelberg).
- Selection: classlabel_dsc_joint = 'quasar' (the high-purity DSC-joint label). Keep G, ra, dec, redshift_qsoc and flags_qsoc.
- Comparison catalogues: SDSS DR17 QSOs (already on the PC, about 753k) and Milliquas v8 (VizieR VII/294, CfA mirror). In Milliquas, types containing Q, A, B, K or N count as spectroscopically classified.
- Match radius: 2.0 arcsec.
- Output: the candidates with no spectroscopic match, ranked by G (brightest first). Reported counts: N_total, N_matched to SDSS, N_matched to Milliquas-spectroscopic, N_unmatched; also N_unmatched with G < 19 and with G < 18.
- Caveat stated up front: DESI DR1 and LAMOST are not checked, so the unmatched list overcounts.

## H2: Origins of the vetted fast stars
- Input: stars.json, vetting == 'solid' (190 stars). Fetch ra, dec, parallax, pmra, pmdec, their errors and radial_velocity from Gaia DR3 (AIP or GAVO). Distance = d_pc already in stars.json.
- Model: galpy MWPotential2014 with the circular velocity scaled to 236 km/s at R0 = 8.122 kpc, z_sun = 20.8 pc, solar motion (11.1, 12.24, 7.25) km/s. Integrate backwards 300 Myr (leapfrog/dop853, 3001 steps).
- Stars with a Gaia RV: one orbit at the nominal values plus 200 Monte Carlo draws (Gaussian errors; distance error ±20%, because only d_pc is stored). Record the minimum distance to the Galactic Centre (r_min,GC), the fraction of draws with r_min,GC < 1 kpc, and the fraction with v_GC > v_esc(r) (galpy vesc).
- Stars without RV: scan RV from −800 to +800 km/s in 10 km/s steps. Report RV* (the RV that minimises r_min,GC), that minimum value, and the RV range over which r_min,GC < 1 kpc. A star counts as a "GC-origin candidate" only if r_min,GC(RV*) < 1 kpc AND |RV*| ≤ 800. This is a **prediction**: a spectrum measuring RV inside that range supports GC origin; one outside it rejects it.
- Disk-origin flag: the backward orbit crosses z = 0 at R between 3 and 25 kpc within 100 Myr, with an implied ejection speed relative to local circular rotation > 300 km/s (runaway / hyper-runaway).
- Ejection speeds use the potential's v_esc. No rerun to change the potential; any fix goes in PREREG_D571_DEVIATIONS.md, written first.

## H3: TESS planet candidates observable by amateurs
- Source: NASA Exoplanet Archive TAP, table toi (all columns as CSV).
- Selection: tfopwg_disp in ('PC','APC'); st_tmag ≤ 12.0; transit depth ≥ 3000 ppm (≥ 3 mmag, reachable by a small telescope); pl_orbper available; pl_tranmid available.
- Ephemeris: the next transits from 2026-11-15 to 2026-12-15 UTC. Timing 1σ = sqrt(σ_T0² + (n·σ_P)²); flag a transit "stale" if 1σ > 1 h.
- Ranking: depth / (1 + timing σ in hours), restricted to non-stale transits.
- Atlas: add a transit table to the Tonight view; the browser computes altitude at the observer's location.

## H4: Bright Gaia variables missing from VSX
- Source: gaiadr3.vari_classifier_result joined to gaia_source; phot_g_mean_mag < 11.0; best_class_score ≥ 0.7. Keep ra, dec, pmra, pmdec, G, best_class_name and best_class_score.
- Comparison: VSX (VizieR B/vsx/vsx, max < 13, CfA mirror). Gaia positions are moved to J2000 using the proper motion.
- Match radius: 10 arcsec (VSX positions are heterogeneous).
- Output: unmatched objects per class, ranked by score. Reported counts: N_total, N_matched and N_unmatched per class.
- Caveat: VSX may hold the star under a coarser position, or under its ASAS-SN or ZTF name; unmatched objects are candidates only.

## Integrity
- Every count is computed in code. Nothing is tuned after seeing the results. A per-object novelty search is run only for the top 5 of each hunt before any "new" wording is used.
