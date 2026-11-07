# S8-WL: weak lensing, newest survey and full likelihood (pre-registration)

**Locked:** 2026-11-07 at the time in `PREREG_S8_WL.md.sha256` (UTC), by Claude at Danny's request ("u do it and research
different options"). Replaces the unlocked `field_tests/S8_WL/DRAFT_PREREG_S8_WL.md`. AI-assisted.
**Not blind, stated plainly:** the stored best fits and the DES Y6 number below both exist at lock time. The rule fixes
only how they are combined. The Oct 29 verdict rule (`PREREGISTRATION_VERDICT.md`, surveys A and B) is unchanged;
this test is reported **beside** it and never swaps its survey.

## Options considered (7 Nov)
1. S8 penalty vs the newest survey, DES Y6 cosmic shear (no fitting). **Chosen, Part 1.**
2. Full DES Y3 cosmic-shear likelihood (public, CosmoSIS) at stored best fits. **Chosen, Part 2 (PC).**
3. Full KiDS-Legacy likelihood: not public when last checked; KiDS-Legacy agrees with the CMB, so it is the weaker test.
4. Joint refit with weak lensing inside the fit: days of compute; deferred.

## Part 1: DES Y6 S8 penalty (now)
- Data: DES Y6 cosmic shear, NLA fiducial, S8 = 0.798 +0.014 / −0.015 (arXiv:2602.10065).
- Model S8 = σ8 √(Ωm/0.3) from each stored best fit. Penalty P = ((S8_M − 0.798)/σ)² − ((S8_ΛCDM − 0.798)/σ)², σ from
  the side the model falls on (+0.014 above, 0.015 below), ΛCDM on the same data.
- Pairs: Locked Twist `cmp_edelockP` vs `cmp_lcdmP`; Spiral `cmp_ax_spa_spiraltwist[_dovekie|_union3]_nlfix` vs
  `cmp_ax_spa_lcdm_halofit[_dovekie|_union3]`.
- Reading per pair: **PASSES** if P ≤ 2 (same limit as PREREG_S8); **OVER** if P > 2.

## Part 2: full DES Y3 cosmic shear (PC, CosmoSIS standard library, fiducial scale cuts)
- At the same stored best fits, minimise over the survey's nuisance parameters only (baryons, intrinsic alignment,
  photo-z shifts, shear calibration), cosmology held fixed. Δ_WL = χ²_WL(model) − χ²_WL(ΛCDM).
- **PASSES** if Δ_WL ≤ +2; **OVER** if > +2. Setup: `field_tests/S8_WL/SETUP.md`. A pipeline that cannot run a model is
  NO VERDICT; settings changes are logged first.
