# Phase 1 deviations log (append only, dated; see PREREG_PHASE1.md)

Every technical change made while running Phase 1 is listed here, with its date and reason, before the affected result
is read. Rules, data and priors are never changed.

## 2026-10-29 23:10 CT (before any Phase 1 run started)
1. **f_EDE prior lower edge is 0.001, not 0.** CAMB's early-quintessence solver cannot run at exactly zero; the
   existing code has always used 0.001. This cannot affect the 1.1 rule, whose threshold is 0.01.
2. **The 4 MCMC chains per model run as 4 independent processes** (seeds 1001 to 1004), each stopping at its own
   Gelman–Rubin R − 1 < 0.02 (computed from its batches). The across-chain R − 1 < 0.02 required by the rule is
   computed afterwards from all 4 chains with GetDist; if it is not met, the chains are extended, never cut.
3. **Twist-1H in MCMC** fixes the width with the same 1% constraint used in the blind test (fwidth.py); that
   constraint's χ² is part of the model, as before.
4. **Order of work:** step 1.2 (profile in N, hours) runs first, then step 1.1 (MCMC, days). Steps 1.3 (exact field
   code) and 1.4 (full weak-lensing likelihood) need new code; it will be written and logged here before they run.
