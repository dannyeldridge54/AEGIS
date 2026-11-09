# JOINT-SHEAR: fit with the full DES Y3 shear inside, judge with the full shear (DRAFT, not locked)

**Status: DRAFT** (9 Nov 2026, after Danny: "keep at it, let's get it together best we can"). AI-assisted. Lock only on
Danny's word. No joint-shear fit exists.

**Why, stated plainly.** Twice now (S8-L, S8-A) a model passed the compressed one-number S8 test and then missed the
full shear test (S8-A on DES Y3: +1.76 / +2.32 / +2.76, OVER, `PREREG_LATE_BASE.md`). The models are tuned without the
shear data and graded on it afterwards. This rule fits with the shear data inside, so each model fails or passes once.
**Not blind:** all the numbers above are known at writing; the KiDS S8-A result may be known at lock and will be stated.

## Model (fixed)
- **S8-A** exactly as `PREREG_S8A_ANGLE.md` (angle-coupled build, β_eff ∈ [0, 0.12], CMB + DESI DR2 + one SN set,
  same priors, starts, best of 4), and **ΛCDM** `ax_spa_lcdm_halofit{...}` with the same treatment (equal effort).
- **Added term: the full DES Y3 cosmic-shear likelihood** (as `PREREG_S8L_NONLINEAR.md`: axionHMcode basic + HMcode-2020
  damping, same flags and z grid, minimised over the shear nuisances), entering the fit through an emulator (below).
  The DES Y6 S8 term is **not** added (no double counting of shear).

## How the shear enters (steer with an emulator, judge with the full pipeline)
1. **Calibrate:** for each model, run the full shear pipeline (nuisance-profiled χ²_WL) at the stored best fit and 12
   design points spread in (S8, Ω_m) over ±3σ of the stored fit's posterior width (plus β_eff for S8-A). Fit a
   quadratic χ²_WL ≈ q(S8, Ω_m[, β_eff]).
2. **Gate G-JS (before any fit):** at 4 held-out points per model, |q − full| ≤ 0.5. If not, add 8 points and refit q
   once; if it still fails: NO FITS, NO VERDICT (logged).
3. **Fit (PC):** minimise χ²_CMB+BAO+SN + q, best of 4, as above. 6 fits (2 models × 3 SN sets).
4. **Judge with the full pipeline, not the emulator:** at each joint best fit, the full shear χ²_WL replaces q. If
   |q − full| > 1 at a best fit: NO VERDICT for that set (the emulator steered the fit somewhere it does not know).

## Verdicts (per SN set; 2 of 3 decides)
- Δ = [χ²_CMB+BAO+SN + χ²_WL(full)](S8-A) − [same](ΛCDM).
  **SURVIVES SHEAR** if Δ ≤ −4; **TIE** if none ≤ −4 and none ≥ +2; else **MIXED** (SF thresholds).
- **Reported, not verdicts:** the shear part alone (Δ_WL at the joint fits, against the +2 line of LATE-BASE); how much
  CMB/BAO/SN fit each model gives up to fit the shear; β_eff, S8, H0.
- KiDS-Legacy rerun at the joint best fits (locked KiDS rule, unchanged): reported as an independent check.

## What may not happen
No change of data, priors, design points or thresholds after any joint result; failures at full size; no rerun to chase
a pass. Counted +1 in V7. Does not change LATE-BASE: its base choice stands on its own rule.

## Cost (estimate)
Calibration: ~34 full shear runs (cloud, ~10–15 min each, resumable). Fits: 6 on the PC (same cost as the S8-A fits).
