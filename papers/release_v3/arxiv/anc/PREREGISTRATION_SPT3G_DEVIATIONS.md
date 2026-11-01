# SPT-3G pre-registrations: deviations log (append only, dated)

Applies to `PREREGISTRATION_SPT3G_N9.md` (DOI 10.5281/zenodo.23838969) and `PREREGISTRATION_SPT3G_SILVER.md`
(DOI 10.5281/zenodo.23839507). Both are locked. Every technical choice made while setting up the runs is listed here
**before any SPT-3G fit of any Twist model has run**. Rules, thresholds and models are not changed.

## 2026-10-31, before the first SPT-3G fit

**1. Likelihood.**
- **What is used:** SPT-3G D1 TT/TE/EE (Camphuis et al. 2025) through `candl` + `spt_candl_data` 3.0.1, in the
  **"lite" variant** (foreground-marginalised; `spt_candl_data.SPT3G_D1_TnE`, variant `lite`).
- **Why:** it is the same data with foregrounds marginalised, the analogue of Planck plik-lite used in all earlier
  fits, and SPT ships it with a Cobaya template.
- **Not run:** the full multi-frequency version.

**2. τ prior.**
- **What is used:** the pre-registrations say "a τ prior from Planck low-ℓ EE". It is implemented as SPT's own
  template prior, **τ ~ N(0.051, 0.006)**, which represents Planck low-ℓ EE, instead of loading the Planck low-ℓ EE
  likelihood itself.
- **Also removed:** Planck low-ℓ TT is not included, as it was not listed. All Planck high-ℓ and lensing likelihoods
  are removed, so **SPT-3G is the only CMB data**.

**3. Calibrations and settings.** These follow SPT's template:
- Tcal and Ecal free on [0.8, 1.2], with Tcal ~ N(1, 0.0036);
- CAMB `lens_potential_accuracy = 4`.

SPT's `lens_margin = 1250` is dropped because CAMB 2.0.5 does not accept it.

**4. Software check.**
- **The problem:** SPT's `run_all_tests()` fails with the installed JAX (0.10.2). The failing call is in candl's
  internal-prior helper, which rejects a Python list.
- **Why it doesn't affect the runs:** the Cobaya runs switch internal priors off (`clear_internal_priors: true`, as
  in SPT's template) and add the same priors explicitly.
- **The check that passed:**
  - Claude reproduced SPT's lite reference test by hand: −χ²/2 = −83.0457, plus the internal priors (τ: −0.1250;
    Tcal: −0.0386), gives −83.2092. The reference is −83.2092, a relative difference of 6 × 10⁻¹¹.
  - The internal priors are exactly the τ and Tcal priors added in item 3.
- **Version:** candl-like 2.0.3, as SPT documents. (2.2.0 was installed first and replaced; the test failure is the
  same with both.)

**5. Fitting.** Each fit uses the AEGIS settings:
- CAMB 2.0.5 EarlyQuintessence + Cobaya, bobyqa minimizer, best of 4;
- started near the earlier best points (START_EDE / START_LCDM);
- one CPU thread per fit, because 12 MCMC chains share the PC.

**6. Runs (job names in `cmbfit_compare.py`):**

| Job | Role |
|---|---|
| `spt_lcdm` | ΛCDM reference for both rules |
| `spt_edelock_F9` | **N = 9 primary test** (one setting, θ_i free); also the silver **angle check** |
| `spt_edelock_th2.41421_F9` | **Silver-ratio primary test** (zero settings) |
| `spt_edelock` | **N = 9 width check** (free width); implied N = 1.2247 / F read from CAMB at the minimum |
| `spt_edelock_th2.78_F9` | Contrast at the Planck-preferred angle. **Not a prediction**, as the silver pre-registration says |

**7. Counting settings.** The zero-setting model still samples f_EDE, but f_EDE is pinned by the 1% width constraint,
as allowed in the silver pre-registration. That constraint's own χ² is removed before comparing with ΛCDM, as in all
earlier width-fixed fits.

