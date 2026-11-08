# Lensing forecasts for the coming surveys (DRAFT, not locked)

**Status: DRAFT** (8 Nov 2026, Danny: "For lensing, let's try to get it right"). To be locked before any of the
named results are public. Purpose: the fair test of the lensing question is new data scored against numbers frozen in
advance, not more runs on DES Y3.

## Frozen numbers (from `theory/PREDICTIONS_FROZEN_8NOV.md`, no change)
S8 at the stored best fits (Pantheon+ / DES-Dovekie / Union3):
- ΛCDM 0.8175 / 0.8162 / 0.8168
- Spiral 0.8326 / 0.8338 / 0.8395
- S8-J 0.8221 / 0.8260 / 0.8269
- S8-L 0.8170 / 0.8168 / 0.8190 (S8-LNL D2 check, 8 Nov: with the ultralight field included the total-matter S8 is
  0.8170 / 0.8168 / 0.8190, i.e. the same to 4 decimals; `theory/s8l_total_matter_S8.json`)

## Data to be scored (only results not yet public at the lock; each scored separately)
1. DES Y6 full cosmic-shear likelihood (its S8 summary is already public and already used; the 2pt data products were
   not public on 8 Nov), 2. Euclid DR1 cosmic shear (mid-2027), 3. Rubin/LSST Y1.
KiDS-Legacy is already public (data vectors, covariance, n(z), CosmoSIS files): it is a test on existing data, with its
own rule (`DRAFT_KIDS_LEGACY_SHEAR.md`), not a forecast.

## Test A (summary S8; runs as soon as each survey quotes S8)
penalty = ((S8_model − S8_obs)/σ)² with the survey's own asymmetric errors; ΔP = penalty(model) − penalty(ΛCDM).
**PASSES** if ΔP ≤ +2 on at least 2 of 3 SN sets, else **OVER**. (Same form as S8-WL Part 1.)

## Test B (full shear likelihood; runs when the likelihood is public)
As S8-WL Part 2: Δ_WL = χ²_WL(model) − χ²_WL(ΛCDM) at the stored best fits, survey nuisance parameters minimised with
equal effort (same number of tries both sides). **PASSES** if Δ_WL ≤ +2 on at least 2 of 3 SN sets.
- Nonlinear power: the survey's own baseline model as stated in its paper, the same for both sides. For S8-L (an
  ultralight field) axionHMcode `basic` with the BAO-damping patch, as in S8-LNL, also for its ΛCDM partner.
- Code gate: reproduce the survey's published ΛCDM best-fit χ² (or its S8) within the tolerance stated at the lock.

## Readings
Per model and survey: PASSES / OVER for A and B. Overall per model: **LENSING OK** if B passes on at least one new
survey and no new survey gives OVER on B; **LENSING PROBLEM CONFIRMED** if B is OVER on two or more new surveys.

## What may not happen
No refit, no change of frozen numbers, no choice of survey after seeing results; failures reported at full size.
