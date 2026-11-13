LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_WA_CEILING — the Twist cannot make w_a very negative

## Hypothesis
Every Twist version is a field that starts frozen and thaws (PURE-TWIST, FLAG-1 with its dark-matter coupling, free
kappa). Read by an observer who assumes ordinary dark matter and fits w0 + wa(1 - a), they give (effective_w.py,
13 Nov 2026, stored best fits): PURE-TWIST w0 -0.905, wa -0.098; FLAG-1 w0 -0.857, wa -0.266 (w_eff dips to -1.04,
an apparent crossing made by the coupling); free kappa w0 -0.899, wa -0.178. Raising the coupling saturates near
wa -0.30 (beta 0.08); CLASS fails beyond beta ~ 0.1. The estimator reads a known w0wa model about 0.06 too shallow in
wa (check: true -0.367, read -0.308). **Ceiling: the Twist predicts wa >= -0.40** (-0.30 saturation, -0.06 estimator
bias, rounded down).

## Context when locked (not scored)
DESI DR2 + CMB + DES Y5 (unified tracer, arXiv:2608.27830): w0 -0.803 +/- 0.054, wa -0.73 (+0.21 / -0.19).
On the TOURNAMENT likelihood (DESI DR2 + Pantheon+ + compressed CMB) a free w0wa fit gives wa -0.367.

## Data that will be scored
The first DESI DR3 BAO cosmology paper's headline w0waCDM result combining DESI BAO + CMB + a supernova set (if
several SN sets are given, each is scored and the reading is the one for the combination DESI names as baseline; the
others are reported). If Euclid or another survey publishes a comparable w0wa result first, it is scored the same way.

## Readings (wa with its published 1 sigma upper error sigma_+)
- **SUPPORTED**: wa + sigma_+ >= -0.40.
- **NOT SUPPORTED**: wa + 3 sigma_+ < -0.40 (the ceiling excluded at 3 sigma).
- **TENSION**: otherwise.
A NOT SUPPORTED reading applies to every thawing Twist version at once (PURE-TWIST, FLAG-1, free kappa).

## Failure handling
No re-reading. Corrections only in PREREG_WA_CEILING_DEVIATIONS.md, written before any rescoring.
