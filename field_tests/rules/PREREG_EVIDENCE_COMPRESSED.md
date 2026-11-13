LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_EVIDENCE_COMPRESSED — Bayesian evidence for the late-time versions

## Question
Best-fit Δχ² rewards extra parameters. The Bayesian evidence Z penalises them through the prior volume. Compare
LCDM, PURE-TWIST (0 extra), K816 (beta free, 1 extra) and free w0wa (2 extra) on equal footing.

## Likelihood
tournament.chi2 FULL configuration (DESI DR2 BAO + Pantheon+ + compressed CMB); log L = -chi2/2.

## Priors (flat; identical shared ranges)
h [0.60, 0.75]; omega_b [0.0215, 0.0235]; omega_cdm [0.105, 0.130]; beta (K816) [0, 0.10]; w0 [-1.5, -0.5];
wa [-2.0, 1.0] with w0 + wa < 0. Shared ranges are wide compared with the posteriors (compressed CMB pins omega_b and
omega_cdm), so they cancel in the ratios to good approximation; the reported ln B depends on the beta, w0, wa ranges,
which are fixed here before any run.

## Sampler
dynesty 3.1.0 static nested sampling, 300 live points, 'rwalk', dlogz = 0.1, seed 1. One run per model.

## Readings (ln B = ln Z_model - ln Z_LCDM; Jeffreys/Trotta scale)
|ln B| < 1 inconclusive; 1-2.5 weak; 2.5-5 moderate; > 5 strong. Reported for each model vs LCDM and PURE-TWIST vs K816.
**PURE PREFERRED BY EVIDENCE** if ln B(PURE vs LCDM) >= 1 and ln B(PURE vs K816) >= 0; **K816 PREFERRED BY EVIDENCE** if
ln B(K816 vs LCDM) >= 1 and ln B(K816 vs PURE) > 0; **NO EVIDENCE FOR THE TWIST** if both ln B vs LCDM < 1; **MIXED** otherwise (numbers reported).

## Failure handling
No reruns to chase results; corrections only in PREREG_EVIDENCE_COMPRESSED_DEVIATIONS.md before any rerun.