## 2026-10-31 12:26 CT

**8. Restart.** The PC was restarted before any SPT-3G fit finished. The three running fits (spt_lcdm, spt_edelock_F9, spt_edelock_th2.41421_F9) start again from scratch: Cobaya's minimizer cannot resume, and its partial files are archived by AEGIS's stale-run rule. Nothing else changes, and no SPT-3G result had been produced or read.

## 2026-10-31 12:48 CT

**9. Second restart.** The PC was restarted again at about 12:44 to clear a hung WSL service, before any SPT-3G fit finished. The SPT-3G fits start again from scratch, exactly as in item 8. Nothing else changes, and no SPT-3G result had been produced or read.

## 2026-10-31 13:25 CT

**10. Re-queued after restart.** spt_edelock and spt_edelock_th2.78_F9 were claimed at 12:44 just before the second restart and were killed (no error in their logs). The runner had marked them failed, so they are re-queued unchanged. They run once a lane frees up. No result was read.

## 2026-10-31T20:08 CT: PREREGISTRATION_COMBINED_CMB.md time stamp

The file says "Written: 31 October 2026, 18:50 CT". That time was wrong: it was written and committed at 20:08 CT
(git commit ed2ce8d, SHA-256 c35316fd...). Every statement in it still holds at 20:08: no combined Planck + ACT +
SPT-3G fit and no w0-wa fit had been written as code, run or queued. The locked file is not edited.

## 2026-10-31 20:43 CT: PREREGISTRATION_DEEP_SEARCH.md time stamp

The file says "about 21:10 CT"; it was written and committed at 20:42 CT (e548f2f). No `_deep` run had been written as
code or run at that time. The locked file is not edited. (From now on the time is taken from the clock, not written
by hand.)

## 2026-10-31 21:05 CT: PREREGISTRATION_POWER_N.md, two deviations before any fit ran

1. **n = 1 cannot be run.** CAMB 2.0.5's EarlyQuintessence (z_c, f_EDE) solver returns a non-finite likelihood for
   n = 1 at every tested point (theta_i 1.0-2.8, f 0.02-0.07). `spa_edelock_n1` is not queued. An n = 1 test needs
   another engine (AxiCLASS supports n = 1) and is deferred. The published literature finds n = 1 does not work as early
   dark energy, because it decays like matter (Poulin et al. 2018); that is context, not our result.
2. **n = 2 starts lower.** At theta_i ~ 2.8 the solver also fails for n = 2. `spa_edelock_n2` starts from theta_i ~
   N(2.5, 0.04) instead of 2.79. Starting point only; the prior, data and rule are unchanged. No result had been read.

## 2026-10-31 22:05 CT: PREREGISTRATION_LATE_TWIST.md, one deviation before any fit ran

HMcode in this AxiCLASS build refuses a scalar field present today ("Cannot use scalar field scf with HMcode (not yet
coded)"). So the Late Twist uses halofit for non-linear lensing, and its references are re-run with the same setting:
`ax_spa_lcdm_halofit` and `ax_spa_w0wa_halofit` replace `ax_spa_lcdm` and `ax_spa_w0wa` in tests L1 and L2.
Everything else is unchanged. No result had been read.

## 2026-11-01 07:00 CT: A3 results saved from Cobaya's own files (bookkeeping, no fit changed)

All four A3 fits (`ax_spa_*`) converged, but `early_late_spa.py` crashed while writing `cmp_<name>.json`. The cause was
`mini.products()["minimum"]`, a Cobaya `OnePoint` with no `keys()`. The JSONs were rebuilt from Cobaya's own
`results/chains/cmp_<name>.minimum.txt` with a new `save` mode, and `run()` now uses the same path. No fit, prior or rule
changed, and nothing was rerun.
## 2026-11-01 07:24 CT: Late Twist minimiser guard (PREREGISTRATION_LATE_TWIST.md; model, priors and rules unchanged)

