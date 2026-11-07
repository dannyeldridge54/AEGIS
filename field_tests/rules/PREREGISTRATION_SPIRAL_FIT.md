# Pre-registration: SF, the effective Spiral Twist fit

**Locked:** 2026-11-02 17:01:01
**Written** before any spiral fit exists. Danny, 2 Nov: "Yes, build it" / "finish data".

## Model (fixed in advance)

- **Effective Spiral Twist** (SPIRAL_W_FEASIBILITY.md; theory note doi:10.5281/zenodo.23899237):
  - an exponential dilaton V ∝ e^{−κχ} (κ free in [0.05, 3]);
  - dark matter coupled with m_c ∝ e^{β_eff φ}, β_eff free in [0, 0.12] (the matter-like BI angle,
    β_eff = 0.816 f; the sign is fixed by the geometry).
- **Two dark-energy parameters,** the same count as w0–wa.
- **Code:** the coupled B0-fixed AxiCLASS build, `double_exp` with one exponential (validated against an independent
  solver: w to 2×10⁻⁵, H to 8×10⁻⁵; spiral_class_mirror.json). Run names `ax_spa_spiraltwist[_dovekie|_union3]_nlfix`;
  same likelihoods and settings as every late fit, halofit, best of 4.
- **Data:** CMB (Planck low-ℓ, ACT DR6 + Planck cut, ACT lensing, SPT-3G D1) + DESI DR2 BAO + one supernova sample:
  Pantheon+, DES-Dovekie, Union3. **DES Y5 is excluded** (LZ: CALIBRATION-SENSITIVE).

## Gate (must pass before any fit counts)

Through the full fitter, at the ΛCDM Union3 best-fit standard parameters, the spiral with κ = 0.05, β_eff = 0 must
give a χ² within 1.0 of the stored ΛCDM halofit χ² (`spiral_fit_mirror.json`). If not: no fits, no verdict.

## Verdicts (per sample s; Δ against the existing halofit references on the same data)

- **Against ΛCDM:** Δ_Λ,s = χ²(spiral) − χ²(ΛCDM). **BEATS ΛCDM** if Δ_Λ ≤ −4 for at least 2 of 3 samples;
  **TIE** if no sample is ≤ −4 and none is ≥ +2; otherwise **MIXED**.
- **Against w0–wa (equal parameter count):** Δ_W,s = χ²(spiral) − χ²(w0–wa).
  - **BEATS w0–wa** if Δ_W ≤ −2 on at least 2 of 3;
  - **COMPETITIVE** if Δ_W ≤ +2 on at least 2 of 3;
  - otherwise **NOT COMPETITIVE**.
- **Geometry check (reported, not a verdict):** implied angle share f = β_eff/0.816 at each best fit. If f > 9%, it
  conflicts with the coupled-dark-matter bound (Babu & Amendola, |β| < 0.073). S8 is reported with the coupled-build
  H0-label caveat.
- **Failures:** a failed or non-finite fit counts as NO VERDICT (code-limited) for that sample; any change of settings
  is logged as a deviation first.

## Expectation (not a rule)

TIE or MIXED against ΛCDM; NOT COMPETITIVE with w0–wa. The background study predicts at best a bend of
Δwa ≈ −0.05 to −0.09 at allowed f, which is far from w0–wa's preferred point.
