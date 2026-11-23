# PREREG D2132: the Weave in ΛCDM parts on the NEWEST public data only (Danny 18:18: "just use the new data"; referee R31-1). Supersedes D2131 for headline use. Locked before computing.

**Data.** Danny OK'd the downloads. The NERSC tarballs came through his browser. The SHA-256 sums are recorded in the D-note.

| Probe | What is used | Why |
|---|---|---|
| CMB | **Planck PR4 (NPIPE)**: HiLLiPoP TTTEEE (binned v4.2) + LoLLiPoP low-ℓ EE, plus Planck 2018 low-ℓ TT (PR4 has no newer low-ℓ TT) | replaces the 2018 plik-lite |
| CMB lensing | **Planck PR4 lensing** (`planckpr4lensing`, Carron et al. 2022, data bundled) | |
| BAO | DESI DR2 | the newest public release |
| SN, one set per fit | **DES-Dovekie** (the recalibrated DES-SN5YR) **replaces** DES-Y5; also **Pantheon+** and **Union3**, each the newest release of its compilation | |

- **No τ prior:** LoLLiPoP measures τ.
- **Not included, and stated:** ACT DR6 and SPT-3G spectra. Their likelihood data are not reachable in this session.

**Models:** as D2131 (L, W, C), with all HiLLiPoP nuisance parameters free under their default priors. W is the Weave with n_s 0.9706 fixed, n_run −9.7e-4, r 5.4e-4, Σm_ν 0.0587 eV in normal ordering, N_eff 3.044 and the exact reverse thread (u_i free). Minimiser: BOBYQA, best of 2. χ²_eff = Σχ²(likelihoods) + the Gaussian nuisance-prior penalties (from the logprior).

**Verdicts:**
- Per SN set (W vs L): PREFERRED if Δχ²_eff < −2, CONSISTENT if ≤ +2, MILD TENSION if ≤ +6, DISFAVOURED if > +6. W vs C is reported by ΔAIC.
- **Pre-registered reading for Dovekie (R31-1):** if W − L ≤ −6 on Dovekie, the DES preference holds; otherwise "SN-calibration dependent".
- **Headline:** CONSISTENT / PREFERRED only if it holds on all three sets.

**Data hashes (SHA-256):**
- HiLLiPoP TTTEEE_bin v4.2: 82120210d4349c1d8adcd442d30ae280daf9d472f13e090347efdcd7aefd3111
- LoLLiPoP: 115564f7acc239f1d47ecac264c93baa702f15f814497211bd24f7ebf9f19a3c
- sn_data v1.8 (git 61d9643), bao_data v2.6 (git b7b8a36), planckpr4lensing (git HEAD, pip)

**χ²_eff** = Σχ²(likelihoods) + Σ((x − μ)/σ)² over the Gaussian-prior nuisance parameters. Flat-prior constants are excluded.
