# DRAFT pre-registration: S8-WL, the full weak-lensing test (Master Plan step 1.4)

**Status: DRAFT. Not locked, no hash.** Written 7 Nov 2026 with AI assistance. The author edits, then locks it (SHA-256 +
timestamp, `.sha256` beside it) **before any weak-lensing number for the Twist is computed**. Until then nothing runs.

## Why
The Twist ties ΛCDM instead of being preferred only because of S8: a single-number penalty of 2.87 against
DES Y3 + KiDS-1000 (limit 2) but 0.75 against KiDS-Legacy (`cmb-fit/PREREG_S8.md`). A single Gaussian in S8 ignores the
survey's real data vector, its nuisance parameters (baryons, intrinsic alignments, photo-z, shear bias) and the shape of
the Twist's matter power spectrum. Step 1.4 replaces it with the surveys' own cosmic-shear likelihoods.

## Models and points (fixed now)
- **ΛCDM** and the **Locked Twist** at their stored best fits on Planck 2018 + DESI DR2 + Pantheon+
  (`cmp_lcdmP.json`, `cmp_edelockP.json`, recomputed fair pair Δχ² = −4.70). No cosmological parameter is refitted.
- Matter power: CAMB with EarlyQuintessence (n = 3, the stored f_EDE, z_c, θ_i) for the Twist and plain CAMB for ΛCDM,
  non-linear HMCode2020 with baryon feedback, as both surveys use.

## Data (fixed now)
- **A: DES Y3 cosmic shear** (the CosmoSIS standard-library DES Y3 2pt shear likelihood, fiducial scale cuts).
- **B: KiDS-Legacy cosmic shear**, COSEBIs (fiducial), via the released CosmoPipe/CosmoSIS pipeline
  (github.com/AngusWright/CosmoPipe).

## Measure
For each survey s and model M: χ²_WL,s(M) = minimum over that survey's nuisance parameters only (baryon log T_AGN,
intrinsic alignment, photo-z shifts, shear calibration), with the survey's own priors, cosmology held at the stored point.
Δ_WL,s = χ²_WL,s(Twist) − χ²_WL,s(ΛCDM).

## Rule
- **Both Δ_WL ≤ +2:** the S8 objection is resolved by the full data; together with the stored supernova results the
  existing PREFERRED rule applies (all SN Δχ² < −2), and the verdict file is updated by that rule.
- **Δ_WL > +2 on one survey only:** survey-dependent; say exactly which, as `PREREG_S8.md` already requires.
- **Δ_WL > +2 on both:** weak lensing disfavours the Twist; the verdict stays TIE and this is reported as a failure.
- **Failures:** a pipeline that cannot run a model counts as NO VERDICT for that survey; any setting change is logged
  first.

## Choices for the author before locking
1. Keep "stored best fits, nuisance-only minimisation" (cheap, fair, no refit), or require a joint refit (stronger,
   far more compute).
2. Keep the limit +2 (same as the S8 penalty rule) or choose another, now.
