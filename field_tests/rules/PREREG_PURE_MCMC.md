LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_PURE_MCMC — posteriors for PURE-TWIST and LCDM on the TOURNAMENT likelihood

## Purpose
PURE-TWIST (kappa = sqrt(2/3), beta = 0) was scored PREFERRED from best fits (PREREG_PURE_TWIST.md). This rule gives the
full parameter posteriors, so the preference and the derived numbers come with honest intervals. It is a precision
exercise on data already used, not a new test: no new verdict on the model, only intervals and a stability check.

## Likelihood and data (identical to the PURE-TWIST FULL configuration)
tournament.chi2(version, p, T.bao_desi()): DESI DR2 BAO + Pantheon+ (analytic magnitude marginalisation) + compressed
CMB (100 theta*, omega_b, omega_b + omega_c at recombination). PURE-TWIST: version "SPIRAL", p = [h, omega_b,
omega_cdm, 0.0, 0.8165]. LCDM: version "LCDM", p = [h, omega_b, omega_cdm]. Log-likelihood = -chi2/2.

## Priors (flat, inside tournament.in_bounds)
h in [0.55, 0.80]; omega_b in [0.018, 0.026]; omega_cdm in [0.09, 0.15]. A point the code rejects (chi2 = 1e10) has
zero prior weight.

## Sampler
emcee 3.1.6, 12 walkers per model, initial ball of radius 1e-3 (relative) around the stored best fits
(pure_twist_predictions.json). Thinning none. Burn-in: the first half of the chain is discarded.
Convergence: split-R-hat (Gelman-Rubin on the walkers' halves of the kept chain) R - 1 < 0.02 for all three
parameters AND chain length > 30 x the integrated autocorrelation time. Checked every 500 steps; maximum 6000 steps.
If the maximum is reached without convergence, the result is reported as NOT CONVERGED with the numbers anyway.

## Reported (both models)
Median and 68% interval of H0, Omega_m (= (omega_b + omega_cdm)/h^2), omega_b, omega_cdm; minimum chi2 in the chain;
posterior mean chi2. For PURE-TWIST also delta chi2_min (PURE - LCDM) from the chains.

## Readings
- **CONSISTENT** if the chains' minimum chi2 are within 0.2 of the stored best fits for both models (the best fits were
  real minima) and |delta chi2_min - (-3.37)| <= 0.5.
- **BEST FIT WAS NOT THE MINIMUM** if a chain finds chi2 lower than the stored best fit by more than 0.2 (the
  PURE-TWIST verdict is then recomputed and reported beside the locked one, which is not changed).
- **NOT CONVERGED** as above.

## Failure handling
No reruns to chase results. Corrections only in PREREG_PURE_MCMC_DEVIATIONS.md, written before any rerun.
