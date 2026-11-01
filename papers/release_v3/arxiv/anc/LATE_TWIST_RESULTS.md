# Late Twist results (PREREGISTRATION_LATE_TWIST.md), with a minimiser failure flagged

**Run:** `ax_spa_latetwist`, rerun with the minimiser guard (deviation logged 07:24 CT, commit 8c2c095). It finished on 1 November 2026
at 07:41 CT.

**References:** `ax_spa_lcdm_halofit` and `ax_spa_w0wa_halofit`, as set by the halofit deviation.

## Verdicts, applied exactly as written

| Test | Number | Verdict |
|---|---|---|
| L1 (vs ΛCDM) | Δχ² = +11.64, ΔAIC = +15.64 | **FAIL** |
| L2 (vs w0–wa) | D = +21.60 | **WORSE** |
| L3 (natural range) | F = 0.536 M_Pl, m = 2.04 H₀ | **CONSISTENT** (a weak test; not at a prior edge) |
| Shared F (PREREGISTRATION_SHARED_F.md) | F_late / F_early = 3.69 (R = +0.57) | **DIFFERENT** |

**Reported beside the verdicts:**
- **The fit's own values:** H₀ = 67.00, S8 = 0.779.
- **The field at the best fit:** w today = −0.922, CPL-equivalent w0 = −0.935, wa = −0.103 (fit residual ≤ 0.013).

## Why these verdicts do not test the model: the minimiser did not find the minimum

A post-hoc diagnostic (`axiclass/probe_corner.py`) evaluated χ² with the cosmological and calibration parameters held at
the ΛCDM (halofit) best fit:

| (F, m) | χ² | vs ΛCDM |
|---|---|---|
| Late Twist best fit (0.54 M_Pl, 2.04 H₀) | **2402.66** | +0.40 |
| (3.16 M_Pl, 0.50 H₀), near the ΛCDM-like corner | 2402.64 | +0.38 |
| (3.16 M_Pl, 1.00 H₀) | 2409.62 | +7.36 |
| (3.16, 0.32) and (2.00, 0.32) | ∞ | closure impossible |

**What this shows:**
- At the reported best-fit F and m, simply moving the other parameters to the ΛCDM best fit gives χ² = 2402.66.
  That is **11.24 lower than the minimiser's "best fit"** of 2413.90.
- Both bobyqa restarts reported "converged", but to a poor point. The guarded landscape (flat penalties around the
  region where the closure is impossible) most likely stalled the trust region.
- **So the official L1 and L2 verdicts stand as judged, but they reflect a minimiser failure, not the model.** The
  diagnostic points show the model reaches at least χ² ≈ ΛCDM + 0.4 without any optimisation of the other parameters.
  The true minimum is lower still.
- The probe also shows that the prior's corner (m ≥ 0.32 H₀ with F ≤ 3.16 M_Pl) cannot reach a fully frozen,
  ΛCDM-like field. The nearest viable point (F = 3.16, m = 0.5) costs +0.38 before refitting.

**What a valid test needs (a deviation, which needs the author's OK because the result has been seen):**
- Rerun `ax_spa_latetwist` with the cosmological references centred on the ΛCDM halofit best fit, and best of 4.
- Same priors and rules. The failed run stays on record.
- The same fix would apply to `ax_spa_latetwist_desy5` before robustness batch 2 starts.

**Shared F:** DIFFERENT either way. The two diagnostic points that fit well have F between 0.5 and 3.2 M_Pl, all more
than 3 times F_early = 0.145 M_Pl, unless a refit lands below 0.48 M_Pl.

**Post-hoc observation (not a test):** the construction's natural scale is s = √(3/2) M_Pl = 1.22 M_Pl. I meant to
pre-register "F_late = s", but the fit finished before I could, so it is reported only as a note: the current
(unreliable) best fit F = 0.54 is 0.44 s.

## Rerun (approved; AxiCLASS ΛCDM start, best of 4; finished 1 November 2026)

All 4 restarts reported "converged", at −log posterior 1172.42, 1171.26, 1174.20 and 1170.79: a spread of 6.8 in χ².

**Verdicts, applied exactly as written:**

| Test | Number | Verdict |
|---|---|---|
| L1 (vs ΛCDM) | Δχ² = +3.23 (χ² 2405.49) | **FAIL** |
| L2 (vs w0–wa) | D = +13.18 | **WORSE** |
| L3 (natural range) | F = 1.02 M_Pl, m = 1.20 H₀ | **CONSISTENT** (weak test; not at a prior edge) |
| Shared F | F_late / F_early = 7.0 | **DIFFERENT** |

**Reported beside them:** H₀ = 67.25, S8 = 0.783.

**The minimiser is still stuck** (corner probe, as the loop rules require). At the rerun's own best (F, m), with the other
parameters moved to the ΛCDM halofit best fit, χ² = 2402.94, which is **+0.68** above ΛCDM, against the reported +3.23.
Near the ΛCDM-like corner (F = 3.16, m = 0.5) it is **+0.38**. So:
- the true minimum is at most +0.38, and refitting the other parameters can only lower it;
- whether it falls **below** ΛCDM, which would turn L1 from FAIL into INCONCLUSIVE or better, is not yet known;
- the published thawing-quintessence results suggest a modest gain of order −3 is possible.

**What would settle it** needs the author's OK, because the result has been seen:
- start the minimiser *at* the probe point, with the 13 parameters set there, using smaller initial steps for F and m;
- or switch the Late Twist to a different minimiser (scipy) that copes better with the guarded landscape.

**Meanwhile, the official verdicts stand as written.** Robustness batch 2 (the Late Twist with DES Y5) uses the same
settings, so it may stall the same way.