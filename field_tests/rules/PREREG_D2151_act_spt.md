# PREREG D2151: the Weave against ACT DR6 and SPT-3G (Danny 21:12, downloads OK'd). Locked before any install output was read and before any fit

**Why.** ACT DR6 and SPT-3G are the newest ground-based CMB data. ACT's n_s (0.974 ± 0.003 with DESI) is the first number experts will check against the Weave's fixed n_s = 0.9706.

## Data combinations (each × SN ∈ {DES-Dovekie, Pantheon+, Union3}, plus DESI DR2 BAO)
- **ACT-based:** ACT DR6 MFLike (TT/TE/EE, baseline foreground model and priors from the package) + ACT DR6 lensing + Planck 2018 low-ℓ TT + PR4 LoLLiPoP low-ℓ EE (for τ).
  - Planck high-ℓ is **not** included, so no sky overlap is double-counted.
- **SPT-based:** the SPT-3G D1 likelihood via candl / spt_candl_data, using the shortcut for the collaboration's baseline TT/TE/EE (and lensing if the shortcut includes it), + the same low-ℓ Planck.
  - The exact shortcut name is recorded in an addendum **before** fitting, from print_all_shortcuts().

## Models
L (ΛCDM, n_s free) and W (Weave: fixed n_s 0.9706, running, r, Σm_ν = 0.0587 eV with normal ordering, thread u_i free). C (w0wa) only if time allows.

## Settings
- The same as D2132: BOBYQA best_of 2, u_i reference range (0.02, 0.20) per the D2132 DEV, CAMB 2.0.5, Cobaya 3.6.2 in a separate venv.
- **Labelled deviation from the ACT baseline:** ACT's baseline uses CosmoRec. This run uses CAMB's default recombination unless CosmoRec is available.

## Verdict rule (fixed now)
- **The D2132 rule** (same free-parameter count): PREFERRED if Δχ²_eff < −2; CONSISTENT if ≤ +2; MILD TENSION if ≤ +6; DISFAVOURED if > +6.
- **Reported in addition:**
  - the n_s pull of L's best fit against 0.9706;
  - the fixed-n_s cost on each CMB block.
- **Cross-experiment rule.** A verdict is "CMB-robust" only if Planck PR4 (D2132/D2135), ACT and SPT all fall in the same class or neighbouring classes.

No reruns to chase results. Code fixes go in DEVIATIONS written before any rerun.

## ADDENDUM 1 (install facts, 21:20 CT; no fit has run)
- **Planned:** a separate venv. **What happened:** the first version of the install script ran, and it installs into the existing venv312.
- **What it added:** only act_dr6_mflike 1.1.0, fgspectra 1.4.1, mflike 1.0.2 and syslibrary 0.2.
  - act_dr6_lenslike 1.2.1, candl-like 2.0.3 and spt_candl_data were **already installed** from earlier sessions.
  - cobaya 3.6.2, camb 2.0.5, numpy and scipy are **unchanged**. The 12 running fits are not affected.
- **Decision:** use venv312 for D2151. This also keeps the versions identical to D2132/D2135.
- **ACT DR6 data:** being fetched by cobaya-install from lambda.gsfc.nasa.gov (dr6_data.tar.gz, 394 MB), into ufe_data\packages.
- **The pip install of spt_candl_data from git failed** (git is not on PATH), but the package was already importable.

## ADDENDUM 2 (fixed after the smoke test; no fit has run, and the smoke test scores nothing)
- **Likelihoods chosen:**
  - **ACT:** the collaboration's official foreground-marginalised **DR6 "lite"** likelihood (`act_dr6_cmbonly`, DR6-ACT-lite 1.0.0, data from LAMBDA), with A_act ~ N(1, 0.003) and P_act ∈ [0.5, 1.5], as in ACT-DR6-parameters, plus `act_dr6_lenslike.ACTDR6LensLike`. The full multi-frequency MFLike (about 30 foreground nuisances) was installed but is **not** used, for runtime reasons. This is labelled.
  - **SPT:** `spt_candl_data.SPT3G_D1_TnE_lite` through candl's CandlCobayaLikelihood. Its internal priors are cleared (our LoLLiPoP sets τ). Tcal ~ N(1, 0.0036), taken from the data set's own prior; Ecal is uniform in [0.9, 1.1].
- **CAMB accuracy:** ACT's settings, without CosmoRec and without `lens_margin`. `lens_margin` is not a CAMB 2.0.5 argument, and the smoke test rejected it. halofit stays 'mead', as in D2132.
- **First launch:** L and W on Dovekie for each experiment (4 processes). Pantheon+ and Union3 follow when cores free up.
