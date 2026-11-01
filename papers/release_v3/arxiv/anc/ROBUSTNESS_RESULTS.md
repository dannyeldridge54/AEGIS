# Robustness results (post-hoc; the official verdicts do not change)

**Pre-registrations:** PREREGISTRATION_ROBUSTNESS.md (R1, R2) and PREREGISTRATION_DOVEKIE.md (the bracket, locked
09:56:48). **Engine:** AxiCLASS, same data and settings as A3, except the supernova set.

## A3 (early alongside late) across supernova sets

D = χ²(early + late) − χ²(late only). The bands: SURVIVES if D < −4; NOT NEEDED if D ≥ −1; MILD in between.

| Supernovae | D | Band | Late gain (w0–wa vs ΛCDM) | Early + late fit |
|---|---|---|---|---|
| Pantheon+ (official A3) | −3.65 | **MILD** | −10.95 (DESI DR2: −10.7) | f 0.069, H₀ 69.40 |
| DES Y5 (original) | −4.70 | **SURVIVES** | −20.67 (DESI DR2: −21.0) | H₀ 68.54 |
| **DES-Dovekie (corrected DES)** | **−2.70** | **MILD** | **−14.20** | f 0.063, θ_i 2.73, H₀ 69.02; w0 −0.815, wa −0.628 |

**Reading:**
- **Early energy reaches SURVIVES only with the uncorrected DES Y5 sample,** which has a reported calibration offset of
  about 0.04 mag (Efstathiou). With the corrected Dovekie sample, and with Pantheon+, it is **MILD**.
- **So A3 is fragile,** and its strongest form rests on the sample with a known systematic. The early hint persists
  (f ≈ 0.06–0.07 in every case) but does not earn its two parameters with corrected supernovae.
- **The late signal is robust in every set** (−11 to −21), and our values match DESI's.
- **Dovekie's late-only fit (w0 −0.824, wa −0.643) agrees with DES's own Dovekie + CMB + DESI result** (w0 = −0.803 ±
  0.054, wa = −0.72 ± 0.21).

**Expectation, written before the fit, against the result:**

| | Expected | Result |
|---|---|---|
| Late gain | −12 to −17 | **−14.20** ✓ |
| D | MILD, near −4 | **MILD, but −2.70**: weaker than expected |

**Convergence note:**
- The two restarts of the Dovekie early + late fit ended 2.58 apart in χ²; the lower is used, as the rule says.
- A third restart could only lower χ²(early + late), which would make D more negative. Even the 2.6 spread would leave
  D above −4 unless χ²(late only) were also overestimated, so MILD is very likely robust.
- The same caution applies to every best-of-2 fit (see R1).

## R1: minimiser stability of A3 (best of 4)

- `ax_spa_w0wa_b4`: 0.37 *worse* than the original, so the original minimum stands.
- `ax_spa_edelock_w0wa_b4`: **0.31 better** than the original (the four restarts span 2.8 in χ²).
- **D_best = −3.96: band MILD, the same as A3, so R1 is STABLE.** It sits **0.04 from the SURVIVES line.**

**What R1 says about the minimiser:**
- Restart spreads of about 2.6–2.8 in χ² appear in both the Dovekie and R1 early + late fits.
- The best of several restarts moves the answer only by about 0.3, but the verdict sits right at a band edge.
- **The honest statement is "MILD, at the edge of SURVIVES" with Pantheon+, and clearly MILD with Dovekie.**

## Filter rule (ranking §4)

- **R1:** STABLE.
- **R2 with DES Y5:** CHANGES to SURVIVES.
- **Dovekie:** MILD.
- **So A3 is FRAGILE by the filter rule.** It is MILD with every corrected supernova set, and reaches SURVIVES only with
  the uncorrected DES Y5 sample.

## R2: the Late Twist with DES Y5

The (F, m) grid is running (deviation at 08:58). It is reported when complete.
