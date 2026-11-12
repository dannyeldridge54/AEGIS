# MISSING-PIECE: where FLAG-1's preference lives, and a direct fifth-force test

**Status: LOCKED** on Danny's word ("Set that up in the cloud and start running it", 12 Nov 2026, 12:53 CT, replying
to the proposal of tests 4, 1 and 5 with locked rules). Written, self-reviewed and locked by Claude before any of
these numbers was computed. AI-assisted. Cloud.

**Why.** DATA-GEN (DOES NOT HOLD) found that FLAG-1 is preferred only with DESI-era data: SDSS-era data disfavour it.
That is either physics that only DESI is precise enough to see, or something specific to DESI-era data. M1 and M3 ask
which. M2 tests the dark-matter fifth force itself.

**Not blind.** Known at writing: V1's real-data anchor (compressed likelihood) Δ = −5.32; DATA-GEN deltas (G1 +2.76,
G2 +6.46, G3 −2.47, G4 −4.71); DESI DR2's LRG bin at z = 0.51 is widely noted as pulling away from ΛCDM; ACT DR6 ×
BOSS E_G values (below) and their stated ΛCDM predictions.

## M1: DESI bin jackknife (decides "one bin or spread")
- Likelihood and fits: exactly V1's real-data anchor (`v1_mockcal.py`: DESI DR2 BAO ALL covariance, Pantheon+ with
  analytic M, compressed CMB vector, background-only; FLAG-1 with β ∈ [0, 0.12], κ = 1, and ΛCDM; Nelder–Mead, the
  same 3 starts).
- Jackknife: drop one DESI redshift bin at a time (7 bins: z = 0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33; both
  DM and DH of a bin go together), keeping the covariance of the rest. Also reported: all DESI dropped.
- **Gate:** the full-data Δ reproduces V1's −5.32 to within 0.05.
- Readings, with Δ_(−i) = Δ after dropping bin i:
  - **ONE BIN CARRIES IT:** some single Δ_(−i) > −2.
  - **SPREAD:** every Δ_(−i) ≤ −4.
  - **PARTLY CONCENTRATED:** otherwise.
- Reported: each bin's share s_i = Δ_(−i) − Δ_full (positive = that bin supports FLAG-1) and β after each drop.

## M2: E_G, lensing versus galaxy motion (a direct fifth-force test)
- Data: ACT DR6 lensing × SDSS BOSS (Wenzl et al. 2024, arXiv:2405.12795), ACT-only rows: CMASS z = 0.555,
  E_G = 0.31 (+0.06/−0.05); LOWZ z = 0.316, E_G = 0.49 (+0.14/−0.11). Their systematic errors (3% and 4% of the
  value) are added in quadrature. The upper error is used when the model lies above the data, the lower error when
  below. The two points are treated as independent.
- Model: E_G(z) = Ω_m,eff(z)/f(z), with Ω_m,eff(z) = (ρ_b + ρ_cdm)(z)·a³/ρ_crit,0 (equal to Ω_m,0 for ΛCDM; it varies
  for coupled CDM), and f = d ln D/d ln a from the linear cb power at k = 0.02 Mpc⁻¹ (finite difference, Δz = ±0.01).
  Lensing obeys the ordinary Poisson equation in this model, and galaxies are taken to move with the dark matter
  (stated simplification).
- Models: the stored s8y6 best fits (Pantheon+ primary; Dovekie and Union3 reported), FLAG-1 and ΛCDM.
- **Gate:** for ΛCDM, f from the power spectrum agrees with CLASS's own f to within 1%.
- Readings, ΔEG = χ²_EG(FLAG-1) − χ²_EG(ΛCDM) on Pantheon+:
  - **FLAG-1 FAVOURED:** ΔEG ≤ −1. **ΛCDM FAVOURED:** ΔEG ≥ +1. **NO DISCRIMINATION:** otherwise.
- Reported: the fractional E_G difference FLAG-1/ΛCDM − 1 at each z, and the E_G precision needed to see it at 2σ
  (the measurement that would settle it).

## M3: the residual map (what the data want, DESI and SDSS side by side)
- Reference: the DESI-HOLDOUT ΛCDM fit (no BAO at all). Waits for that fit.
- For every BAO point, fractional residual (data − reference)/reference with its error: DESI DR2 (13 points) and SDSS
  (DR12 consensus z = 0.38, 0.51, 0.61, rs_fid 147.78 Mpc; DR16 LRG z = 0.698; DR16 QSO z = 1.48; all with their
  own covariances). The holdout FLAG-1 prediction is overlaid as a curve.
- Readings, comparing the surveys where both measured: DESI vs SDSS at z ≈ 0.51 (DM, DH), 0.70 (DM, DH) and 1.48
  (DM, DH), six differences of fractional residuals, each survey's covariance kept, the surveys treated as independent:
  - **SURVEYS AGREE:** p ≥ 0.05. **TENSION:** 0.01 ≤ p < 0.05. **SURVEYS DISAGREE:** p < 0.01.
  - Caveat, stated now: CMASS and DESI LRGs partly share sky and volume, so independence overstates p's precision.
- Also reported: χ² of the holdout FLAG-1 and ΛCDM predictions on SDSS, next to DESI-HOLDOUT Test A on DESI.
- **Gate:** this code's DESI χ² for the holdout ΛCDM matches Test A's Cobaya value to within 0.1.

## What may not happen
No change of data, bins, errors, starts, thresholds or reference after any result. No dropping of a part. Each part is
reported once. Deviations are logged before any rerun. Counted +3 in V7.

## Code
`field_tests/missing_piece/m1_jackknife.py`, `m2_eg.py`, `m3_map.py` (cloud). Results: `field_tests/results/missing_piece_m{1,2,3}.json`.
