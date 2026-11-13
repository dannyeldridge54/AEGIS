LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_DESY5_SWAP — does the Twist survive on the supernovae that drive w_a ~ -0.7?

## Question
DESI's headline w_a ~ -0.73 (DR2 + CMB + DES Y5) is far below the Twist's ceiling (-0.40, PREREG_WA_CEILING). Our
TOURNAMENT likelihood uses Pantheon+, where a free w0wa fit gives w_a -0.37. Swap Pantheon+ for DES Y5 and refit.

## Likelihood
tournament.chi2 (FULL configuration: DESI DR2 BAO + compressed CMB) with the supernova block replaced by DES-SN5YR
(cobaya_packages sn_data/DESY5: DES-SN5YR_HD.csv, all 1829 SNe, MU with covariance covsys_000 + diag(MUERR_FINAL^2)),
same analytic offset marginalisation, redshifts zHD (cosmological) and zHEL (heliocentric). Nothing else changes.

## Models and fitting
LCDM [h, wb, wc]; W0WA [h, wb, wc, w0, wa]; PURE-TWIST ("SPIRAL", beta 0, kappa 0.8165 fixed: 3 free);
FLAG-1 ("FLAG1", 4 free). Starts: tournament.starts (PURE-TWIST uses the LCDM starts). Nelder-Mead exactly as
pure_twist.fit (xatol 1e-6, fatol 1e-3, maxiter = maxfev = 1500); best of the starts.

## Gate
DES Y5 loads with 1829 SNe and the LCDM best chi2 is finite; the W0WA fit gives w_a < -0.40 (the swap reproduces the
low-w_a preference that motivates the test). If the gate fails: NO VERDICT.

## Readings (Delta = chi2_model - chi2_LCDM on this likelihood)
- **TWIST HOLDS ON DES Y5** if Delta_PURE <= -2 AND Delta_PURE - Delta_W0WA <= +4 (W0WA has 2 more parameters).
- **STRAINED** if Delta_PURE <= 0 but Delta_PURE - Delta_W0WA > +4.
- **FAILS ON DES Y5** if Delta_PURE > 0.
FLAG-1 is scored with the same three bands (secondary, reported beside PURE-TWIST). The effective w0, wa of the Twist
fits (effective_w.py method) are reported beside the W0WA fit.

## Failure handling
No reruns to chase results. Corrections only in PREREG_DESY5_SWAP_DEVIATIONS.md, written before any rerun.
