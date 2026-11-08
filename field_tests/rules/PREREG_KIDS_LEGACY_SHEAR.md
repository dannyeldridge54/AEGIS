# Lensing on KiDS-Legacy cosmic shear (Part 3)

**Status: LOCKED** on Danny's word (8 Nov 2026: "Get them all ready and set and scheduled ... Just let's try to fix the lensing. Do what you need to"). Fingerprint and UTC time in the .sha256 file. An independent full-shear test on public data we have not yet looked at: KiDS-Legacy
(Wright et al. 2025, A&A 703, A158), released with data vectors, covariance, n(z) and CosmoSIS configuration files
(kids.strw.leidenuniv.nl/sciencedata.php). Different telescope, sky, shape method and photo-z than DES Y3.

## Question
At the stored best fits (no refit), does each model's lensing cost against ΛCDM stay within +2 on KiDS-Legacy?

## Method (fixed when locked)
- KiDS-Legacy baseline likelihood exactly as in their CosmoSIS files (their statistic, scale cuts, n(z), covariance,
  priors on their nuisance parameters, including intrinsic alignments and baryon feedback).
- Cosmology fixed at the stored best fits; only KiDS nuisance parameters are minimised, equal effort both sides (the
  same number of tries and starting points as run_part2.py).
- Pairs (Pantheon+ / DES-Dovekie / Union3): Spiral vs ΛCDM, S8-J vs its ΛCDM+S8 partner, S8-L vs ΛCDM.
- Nonlinear power: KiDS-Legacy's own baseline for ΛCDM, Spiral, S8-J. For the S8-L pair both sides use axionHMcode
  `basic` + BAO-damping patch (as S8-LNL); if KiDS's baryon-feedback model cannot be applied on top, that limitation
  is stated and the S8-L pair is read with it.
- Δ_KiDS = χ²_KiDS(model) − χ²_KiDS(ΛCDM partner).

## Code gate (before any model pair)
Reproduce KiDS-Legacy's own ΛCDM result: at the best-fit point of their public chain, our pipeline's χ² equals the
chain's value within 0.5. If it does not, stop and report.

## Readings
Per model: **PASSES** if Δ_KiDS ≤ +2 on at least 2 of 3 SN sets, else **OVER**. Combined with DES Y3 (Part 2): a
model whose lensing tension is real should fail both; passing KiDS but not DES points to survey systematics, and that
is reported as a question, not as a fix.

## What may not happen
No refit; no change of KiDS settings; no choice of statistic after seeing results; failures at full size.
