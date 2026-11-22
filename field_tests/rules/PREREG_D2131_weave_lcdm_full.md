# PREREG D2131: the Weave in ΛCDM parts on CMB power spectra + DESI DR2 + supernovae (the SN extension of D2130; referee SN plan folded in). Locked before computing.

**Data:** downloaded with Danny's OK via git from CobayaSampler/sn_data **v1.8** and bao_data **v2.6** (tags checked out). The Cobaya native loaders are used throughout.
- **CMB:** Planck 2018 high-ℓ TTTEEE plik-lite (native), with a Gaussian **τ prior 0.054 ± 0.007** in place of low-ℓ EE. **No low-ℓ TT and no lensing:** those data are not obtainable here (release-asset downloads are blocked), and this is stated as a limitation.
- **BAO:** DESI DR2 (`bao.desi_dr2`).
- **SN, one set per fit, never combined:** Pantheon+ (z > 0.01 cut as in the loader, M marginalised), DES-Y5, Union3.

**Models,** with A_planck ~ N(1, 0.0025) in all of them:

| Model | Free parameters | Fixed |
|---|---|---|
| **L** (ΛCDM) | ω_b, ω_c, H0, n_s, log A, τ, A_planck | Σm_ν 0.06, 1 massive ν |
| **W** (Weave) | ω_b, ω_c, H0, log A, τ, A_planck, u_i | **n_s 0.9706**, n_run −9.7e-4, r 5.4e-4, Σm_ν 0.0587 eV (3ν, normal ordering), N_eff 3.044. DE = the exact reverse thread (A = 7.30, β = 2√2) through the existing rt_theory (cmb-fit/rt_planck_fit.py) |
| **C** (w0waCDM) | the L set + w0, wa | (w0 + wa < 0) |

- **Minimiser:** Cobaya BOBYQA, best of 2.

**Output:**
- χ² per likelihood, plus χ²_eff including the Gaussian τ and A_planck priors;
- Δχ²_eff and ΔAIC versus L;
- for W, the thread's CPL-fitted (w0, wa) over z < 2;
- the n_s pull in L.

**Verdict per SN set (W vs L):** PREFERRED if ΔAIC < −2, CONSISTENT if ≤ +2, MILD TENSION if ≤ +6, DISFAVOURED if > +6. Also report W vs C.
