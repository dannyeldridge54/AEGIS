# SELFCHECK: verifying the flagship's evidence, and the probes not yet tried

**Status: LOCKED** on Danny's word ("Get these all planned and scheduled", 11 Nov 2026, 10:01 CT). He was answering
a proposal that listed these checks. Time and fingerprint are in the .sha256 file. AI-assisted.

**Not blind.** Known at writing:
- FLAG-1 vs ΛCDM+S8: Δχ² −4.71 / −6.01 / −7.69 (local 2.2–2.8σ by Wilks, k = 1).
- Global 0.2–1.0σ after the V7 statistic (N = 66; exploratory).
- Both full-shear passes.
- The cluster S8 values and the Planck coupled-DE result quoted below.

V4 and V5 are arithmetic on numbers already known, so they are **reported checks, not tests**. The rule only fixes
how they are reported.

Frozen inputs (no refit under this rule, except the V2 fits it defines):
- the FLAG-1 fits and ΛCDM+S8 partners listed in `PREREG_LENSING_FORECASTS_FLAG1.md`;
- `theory/fpc_ax_spa_spiraltwist_kappa1*_s8y6.json` (fσ8, σ8).

## V1: fake-universe calibration of the local significance (cloud)

**Why.** At β = 0 the flagship is not ΛCDM: with κ = 1 it is still a rolling exponential field. FLAG-1 vs ΛCDM is
therefore not a nested comparison, and β has a boundary at 0. Wilks' χ²₁ is not guaranteed. This measures the real
chance rate.

**Mock data.**
- Data: DESI DR2 BAO (ALL covariance) + Pantheon+ (STAT+SYS, z > 0.01, non-calibrators, M marginalised analytically)
  + compressed CMB (100θ*, ω_b, ω_b + ω_c; σ = 0.00030 / 0.00015 / 0.0011). This is the same compressed likelihood as
  `PREREG_DESI_MOCK.md`.
- Truth: the ΛCDM+S8 Pantheon+ partner's best fit (`cmp_ax_spa_lcdm_halofit_s8y6`).
- Noise: Gaussian, from the same covariances. Seeds are 1..N_mock.

**Fits.** On each mock, fit ΛCDM (h, ω_b, ω_c) and FLAG-1 (h, ω_b, ω_c, β_eff ∈ [0, 0.12], κ = 1).
- Engine: background only, the coupled build for both, ΛCDM via its Λ settings.
- Optimiser: Nelder–Mead, best of 3 starts. ΛCDM starts: the truth and two offsets. FLAG-1 starts: the same three
  points with β = 0.01 / 0.04 / 0.08.
- Statistic: Δ = χ²(FLAG-1) − χ²(ΛCDM).
- N_mock = 200 target. At least 100 must finish for a reading; the number finished is reported.

**Real-data anchor.** The same two fits on the real data, through the same compressed likelihood, give Δ_real.

**Readings.**
- p_emp = fraction of mocks with Δ ≤ Δ_real, with its binomial 68% interval. This is compared with p_Wilks = P(χ²₁ ≥ −Δ_real).
- **WILKS ADEQUATE:** p_emp within a factor 2 of p_Wilks.
- **WILKS OVERSTATES:** p_emp > 2 p_Wilks. The local σ is lower than quoted.
- **WILKS UNDERSTATES:** p_emp < p_Wilks / 2. The local σ is higher than quoted.

**Also reported:**
- the empirical local σ;
- the global σ recomputed with p_emp and V7's N = 66;
- the share of mocks with β at the 0 boundary.

**Limitation (stated):** background-only and compressed CMB. It calibrates the shape of the Δ distribution, not the
full-likelihood Δ.

## V2: the flagship without supernovae (PC)

**Fits.** FLAG-1 (κ = 1, β free) and ΛCDM, each refit with every supernova likelihood removed. Everything else is
exactly as the stored s8y6 fits: same CMB, DESI DR2 BAO, DES Y6 S8 term, priors, build and best of 4.
- Starts: each from its own stored Pantheon+ s8y6 minimum.
- Names: `ax_spa_spiraltwist_kappa1_nlfix_nosn_s8y6` and `ax_spa_lcdm_halofit_nosn_s8y6`.
- Runs only after the DESI-MOCK-CMB fits have finished on the PC.

