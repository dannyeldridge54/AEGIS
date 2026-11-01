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
