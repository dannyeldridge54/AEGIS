# Flagship: the Spiral with κ = 1, refit with lensing inside (FLAG-1)

**Locked:** 9 Nov 2026, time in `PREREG_FLAGSHIP.md.sha256` (UTC), on Danny's word ("Start them", 01:33 CT, after the
plan: one flagship model, freeze it, let new data judge). AI-assisted. No flagship fit exists at lock.

**Not blind, stated plainly.** Known at lock: S8-J (free κ) beats ΛCDM+S8 by 7.32 / 8.14 / 8.23; SIMPLIFY-L picked
κ = 1 (margin 5.60, without the S8 term). This rule fixes how the flagship is fitted and read; it does not hide that the
choice of flagship was made after those results.

## Model (fixed)
The S8-J fit exactly (`PREREG_S8_JOINT.md`: SF engine, coupled B0-fixed AxiCLASS, halofit, CMB + DESI DR2 + one SN set,
DES Y6 S8 term, best of 4, same priors and starting points), with **κ fixed at 1** (SIMPLIFY-L's K2). Free: β_eff and
the standard parameters. Runs: `ax_spa_spiraltwist_kappa1{,_dovekie,_union3}_nlfix_s8y6` (3 fits, PC),
code `field_tests/S8_WL/joint/flagship_fit.py` (calls the S8-J wrapper unchanged).

## Gate
None new: the S8-J gate (G-J, passed 8 Nov) and the SIMPLIFY-L κ = 1 fits cover the engine.

## Readings (per SN set; 2 of 3 decides)
- **vs ΛCDM+S8** (stored `ax_spa_lcdm_halofit{...}_s8y6`, lower of the two restart files): Δ ≤ −4 **SURVIVES**;
  none ≤ −4 and none ≥ +2 **TIE**; else **MIXED**.
- **vs S8-J (free κ):** score χ² − 2 for the flagship; **FLAGSHIP KEPT** if the summed score is ≤ the S8-J sum, else
  **κ = 1 COSTS FIT** (reported; the flagship is still the one carried forward unless it loses to ΛCDM).
- Reported, not verdicts: β_eff, S8, H0, w0/wa; then (separate step, cloud) the locked KiDS-Legacy and DES Y3 shear
  rules rerun at the flagship best fits, and frozen DESI DR3 / Euclid predictions written before those data appear.

## What may not happen
No change of priors, data or κ after seeing results; a failed fit is NO VERDICT for that set; failures at full size.
Counted as +1 in the V7 look-elsewhere inventory.