**Readings.** Δ_noSN = χ²(FLAG-1) − χ²(ΛCDM):
- **PREFERENCE SURVIVES WITHOUT SNe:** Δ_noSN ≤ −4.
- **SN-DRIVEN:** Δ_noSN > −2.
- **WEAK:** otherwise.

β_eff, H0, S8 and the per-likelihood χ² of both fits are reported.

## V3: DESI DR1 full-shape growth (cloud; a test on existing data, not a forecast)

**Data.** DESI DR1 full-shape ShapeFit compressed results (arXiv:2411.12021, Appendix A): the fσ_s8 entry for each of
the six tracers (BGS, LRG1, LRG2, LRG3, ELG2, QSO).
- Covariance: the marginal fσ_s8 variances from each tracer's printed SF+BAO covariance. Tracers are treated as
  independent, as DESI's compressed likelihood does.

**Predictions.** Computed from the frozen FLAG-1 best fits and their ΛCDM+S8 partners. The fσ_s8 definition is
followed exactly as the paper states it, including its σ_s8 smoothing scale and the fiducial template. That
conversion is written into the scorer, with the equation number quoted, **before any χ² is computed**.
- If the paper does not give enough to reproduce fσ_s8 exactly, V3 is reported as NO VERDICT.
- In that case no substitute statistic is chosen afterwards.

**Readings (Pantheon+ fit primary; all three reported).** χ²_FS for FLAG-1 and for ΛCDM, 6 points, no free
parameter.
- **CONSISTENT:** p ≥ 0.01.
- **FAIL:** p < 0.001.
- Otherwise **TENSION**.

Δχ²_FS = FLAG-1 − ΛCDM is reported for scale.

## V4: cluster counts (reported check, cloud)

Test A form, as in `PREREG_LENSING_FORECASTS.md`: ΔP = penalty(FLAG-1) − penalty(ΛCDM), using each survey's quoted
S8 and 1σ.
- eROSITA eRASS1 (arXiv:2402.08458): S8 = 0.86 ± 0.01.
- SPT clusters (Bocquet et al. 2024): S8 = 0.795 ± 0.029, value checked against the paper before scoring.

**Readings.** PASSES if ΔP ≤ +2, per survey. The two surveys disagree with each other, and both are reported.

## V5: dark-matter fifth force (reported check, cloud)

A coupling β gives dark matter an extra attraction G_eff/G − 1 = 2β² in the convention m_c ∝ e^(βφ) (as `spiral_guess.py`), with φ in
reduced Planck units. The scorer states the convention and maps it to each reference's convention.

Compared with:
1. Planck + BAO coupled dark energy (arXiv:1305.7457): β = 0.036 ± 0.016, convention Q = −β ρ_c φ′. Reading: FLAG-1's
   β_eff within 2σ of it, or beyond.
2. Tidal-stream and cluster limits on a dark-sector fifth force: values and conventions taken from the papers and
   quoted with their sources.

**Reading.** PASSES if FLAG-1's G_eff is inside every quoted bound; otherwise FAILS, naming the bound.

## Not in this rule
- **V6, Planck PR4 robustness refit:** needs a Planck PR4 likelihood download, which requires Danny's permission
  first. It gets its own rule.
- **Bayes factor from the MCMC:** dropped. FLAG-1 at β = 0 is not ΛCDM, so a Savage–Dickey ratio would compare FLAG-1
  with exponential quintessence, not with ΛCDM. A proper evidence needs nested sampling (expensive). It is not
  scheduled.

## What may not happen
- No change of truth, mock count, starts, data, bands or conversions after any result.
- No dropping of a part because of its result.
- Each part is reported once, whatever it gives.
- Deviations are logged before any rerun.
- Counted +1 in V7, as a single test.
