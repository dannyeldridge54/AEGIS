# Pre-registration S8-J: the Spiral refit with weak lensing inside the fit

**Locked:** 8 Nov 2026, time in `PREREG_S8_JOINT.md.sha256` (UTC), by Claude at Danny's request ("Set them all up to be
run today"), with the recommended choices: DES Y6 inside the fit, SF thresholds. AI-assisted. No S8-J fit exists at lock.

**Not blind, stated plainly.** At writing time we already know S8-WL Part 1 and Part 2, and the expected joint χ² at
the stored SF best fits (`field_tests/S8_WL/joint/s8j_gate.json`): Spiral minus ΛCDM is −5.06 / −6.57 / −5.91 with the
S8 term added but **no refit**. The refit can move both models. This rule fixes only how the refit is done and read.

## Question
With the newest cosmic-shear S8 inside the fit, does the Spiral still beat ΛCDM, and how much supernova/CMB fit does it
give up to match lensing?

## Model and engine (fixed)
- The Spiral exactly as SF (`PREREGISTRATION_SPIRAL_FIT.md`): κ ∈ [0.05, 3], β_eff ∈ [0, 0.12], coupled B0-fixed
  AxiCLASS build, halofit, same CMB + DESI DR2 + one SN set (Pantheon+, DES-Dovekie, Union3), same priors, same
  starting points, best of 4. ΛCDM reference: `ax_spa_lcdm_halofit[_dovekie|_union3]`, same treatment.
- **One added likelihood:** DES Y6 cosmic shear, −2 ln L = ((S8 − 0.798)/σ)², σ = 0.014 above, 0.015 below
  (arXiv:2602.10065, as S8-WL Part 1). S8 = σ8 √((ω_b + ω_cdm + ω_ν)/h²/0.3), as `s8wl_score.py`.
- Code: `field_tests/S8_WL/joint/s8_joint_fit.py` (wraps the SF fitter unchanged). Run names `<SF run>_s8y6` (6 fits, PC).

## Gate (before any fit)
G-J: through the full fitter, at each stored SF best fit, total χ² = stored χ² + χ²_S8 within 0.05
(`python s8_joint_fit.py gate_pc` → `results/s8j_gate_pc.json`). If not: no fits, no verdict.

## Verdicts (per SN set s; both models fitted with the S8 term)
- **Against ΛCDM:** Δ_s = χ²(Spiral+S8) − χ²(ΛCDM+S8). **SURVIVES LENSING** if Δ ≤ −4 on at least 2 of 3;
  **TIE** if none ≤ −4 and none ≥ +2; otherwise **MIXED** (the SF thresholds).
- **Reported, not verdicts:** the lensing cost C_s = [χ²_noS8(Spiral+S8) − χ²(Spiral SF)] − [same for ΛCDM];
  β_eff, κ and S8 at each joint best fit; the S8-WL Part 2 full DES Y3 Δ_WL rerun at the joint best fits.
- **Failures:** a failed or non-finite fit is NO VERDICT for that set; any settings change is logged first.

## Choices made at lock
1. Lensing number inside the fit: DES Y6 (newest, same as Part 1).
2. Thresholds: the SF thresholds.
