# Lensing forecasts, addendum: the flagship (FLAG-1)

**Status: LOCKED** on Danny's word ("Lock, then post", 11 Nov 2026, 04:23 CT, answering "Lock it before I post to Zenodo?"); time and fingerprint in the .sha256 file. AI-assisted. This adds FLAG-1 to `PREREG_LENSING_FORECASTS.md` (locked
8 Nov), which named only the pre-flagship models (Spiral, S8-J, S8-L) because FLAG-1 did not exist yet. Tests A and B,
the readings and the "what may not happen" lines are those of the parent rule, unchanged. Nothing here changes the
parent rule or its scores for the older models.

## Frozen numbers (no refit, ever, under this rule)
The stored FLAG-1 fits and their ΛCDM partners. The partners are the same runs the DES Y3 full-shear test used
(`field_tests/S8_WL/results/part2_desy3.json`). S8 = σ8 (Ω_m/0.3)^0.5 from each fit's own `minimum`.

| SN set | FLAG-1 fit (sha256, 16 hex) | S8 | ΛCDM partner (sha256, 16 hex) | S8 |
|---|---|---|---|---|
| Pantheon+ (primary) | `cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6` af165b5739c2bdf2 | 0.8251 | `cmp_ax_spa_lcdm_halofit_s8y6` 808f54eb49c9b1f3 | 0.8142 |
| DES-Dovekie | `cmp_ax_spa_spiraltwist_kappa1_dovekie_nlfix_s8y6` 761df7af358eda8a | 0.8282 | `cmp_ax_spa_lcdm_halofit_dovekie_s8y6_more` 50f67409e9138271 | 0.8157 |
| Union3 | `cmp_ax_spa_spiraltwist_kappa1_union3_nlfix_s8y6` e7c22a4ec55c3221 | 0.8249 | `cmp_ax_spa_lcdm_halofit_union3_s8y6_more` 7f343e5ba5d5b39b | 0.8137 |

FLAG-1's S8 is about 0.011–0.013 above its ΛCDM partner's. These fits carry the DES Y6 S8 summary term (`s8y6`), so
DES Y6 Test A is not a forecast for them and is not scored under this addendum.

## Data to be scored
As the parent rule: Euclid DR1 cosmic shear, Rubin/LSST Y1, and the DES Y6 full cosmic-shear likelihood (Test B
only). Each is scored once and reported whatever the outcome. If a data product was already public at this lock, its
score is labelled **"test on existing data, not a forecast"**. That applies to DES Y6 if its 2pt products were
released between 8 Nov and this lock. KiDS-Legacy stays under its own rule (`PREREG_KIDS_LEGACY_SHEAR.md`).

## Method
- **Test B nonlinear power:** the survey's baseline model for both sides. For FLAG-1 this goes through the same coupled
  build and translation as the DES Y3 and KiDS-Legacy FLAG-1 rows. Nuisance parameters are minimised with equal
  effort on both sides.
- **Code gate:** as the parent rule.
- **Overall reading for FLAG-1:** LENSING OK / LENSING PROBLEM CONFIRMED / neither, with the parent rule's definitions.
  The Pantheon+ fit is primary; all three are scored and reported.

## What may not happen
No refit of FLAG-1 or its partners, no change of partner, no change of survey list after any of these results is
public. Counted +1 in V7.
