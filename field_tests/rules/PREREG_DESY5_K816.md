LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_DESY5_K816 — the base-slope coupled Twist on DES Y5

## Question
PREREG_DESY5_SWAP (scored 13 Nov) found PURE-TWIST (kappa = sqrt(2/3), beta = 0) STRAINED and FLAG-1 (kappa = 1,
beta free) HOLDS on DES Y5. The base theory fixes kappa = sqrt(2/3); the version with that slope and beta free (K816,
as in PREREG_KAPPA_ALPHA1) was not in the swap. This rule adds it, with everything else identical.

## Likelihood, fitting, comparison
desy5_swap.py likelihood unchanged (TOURNAMENT FULL with DES Y5). Model K816: tournament "SPIRAL" with
p = [h, wb, wc, beta, 0.8165] (4 free: h, wb, wc, beta). Starts: tournament.starts("FLAG1"). Nelder-Mead as in the swap.
Compared with the stored DESY5-SWAP fits (field_tests/results/desy5_swap.json): LCDM chi2 1661.794, W0WA 1645.628.

## Readings (same bands as PREREG_DESY5_SWAP)
Delta = chi2_K816 - chi2_LCDM; TWIST HOLDS ON DES Y5 if Delta <= -2 and Delta - Delta_W0WA <= +4; STRAINED if
Delta <= 0 otherwise; FAILS ON DES Y5 if Delta > 0. Effective w0, wa of the K816 fit reported (effective_w.py method).

## Failure handling
No reruns to chase results; corrections only in PREREG_DESY5_K816_DEVIATIONS.md before any rerun.
