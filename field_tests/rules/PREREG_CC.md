# CC: cosmic chronometers, an independent check of the expansion rate

**Status: LOCKED** on Danny's word ("schedule them all to set automatically in q", 12 Nov 2026, 14:17 CT, asking for every pending test to be queued to run). Draft text below unchanged except this line. Drafted, written 12 Nov 2026 at Danny's request ("Set this up", 13:33 CT). It becomes LOCKED only on
Danny's word; nothing under it is computed before the lock. AI-assisted. Cloud.

**Why.** DESI and SDSS both show the expansion running slightly fast near z ≈ 0.5–0.7 (D_H a few percent short), and
FLAG-1 predicts about +1.1% in H there. Cosmic chronometers measure H(z) directly from the ageing of passive galaxies:
no standard ruler and no supernova calibration. They are independent of every dataset in the FLAG-1 fits.

**Not blind, and the expected reach, stated now.** Known at writing: the 32-point compilation below and its errors.
No model prediction was computed. With diagonal errors, the 11 points at 0.4 ≤ z ≤ 0.8 combine to about ±4.7% on H,
looser with the systematic covariance. FLAG-1's +1.1% and the BAO surveys' roughly +3% are both inside 1σ of that, so
the expected outcome of both readings is no discrimination. The test is set up now as an independent cross-check, and
so that sharper chronometer data can be scored the same way later.

## Data
The standard 32-point compilation, 0.07 ≤ z ≤ 1.965 (Simon 2005; Stern 2010; Moresco 2012, 2015, 2016; Zhang 2014;
Ratsimbazafy 2017; Borghi 2022; Jimenez 2003), as tabulated in arXiv:2301.09591, Table 1 (Moresco points are the mean
of the BC03 and MaStro values). File: `field_tests/cc/cc_data.csv`. Errors are taken as independent (diagonal). The
Moresco et al. 2020 systematic covariance (gitlab.com/mmoresco/CCcovariance) is not reachable from this environment;
using it would widen the errors. That is a stated limitation, not a reason to change any reading.

## Models (no refit)
The stored Pantheon+ s8y6 fits: FLAG-1 (`cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6`) and its ΛCDM partner
(`cmp_ax_spa_lcdm_halofit_s8y6`); Dovekie and Union3 pairs reported. H(z) from the coupled build, as in MISSING-PIECE M2.
Neither fit used chronometer data, so this is a prediction test.

## Readings
- **CC-1 (decides): all 32 points.** Δ = χ²(FLAG-1) − χ²(ΛCDM), Pantheon+ pair.
  **FLAG-1 FAVOURED:** Δ ≤ −2. **ΛCDM FAVOURED:** Δ ≥ +2. **NO DISCRIMINATION:** otherwise.
- **CC-2 (reported, its own reading): the z ≈ 0.4–0.8 window.** The weighted mean of H_CC/H_ΛCDM − 1 over the 11 points
  with 0.4 ≤ z ≤ 0.8, with its error σ_w.
  **FAST, AS BAO SUGGESTS:** mean ≥ +2σ_w. **SLOW:** mean ≤ −2σ_w. **NOT RESOLVED:** otherwise. FLAG-1's own value
  of the same weighted mean is reported beside it.
- Also reported: each model's χ² and p-value for 32 points, and the precision a future chronometer set needs to tell
  FLAG-1 from ΛCDM at 2σ in the window.

## What may not happen
No change of the data list, errors, window, models or bands after any number is computed. Counted +2 in V7.

## Code
`field_tests/cc/cc_test.py` → `field_tests/results/cc.json`.