The first `ax_spa_latetwist` run failed: both bobyqa restarts stopped with a singular matrix after the likelihood sum
overflowed. No result was produced or read. A diagnostic grid (`axiclass/probe_latetwist.py`, other parameters at the
AxiCLASS LCDM best fit) shows three regions:
- **-inf where F x m is too small:** the field cannot hold enough energy to close the budget.
- **NaN near m ~ 6 H0:** the field overshoots and oscillates.
- **A finite valley near F ~ 1 M_Pl, m ~ 1.6 H0.**

**Change:** for Late Twist runs only (`ax_spa_latetwist`, `ax_spa_latetwist_desy5`), any non-finite log-posterior,
or one below -1e5, is returned to the minimiser as -1e5, a clean rejection instead of an overflow. The guard applies
only during minimisation, so Cobaya's check that redraws non-finite starting points is unchanged. Same priors, same
references, same best of 2. The run is repeated, and the earlier failed attempt is kept in its log.
## 2026-11-01 07:46 CT: Late Twist rerun with better starting points (author approved in chat: "Yes, rerun it")

**The result was seen first** (LATE_TWIST_RESULTS.md), so this deviation is disclosed as post-result.

**Why:** the guarded `ax_spa_latetwist` run reported chi2 = 2413.90, but holding its own best (F, m) and moving the
other parameters to the AxiCLASS LCDM halofit best fit gives chi2 = 2402.66 (`axiclass/probe_corner.py`). The minimiser
did not find the minimum. Its starting references came from CAMB fits (`_start_from_camb`), whose theta parameter is
not the same quantity as CLASS's 100*theta_s.

**Change** (Late Twist runs only, `ax_spa_latetwist` and `ax_spa_latetwist_desy5`):
- The cosmological and calibration references are centred on the AxiCLASS `ax_spa_lcdm_halofit` best fit.
- **Best of 4** instead of 2.

**Unchanged:** priors, the F and m references, the guard, data, rules and verdict bands.

**Record:** the stalled result is kept as `cmp_ax_spa_latetwist.stalled1.json`, with its verdicts recorded in
LATE_TWIST_RESULTS.md. The rerun's verdicts are reported beside it, with both runs shown.
## 2026-11-01 07:52 CT: robustness queue restarted (scheduling only)

`run_robustness.sh` waited for `cmp_ax_spa_latetwist.json`, which was archived for the approved rerun, so batch 1
never started. It was replaced by `run_robustness2.sh`:
- batch 1 starts now, at 2 threads per fit beside the 4-thread Late Twist rerun;
- batch 2 starts after both batch 1 and the rerun have finished.

The runs, settings and rules are unchanged.
## 2026-11-01 (audit): correction to PREREGISTRATION_SPT3G_LETTERS.md timing statement

The Letters pre-registration says it was written "before any SPT-3G fit of the free-width Locked Twist (spt_edelock)
had run". The timestamps disagree:
- the run was **launched at 14:04:34** (its Cobaya input file);
- the pre-registration was committed at 14:07:35;
- the run's result (`cmp_spt_edelock.json`) was first written at 17:04:51.

So the rule was locked **after the fit started but about 3 hours before any result existed**. No number from it could
have been seen. The sentence should have read "before any result of that fit existed". The verdict (Inconclusive)
stands. The file itself is unchanged (hash `c86f2b75…`).

Every other pre-registration was checked the same way and was committed before its first run started (gaps from
14 seconds to 9 hours).
## 2026-11-01 08:08 CT: PREREGISTRATION_COUPLED_TWIST.md time stamp

The header says "Written: 2026-11-01 08:10 CT". That time was hand-written and is wrong (the same mistake as twice on
31 October). The file was committed at **08:06:59** (commit b75b8f8), after a clock check at 08:05:42 confirmed that
`cmp_ax_spa_latetwist.json` did not exist. The true written time is therefore **08:05–08:07**. Nothing else is
affected; the file is unchanged (SHA-256 `1aea70eb…`).

