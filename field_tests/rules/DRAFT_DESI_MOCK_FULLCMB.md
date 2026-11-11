# DESI-MOCK-CMB: the DESI-MOCK test with the full CMB likelihoods (DRAFT, not locked)

**Status: DRAFT** (10 Nov 2026). It runs on the PC after the FLAG-1 MCMC frees the cores. Lock on Danny's word before
any mock fit. AI-assisted.

**Why.** DESI-MOCK (locked, REPRODUCES DESI'S SIGNAL: 2.9σ, w0 −0.833, wa −0.451) used a compressed CMB vector
(100θ*, ω_b, ω_bc). DESI's own result uses the full CMB. This asks whether the reading survives when the CMB enters at
full strength.

## Method (to fix at lock)
- **Truth:** the FLAG-1 Pantheon+ best fit.
- **Mock CMB:** its lensed C_ℓ (TT, TE, EE, φφ) at the stored nuisance values, written in place of the data vectors of
  Planck low-ℓ, P-ACT (Planck cut + ACT DR6 CMB-only), SPT-3G D1 and ACT DR6 lensing. Covariances unchanged.
- **Mock BAO and SN:** DESI DR2 BAO and Pantheon+, as in DESI-MOCK (Asimov).
- **Fits:** ΛCDM and w0waCDM (uncoupled CDM, PPF), Cobaya minimise, best of 4, the CMB nuisances free.
- **Gate:** at the truth point the mock χ² of each CMB likelihood is 0 within 0.01.
- **Readings:** exactly as DESI-MOCK (REPRODUCES at 2σ or more with the crossing signs; PARTIAL 1–2σ; DOES NOT).
- **Reported:** BAO + CMB alone.

## Engineering note
The mock writer needs each likelihood's data-vector format (act_dr6_cmbonly, candl SPT-3G lite, Planck clik-free
lite, ACT lensing). About a day of code, PC only (those likelihoods are not installed in the cloud).
