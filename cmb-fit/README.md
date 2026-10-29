# AEGIS CMB fit — the decisive test of the torsion-born EDE model

**Question:** does the torsion field still raise H0 once the *full* Planck CMB spectrum is included,
not just the acoustic angle? Background-only fits (AEGIS v2) cannot answer this, because the CMB peak
heights are what pin down the dark-matter density ω_c.

**How:** the torsion field's Lagrangian (canonical Barbero–Immirzi pseudoscalar,
V = Λ⁴[1 − cos(φ/F)]ⁿ) is identical to CAMB's built-in `EarlyQuintessence` model,
V = m²f²[1 − cos(φ/f)]ⁿ. So the test uses CAMB, the Boltzmann code used by the Planck collaboration,
and Cobaya, the standard sampler, with no custom physics code.

| Setting | Value |
|---|---|
| Model | EarlyQuintessence, n = 3; free: f_EDE(z_c), log10 z_c ∈ [3, 4.3], θ_i ∈ [0.1, 3.1] |
| Cosmology | ω_b, ω_c, 100θ\* (exact `thetastar`, not the cosmomc approximation), ln10¹⁰A_s, n_s, τ; Σm_ν = 0.06 eV |
| CMB | Planck 2018: low-ℓ TT, low-ℓ EE, high-ℓ TTTEEE (plik-lite), lensing |
| BAO | DESI DR2, all tracers (`bao.desi_dr2.desi_bao_all`) |
| SNe | Pantheon+ (`sn.pantheonplus`); with SH0ES: `sn.pantheonplusshoes` |
| Runs | ΛCDM and torsion EDE, each without and with SH0ES |

## Steps (Windows)

1. `SETUP_CMB_FIT.bat` — makes a private Python environment in this folder, installs CAMB + Cobaya,
   **validates CAMB against its own documented example (H0 = 73.2113)**, downloads the likelihood
   data, and times one full evaluation.
2. `RUN_CMB_FIT.bat` — the four best fits (hours; low priority, 2 threads). Resumable.
3. Results: `results/REPORT.md` (Δχ² and ΔAIC of torsion EDE vs ΛCDM, H0, f_EDE) and `results/*.json`.

Optional afterwards: `venv\Scripts\python cmbfit.py mcmc` for full posterior chains (one to several days).

## How to read the outcome (decided in advance)

* The torsion field earns a claim only if, **without SH0ES**, ΔAIC (EDE − ΛCDM) < 0, i.e. it improves the
  fit by more than its 3 extra parameters cost, and the best-fit H0 moves toward 73.
* If ΔAIC ≥ 0 without SH0ES, the honest statement is: the model is allowed by the data but not preferred.
* With SH0ES, any improvement mostly reflects absorbing the SH0ES prior; report it, but don't lead with it.
* Published comparison: Poulin, Smith, Calderón & Simon 2025 (arXiv:2505.08051) find f_EDE ≈ 0.09 and
  H0 ≈ 72 with Planck + ACT DR6 + DESI DR2 (profile likelihood, no SH0ES).

## Caveats

* CAMB's own docs note EarlyQuintessence is "not as well tested as most of the rest of CAMB"; the
  validation step checks it reproduces the documented result.
* Plik-lite marginalizes Planck foregrounds assuming ΛCDM-like spectra; this is standard for quick EDE
  tests, but a final paper should repeat the fit with the full plik or NPIPE CamSpec likelihoods.
* Best fits in EDE are known to be harder to find than in ΛCDM (`best_of: 2` restarts are used).
