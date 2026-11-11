# DESI-MOCK-CMB: the DESI-MOCK test with the full CMB likelihoods

**Status: LOCKED** on Danny's word ("Get them ready, schedule after", 10 Nov 2026, 22:55 CT, replying to "Say 'lock it'
and I'll lock the rules and write its code tonight, so it's ready to start the moment the MCMC finishes").
AI-assisted. No mock fit exists at lock. Runs on the PC after the FLAG-1 MCMC frees the cores.

**Not blind.** Known at writing: DESI-MOCK (locked) gave REPRODUCES DESI'S SIGNAL with a compressed CMB vector:
Δχ² 11.13 (2.9σ), w0 −0.833, wa −0.451; BAO + CMB alone 1.0σ. DESI DR2 + CMB + Pantheon+: w0 −0.838 ± 0.055,
wa −0.62 ± 0.21.

**Question.** Does the DESI-MOCK reading survive when the CMB enters through the full likelihoods used in our fits,
instead of three compressed numbers?

## Truth
The FLAG-1 Pantheon+ best fit, `cmb-fit/results/cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6.json` (sha256 af165b5739c2bdf2),
all parameters including the CMB nuisances, on its own build (`AxiCLASS_coupled_nlfix`) through Cobaya, with the
fit's own setup (`early_late_spa.make`).

## Mock (noiseless, "Asimov")
Each likelihood's data vector is replaced by that likelihood's own theory vector at the truth, computed by its own code.
Covariances, binning, windows and cuts are unchanged.
- ACT DR6 CMB-only (`act_dr6_cmbonly.ACTDR6CMBonly`): `data_vec`.
- Planck cut (`act_dr6_cmbonly.PlanckActCut`, plik-lite): `X_data`.
- SPT-3G D1 T&E lite (candl): the bandpowers.
- ACT DR6 lensing (`actplanck_baseline`, lens_only False): `data_binned_clkk`.
- DESI DR2 BAO (`bao.desi_dr2.desi_bao_all`): the values.
- Pantheon+ (`sn.pantheonplus`, its own cuts and analytic M marginalisation): the magnitudes.

**Low-ℓ Planck (a change from the draft, decided before any run).** The low-ℓ TT (Gibbs) and EE (probability table)
likelihoods have no data vector to replace, so no Asimov version exists. In every mock fit they are replaced by one
Gaussian prior τ ~ N(τ_truth, 0.0086), the Planck 2018 lowE-alone width. Low-ℓ TT carries little information on w0 or wa.
The DES Y6 S8 term is not used (DESI's analysis has none).

## Fits (DESI convention: uncoupled CDM, plain AxiCLASS build, halofit)
- **ΛCDM:** the `ax_spa_lcdm_halofit` setup.
- **w0waCDM:** the `ax_spa_w0wa_halofit` setup (PPF, CLP fluid, w0 ∈ [−3, 1], wa ∈ [−3, 2], w0 + wa < 0).
- CMB nuisances free with their usual priors (unchanged). Cobaya minimize (bobyqa), best of 4. Starts: shared
  parameters at the truth values; w0 = −1, wa = 0.
- Two combinations: **CMB + BAO + SN** (decides) and **CMB + BAO** (reported).

## Gate (before any fit)
**G-MC:** with the mock installed, at the truth point, every mocked likelihood's χ² (each data term) is ≤ 0.01. The
same point with the real data must give χ² ≠ 0 on each (the swap really happened). If the gate fails: no fits.

## Readings (the same as DESI-MOCK)
Δχ² = χ²(ΛCDM) − χ²(w0wa); significance from χ² with 2 degrees of freedom.
- **REPRODUCES DESI'S SIGNAL:** ≥ 2σ, with recovered wa < 0 and w0 > −1.
- **PARTIAL:** 1–2σ with the same signs.
- **DOES NOT:** anything else.
- Reported: recovered (w0, wa) and their distance from DESI DR2 + CMB + Pantheon+ (one parameter at a time); the
  CMB + BAO significance; the change from the compressed DESI-MOCK.

## What may not happen
No change of truth, mock, covariances, priors, τ width or thresholds after any result. A failed fit is NO VERDICT for
that combination. No rerun to chase a reading. Counted +1 in V7.

## Code
`field_tests/desi_mock/desi_mock_cmb.py` (modes truth, gate, fit, score); PC job
`field_tests/desi_mock/run_mock_cmb_pc.sh` (waits for the MCMC to finish).
