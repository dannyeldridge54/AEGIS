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

## 2026-10-29 23:38 CT
5. **Runner restart (no change).** The lane runner process was terminated about 35 minutes in (exit -1, cause not in its log); the five N-profile fits (N = 6, 7, 8, 10, 11 on P-ACT) died mid-minimisation. Their partial files are archived by the existing stale-run rule and the same jobs are restarted unchanged. No result had been produced or read.

## 2026-10-31 10:10 CT
6. **Runner restart (no change).** The lane runner had been stopped with results/lanes/STOP (created 2026-10-30 03:11). It is restarted unchanged at Danny's request, with the same queue: the remaining Planck N-profile fits (edelockP_F8, F10, F12) and the 12 MCMC chains of step 1.1 (pact_lcdm, pact_edelock, pact_edelock_F9; chains 1-4 each). No Phase 1 result file was opened before this restart. Restarted by Claude.

## 2026-10-31 12:26 CT
7. **PC restart (no change).** Danny restarted the PC to enable virtualization (for WSL/AxiCLASS, step 1.3). All fits stopped. The 12 MCMC chains resume from their saved samples; their stale 'running' entries in results/lanes/status.json are cleared so the runner re-claims them. Queue, priors, settings and rules are unchanged; no Phase 1 MCMC result was read. Restarted by Claude.

## 2026-10-31 12:48 CT
8. **Second PC restart (no change).** The WSL service had hung during Ubuntu setup, so the PC was restarted again at about 12:44. As in entry 7, the chains resume from their saved samples and their stale status entries are cleared. Nothing else changes, and no Phase 1 MCMC result was read.

## 2026-10-31 13:23 CT
9. **Step 1.3 premise (reported, rule unchanged).** Step 1.3 says the CAMB fits use "the fluid approximation". They do not:
   - CAMB's EarlyQuintessence integrates the scalar field and its perturbations directly. Its documentation says field
     value and derivative are stored and splined.
   - The 26 Oct AxiCLASS cloud runs also used AxiCLASS's scalar-field mode (f_axion_ac, scf_param_1), not its fluid
     mode.

   So every AEGIS fit already uses an exact (linear-order) scalar-field solver. The existing engine check
   (engine_check.py) compared the two independent field solvers at the same points: Δχ² −6.54 (CAMB) vs −6.52
   (AxiCLASS), a difference of 0.02.

   Step 1.3 as written (P-ACT, Locked Twist and Twist-1H, re-minimised) has not been run, so no verdict is claimed
   here. AxiCLASS is now built in WSL (Ubuntu, micromamba env 'aegis', classy 3.3.0, smoke test passed), so the step
   can still be run as a same-data cross-engine check if wanted. Logged by Claude.