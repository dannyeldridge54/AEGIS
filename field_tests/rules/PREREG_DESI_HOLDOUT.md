# DESI-HOLDOUT: does FLAG-1, fitted without DESI, predict DESI?

**Status: LOCKED** under Danny's advance authorisation ("I authorize it now just do it if im asleep", 11 Nov 2026,
21:09 CT, replying to the plan "the cleaner DESI test … stays a draft until you say 'lock'"; he authorised the lock in
advance). Written, self-reviewed and locked by Claude on 12 Nov 2026 before any holdout fit existed. AI-assisted.

**Why.** FLAG-1 was fitted with DESI DR2 BAO included, so DESI-MOCK (FLAG-1 reproduces DESI's evolving-dark-energy
signal) is a consistency check, not a prediction. Here DESI is held out of the fit, and FLAG-1 must predict it.

**Not blind.** Known at writing:
- In the stored fits (DESI included), DESI BAO χ²: FLAG-1 8.646, ΛCDM+S8 12.733 (difference −4.09).
- V2 (no SNe, DESI included): BAO difference −3.03.
- An earlier no-BAO fit of the general spiral twist (`cmp_ax_spa_spiraltwist_nobao_nlfix`, no S8 term, not κ = 1)
  gave β 0.045 and Δχ² −0.97 against `cmp_ax_spa_lcdm_halofit_nobao`. Its DESI χ² was never computed.
- DESI-MOCK and DESI-MOCK-CMB: REPRODUCES DESI'S SIGNAL (2.9σ) with the DESI-included truth.

## Holdout fits
Exactly the stored s8y6 fits (same build, CMB suite, Pantheon+, DES Y6 S8 term, priors and parameters), with every
`bao.` likelihood removed:
- **FLAG-1:** `ax_spa_spiraltwist_kappa1_nlfix` → `ax_spa_spiraltwist_kappa1_nlfix_nodesi_s8y6` (κ = 1, β free).
- **ΛCDM+S8:** `ax_spa_lcdm_halofit` → `ax_spa_lcdm_halofit_nodesi_s8y6`.
- Cobaya minimize, best of 4, each started from its own stored Pantheon+ s8y6 minimum (as V2).
- If a holdout fit fails, or β ends at a prior edge, that is reported, and the reading is NO VERDICT.

## Test A: prediction (decides)
Each holdout best fit predicts the DESI DR2 BAO data (`bao.desi_dr2.desi_bao_all`, ALL covariance), with no refit:
the DESI likelihood is evaluated, through Cobaya, at the holdout minimum. ΔA = χ²_DESI(FLAG-1) − χ²_DESI(ΛCDM).
**Gate:** the same evaluation at the stored DESI-included minima must reproduce their stored DESI χ² (8.646 and
12.733) to within 0.01. If it does not, Test A is NO VERDICT.
- **FLAG-1 PREDICTS DESI BETTER:** ΔA ≤ −4.
- **LEANS FLAG-1:** −4 < ΔA ≤ −1.
- **NO DIFFERENCE:** −1 < ΔA < +1.
- **LEANS ΛCDM:** +1 ≤ ΔA < +4.
- **ΛCDM PREDICTS DESI BETTER:** ΔA ≥ +4.

## Test B: DESI-style mock from the holdout (reported, its own reading)
The DESI-MOCK procedure (`PREREG_DESI_MOCK.md`, compressed CMB, cloud), unchanged except that the truth is the holdout
FLAG-1 minimum instead of the DESI-included one. Same mock, covariances, fits, starts and readings (REPRODUCES DESI'S
SIGNAL / PARTIAL / DOES NOT). Compressed CMB is used because DESI-MOCK-CMB agreed with it to within 0.03σ.

## Also reported
Holdout β, H0, S8 and Δχ²_total for both models; the shift of β from the DESI-included fit; the DESI-included ΔA
(−4.09) next to the holdout ΔA.

## What may not happen
No change of fits, likelihoods, priors, starts, data or thresholds after any result. No rerun to chase a reading.
No second truth to chase Test B (Dovekie or Union3 holdouts may be run afterwards as clearly marked extras only).
Counted +2 in V7 (Test A and Test B).

## Code
`field_tests/desi_holdout/desi_holdout.py` (modes fit FLAG1 | LCDM, predict, truth, mock, score). The fits run where
they fit (the PC queue when it is free, else the cloud); the venue does not change the method.
