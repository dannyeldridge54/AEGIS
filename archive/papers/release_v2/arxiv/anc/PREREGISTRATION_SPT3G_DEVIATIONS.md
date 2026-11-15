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
