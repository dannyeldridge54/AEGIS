# V6: the flagship on Planck PR4 (NPIPE) instead of Planck 2018

**Status: LOCKED** on Danny's word ("Start trsting them", 12 Nov 2026, 18:14 CT, replying to the pending draft rules), before any of its numbers were computed. Drafted:, written 12 Nov 2026 when Danny asked for every pending test to be queued ("schedule them all to set
automatically in q", 14:17 CT). V6 had no rule yet (PREREG_SELFCHECK.md: "It gets its own rule"), so this one is a
draft and becomes AI-assisted. PC.

**Why.** All flagship fits use Planck 2018 (PR3) data. Planck's final reprocessing, PR4 (NPIPE), has lower noise and
different systematics handling. If FLAG-1's edge depends on PR3's particular processing, it should change on PR4.

**Not blind.** Known at writing: DATA-GEN fit C (Planck-only CMB with PR3: low-ℓ TT and EE, plik-lite TTTEEE, PR3
lensing; DESI DR2; Pantheon+; DES Y6 S8): Δχ² −3.91, β 0.040.

## Fits (PC)
Exactly DATA-GEN fit C (`_planckfull` setup, same build, priors, starts from the stored Pantheon+ s8y6 minima, best of 4),
with one change: the Planck high-ℓ likelihood `planck_2018_highl_plik.TTTEEE_lite_native` is replaced by Planck PR4
CamSpec, `planck_NPIPE_highl_CamSpec.TTTEEE`, with its own default nuisance parameters and priors. Low-ℓ TT and EE and
the lensing likelihood stay PR3 (no PR4 versions are installed). Data: the PR4 CamSpec files already on the PC
(`ufe_data/packages/data/planck_NPIPE_CamSpec`, used on 30 Oct); no download.
- Names: `ax_spa_spiraltwist_kappa1_nlfix_pr4_s8y6`, `ax_spa_lcdm_halofit_pr4_s8y6`.
- **Gate:** before the fits, the full setup is evaluated at each model's stored fit-C minimum; every likelihood term must
  be finite. If not: NO VERDICT, no fits.

## Readings
Δ_PR4 = χ²(FLAG-1) − χ²(ΛCDM) with PR4.
- **HOLDS ON PR4:** Δ_PR4 ≤ −2 and β_eff > 0.01.
- **WEAKENS:** −2 < Δ_PR4 ≤ 0.
- **REVERSES:** Δ_PR4 > 0.
- Also reported: β, H0, S8 for both models; Δ_PR4 beside fit C's −3.91; the per-likelihood χ².

## What may not happen
No change of likelihoods, priors, starts or bands after any result. A failed fit is NO VERDICT. Counted +1 in V7.

## Code
`field_tests/selfcheck/v6_pr4_fit.py` (modes gate FLAG1|LCDM, fit FLAG1|LCDM, score); PC job
`field_tests/selfcheck/run_v6_pc.sh` (waits for the DESI-HOLDOUT fits to finish).
