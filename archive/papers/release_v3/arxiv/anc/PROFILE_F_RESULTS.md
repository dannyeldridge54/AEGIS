# A1: profile likelihood in f_EDE on all CMB data combined (PREREGISTRATION_PROFILE_F.md)

All seven points finished on 1 November 2026, by about 02:30 CT. Data: Planck (P-ACT) + ACT DR6 + SPT-3G D1 lite + DESI
DR2 + Pantheon+. Locked Twist, n = 3, f_EDE fixed, everything else refitted (CAMB, best of 4).

| f_EDE | χ² − χ²_min |
|---|---|
| 0 (ΛCDM) | +5.98 |
| 0.01 | +4.51 |
| 0.02 | +3.24 |
| 0.04 | +1.57 |
| 0.06 | +0.26 |
| **0.08** | **0 (minimum, χ² = 2396.42)** |
| 0.10 | +0.81 |
| 0.12 | +2.66 |
| free fit (f = 0.070) | +0.35 |

## Verdict (rule applied as written)

- **Rise at f = 0: 5.98 > 3.84, so early energy is PREFERRED.** The profile significance is √5.98 ≈ 2.4σ.
- **68% range** (rise 1): f_EDE ≈ 0.049–0.102.
- **95% range** (rise 3.84): f_EDE ≈ 0.015 to beyond 0.12, the grid edge. A 0.14 point would close it.

## Notes beside the verdict

- **The free fit missed its best point by 0.35.** The f = 0.08 point beats it. That is below the 0.5 the rule flags,
  but it confirms the reviewer's concern about minimiser scatter. The true best fit is near f ≈ 0.08, with Δχ² ≈ −5.98
  against ΛCDM.
- **Comparison with the SPT-3G collaboration's posterior** for the same CMB data (f_EDE < 0.070 at 95%): our profile
  prefers *more* early energy (best 0.08, 68% range 0.05–0.10).
  - This is the known profile-versus-posterior difference for EDE: posteriors are pulled towards f = 0 by the prior
    volume of the angle and critical-redshift parameters.
  - Our analysis also adds DESI and Pantheon+, and locks the onset.
  - The two are not in direct conflict, but they read differently, and that should be stated.
- **Wilks thresholds are approximate here** (f = 0 is a boundary and θ_i is undefined there). The look-elsewhere
  calibration (A2, PREREGISTRATION_LOOK_ELSEWHERE.md) is the proper correction, and is running now.

**Rounding note (audit, 1 November 2026):** recomputing from the result files gives a rise at f = 0 of **5.988** and a
free-fit gap of **0.357**. The values above (5.98, 0.35) come from the pre-registered reference χ² rounded to two
decimals (ΛCDM 2402.40, free fit 2396.77). The difference is 0.003 and does not change the verdict.