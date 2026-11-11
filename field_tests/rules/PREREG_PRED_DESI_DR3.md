# Flagship predictions for DESI DR3 (and later BAO / growth data), frozen before release

**Status: LOCKED** on Danny's word ("do that", 10 Nov 2026, 19:43 CT, replying to "Next up: locking the flagship's
predictions for DESI DR3 and Euclid"). AI-assisted. DESI DR3 cosmology results are not public at lock. The Euclid
numbers are already frozen under `PREREG_PRED_EUCLID.md` and `PREREG_LENSING_FORECASTS.md`; this rule adds DESI.

## What is frozen (no refit, ever, under this rule)
The FLAG-1 best fits and the predictions computed from them, identified by SHA-256 (first 16 hex digits):

| File | sha256 |
|---|---|
| `cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6.json` (Pantheon+ fit, **primary**) | af165b5739c2bdf2 |
| `cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6.json` | 761df7af358eda8a |
| `cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6.json` | e7c22a4ec55c3221 |
| `theory/fpc_ax_spa_spiraltwist_kappa1_nlfix_s8y6.json` (BAO D_M/r_d, D_H/r_d, D_V/r_d; fσ8; σ8; S8) | 80775f37c4ae1979 |
| `theory/fpc_ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6.json` | 5e1e5db3a53898db |
| `theory/fpc_ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6.json` | f9637cd6713f2958 |
| `field_tests/desi_mock/desi_mock_part_SN.json` (DESI-style w0wa reading of the primary fit) | 659282571edec058 |

Predictions at redshifts not in the fpc files are computed from the frozen best-fit point with the same build
(`AxiCLASS_coupled_nlfix`) and the same translation as `field_tests/desi_mock/desi_mock.py truth`. That step is a
calculation, not a fit.

Key numbers (primary fit):
- r_d = 147.45 Mpc; H0 = 67.16 (reported; true H(0) 0.108% lower); σ8 = 0.807; S8 = 0.825.
- fσ8 at z = 0, 0.3, 0.5, 0.7, 1.0, 1.5: 0.419, 0.457, 0.459, 0.450, 0.425, 0.373.
- DESI-style reading (uncoupled-CDM w0waCDM fit to the flagship, DR2 errors): **w0 = −0.833, wa = −0.451**.

## Scoring (when DESI DR3 publishes; each line scored once and reported whatever the outcome)
- **P1, dark-energy reading.** DESI DR3 BAO + CMB + Pantheon+ in w0waCDM (DESI's own published numbers). CONSISTENT
  if both central values are within 2σ of (−0.833, −0.451), using DESI's quoted 1σ, one parameter at a time; FAIL if
  either is beyond 3σ; otherwise TENSION.
- **P2, the signal persists.** The Twist says the evolving-dark-energy preference with Pantheon+ comes from the
  coupling and does not go away. FAIL if DESI DR3 + CMB + Pantheon+ prefers w0wa over ΛCDM at less than 1σ;
  otherwise CONSISTENT.
- **P3, BAO distances.** χ² of the DR3 BAO points (DESI's covariance) against the frozen primary-fit predictions, with
  no free parameter. CONSISTENT if p ≥ 0.01; FAIL if p < 0.001; otherwise TENSION. The same χ² for DESI's own
  best-fit ΛCDM is reported beside it, for scale.
- **P4, growth.** χ² of DESI full-shape fσ8 (DR1 or DR3, whichever is the latest published) against the frozen fσ8,
  with DESI's covariance. Same p-value bands as P3.
- The Dovekie and Union3 fits are scored too and reported; the primary fit decides.

## What may not happen
No refit, no reinterpretation of which fit is primary, and no change of bands after DESI DR3 is public. If DESI changes
its data format, the conversion is written down before the χ² is computed. Counted +1 in V7.