**Process fix:** from now on, the "Written" line is filled from `Get-Date` in the same command that hashes the file.
## 2026-11-01 08:20 CT: PREREGISTRATION_COUPLED_TWIST.md gate V4 sign wording (before any code exists)

Gate V4 says "β > 0 makes ρ_c fall faster than a⁻³ while φ̇ > 0". The model's own equation,
ρ̇_c + 3Hρ_c = (β/M_Pl) φ̇ ρ_c, gives faster-than-a⁻³ dilution when **β φ̇ < 0**. The derivation is in
COUPLED_TWIST_NOTES.md §1; in the φMDE, x = −√(2/3) β, so β > 0 pairs with φ̇ < 0.

**Change:** V4 will be applied as "d ln(ρ_c a³)/dt = (β/M_Pl) φ̇, with the sign of β φ̇", the physical content it
intended. No model, prior or rule is otherwise changed, and no coupled code or fit exists yet.
## 2026-11-01 08:12 CT: two hand-typed header times in this log (audit), corrected below

The house check now compares each header's time with the commit that added it. Two headers were typed by hand, after I
had said times would come from the clock:
- **header 08:08 corrected** to 08:07: the time-stamp entry was committed at 08:07:14 (3a11f3a);
- **header 08:20 corrected** to 08:08: the V4 sign-wording entry was committed at 08:08:48 (12a523d).

Also corrected: LATE_TWIST_RESULTS.md said the guard deviation was "logged 07:16"; its commit (8c2c095) is at 07:24:18.
The order of events is unaffected: each deviation was committed before the run or code it covers. Only the written
times were wrong. This header was taken from `Get-Date`.
## 2026-11-01 08:39 CT: Coupled Twist C5, reading of a fit with no finite point (before any coupled fit)

A smoke test of the C5 run (|β| = 0.816 fixed) found no finite likelihood at the reference point. CLASS's
recombination solver fails ("step size too small") because the field holds about 30% of the energy through the matter
era (Ω_φ ≈ 2β²f_c²/3 ≈ 0.31). The background code runs fine at β = 0.3 (energy balance 1.2 × 10⁻⁷).

**How C5 will be read:**
- If the C5 fits (both signs, best of 4, with Cobaya's redraws of the starting point) find **no finite point**, C5 is
  reported as **EXCLUDED (code-limited)**. The wording says the cosmology cannot be computed, rather than that a χ²
  was compared.
- If either sign finds a finite best fit, the rule applies as written.

No rule, prior or band is changed.
## 2026-11-01 08:58 CT: (F, m) profile grid replaces free (F, m) minimisation for scalar-field late models (author approved: "Yes")

**This change is made after the result was seen.** The Late Twist results (stalled +11.6, then +3.2) were known before
it.

**Why:** bobyqa stalls on the walled (F, m) surface: restarts disagree by up to 6.8, and probe points that need no fitting
sit 2.5 or more below the reported minima (DEEP_REVIEW_2026-11-01b.md §3).

**Change:**
- **Late Twist, Pantheon+ and DES Y5:** F and m are fixed on a grid, log10(F/M_Pl) ∈ {−0.4, −0.2, 0, 0.2, 0.4, 0.5}
  × log10(m/H₀) ∈ {−0.3, 0, 0.2, 0.4} (24 points, inside the pre-registered priors). At each point the 11 standard
  parameters are minimised (best of 2). **The fit is the lowest grid χ².** L1–L3 and shared F are judged on it, using the
  F and m of that point. A grid point with no finite likelihood (closure impossible) is recorded as non-viable.
  - The grid's resolution is 0.2 dex. It is reported as a caveat; no refinement is added after seeing the results.
- **Coupled Twist** (no coupled result exists yet):
  - the C1–C4 fit becomes a 3 × 3 (F, m) grid at ±0.2 dex around the best Late Twist (Pantheon+) grid point, with β
    free;
  - C5 (β = ±0.816) and the 5-point β profile are run at the best coupled grid point.
- **Unchanged:** priors, data, the guard, and every rule and band.
- **Kept on record:** the two free Late Twist fits.