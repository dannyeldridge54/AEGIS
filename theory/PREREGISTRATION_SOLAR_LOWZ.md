# Pre-registration: solar-system gate (SSG) for the Spiral Twist, and low-redshift split (LZ) of the Late Twist hint

**Locked:** 2026-11-02 15:17:31
**Written** before any number below was computed. Path: PATH_DECISION_2026-11-02.md, steps 2 and 4 (gate part only).

## SSG. Can the BI dilaton exist without breaking solar-system gravity?

**Setup (fixed):** Gates, Ketov & Yunes (arXiv:0906.4978) eqs. 5.36–5.37: Ω = e^{Φ+Φ̄}(Φ+Φ̄), K = −3 ln(−Ω/3),
Φ = ϕ + i a, ϕ < 0. Reduced Planck units.

- **Reading A (main):** matter couples to the frame in which Ω multiplies R (the supergravity Jordan frame). The
  Einstein-frame metric is g_E = (−Ω/3) g_J, so matter feels A(χ)² = −3/Ω, with χ the canonical dilaton
  (χ = √(3/2) ln|ϕ|, from bi_kahler_lambda.py).
- **Coupling:** α(χ) = √2 · d ln A/dχ (Damour–Esposito-Farèse normalisation). PPN: γ − 1 = −2α²/(1 + α²).
- **Bound:** Cassini |γ − 1| < 2.3×10⁻⁵.

**Computed (sympy, `solar_lowz.py`):** α(χ); every field value where α = 0 (a "GR point"); d²ln A/dχ² there; the
band |Δχ| around the GR point allowed by Cassini.

**Verdict (Reading A):**
- **EXCLUDED** if no field value meets the Cassini bound.
- **FINE-TUNED** if the bound is met only within a band |Δχ| < 0.01 and the GR point is not an attractor
  (d²ln A/dχ² ≤ 0).
- **ATTRACTOR-PROTECTED** if a GR point exists and is a cosmological attractor (d²ln A/dχ² > 0; Damour–Nordtvedt).
  The allowed band is reported. The consequence is stated: the dilaton must sit near the GR point today, so the
  dark-energy roll must come mainly from the axion angle, and the kinetic mixing acts through a nearly frozen dilaton.
- **Reading B** (matter couples to the Einstein frame): coupling zero by construction. This is reported as an extra
  assumption, not a pass.

**Expectation (not a rule):** ATTRACTOR-PROTECTED or FINE-TUNED; a dilaton–gravity coupling of order one is the
standard problem (cf. arXiv:2512.13544).

## LZ. How much of the Late Twist's DES Y5 supernova gain comes from z ≤ 0.1?

**Points (fixed, no refit):** the stored best fits `cmp_ax_spa_latetwist_gF0m0.102_desy5_nlfix` and
`cmp_ax_spa_lcdm_halofit_desy5`, rebuilt from their `.minimize.updated.yaml` in the aegis environment.

**Method:**
- From the Cobaya `sn.desy5` likelihood's own data (z_cmb, z_hel, magnitudes, full covariance), compute the
  supernova χ² with the same analytic marginalisation over the absolute magnitude that the likelihood uses.
- **Mirror (must pass first):** the recomputed full-sample χ²_SN must match the stored `chi2__SN` within 0.05 for
  both points. If not, stop and report; no verdict.
- **Split** at z_cmb = 0.1. Each subset uses its own sub-covariance and its own marginalisation over the absolute
  magnitude.
- Δ_full = χ²_SN(Twist) − χ²_SN(ΛCDM) on all supernovae; Δ_high and Δ_low the same on z > 0.1 and z ≤ 0.1.
- r = Δ_high / Δ_full.

**Verdict:**
- **CALIBRATION-SENSITIVE** if r < 0.5: less than half the gain survives without the low-redshift supernovae.
- **MIXED** if 0.5 ≤ r < 0.8.
- **ROBUST TO LOW-Z** if r ≥ 0.8.

**Caveats fixed in advance:**
- No refit: parameters stay at the full-data best fits (as in Zhang 2026, which refits; ours is the cheaper
  version).
- The split sums need not add to Δ_full, because the covariance couples the subsets and each subset has its own
  absolute magnitude. Both pieces are reported.

**Expectation (not a rule):** CALIBRATION-SENSITIVE (Zhang, MNRAS 552; Huang et al. arXiv:2502.04212).
