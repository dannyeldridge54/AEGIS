# Pre-registration: robustness of A3 and the Late Twist (DEEP_REVIEW_2026-11-01.md, points B and E)

**Written:** 2026-11-01 07:12 CT (time from the clock). A3 results were already known when this was written: they are
in EARLY_LATE_RESULTS.md, so **these checks are post-hoc**, and are labelled that way everywhere. No Late Twist result
and no fit below had been run or read.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

**What does not change:** the official A3 verdict (MILD) and the Late Twist verdicts stand as judged under their own
pre-registrations. These checks only report how stable those verdicts are.

**Engine and settings:** AxiCLASS, same as PREREGISTRATION_EARLY_LATE.md and PREREGISTRATION_LATE_TWIST.md (bobyqa,
CAMB-start references, same priors and calibrations), unless a line below says otherwise.

## R1: minimiser stability of A3 (review point B)

**Runs:** `ax_spa_w0wa_b4` and `ax_spa_edelock_w0wa_b4`. These are the same two models as A3 with **best of 4**
restarts instead of 2.

**Method:**
- For each model, take the lower χ² of the original A3 run and the b4 run: the best minimum found.
- D_best = χ²_best(early + late) − χ²_best(late only).
- Both models get the same extra effort, so the comparison stays fair.

**Bands** (the same as A3):
- SURVIVES: D < −4 and D + 4 < 0.
- NOT NEEDED: D ≥ −1.
- MILD: in between.

**Report:**
- **STABLE** if D_best falls in the same band as A3 (MILD).
- **SHIFTED to <band>** otherwise.
- The scatter between restarts for each model.

## R2: supernova dependence (review point E)

**Runs:** Pantheon+ is replaced by **DES Y5** (`sn.desy5`); everything else is unchanged (best of 2, as in A3 and the
Late Twist).
- `ax_spa_lcdm_desy5`, `ax_spa_w0wa_desy5`, `ax_spa_edelock_w0wa_desy5` (A3 with DES Y5);
- `ax_spa_latetwist_desy5`, `ax_spa_lcdm_halofit_desy5`, `ax_spa_w0wa_halofit_desy5` (Late Twist with DES Y5,
  halofit references as in its deviation).

**Bands:**
- **A3 with DES Y5:** D_Y5 = χ²(edelock_w0wa_desy5) − χ²(w0wa_desy5), judged in the A3 bands. Also reported: the late
  gain χ²(w0wa_desy5) − χ²(lcdm_desy5) against the Pantheon+ value (−10.95).
- **Late Twist with DES Y5:** the L1 and L2 bands of PREREGISTRATION_LATE_TWIST.md, applied to the _desy5 runs. L3
  (natural range) is reported for the best-fit F and m.

**Report for each test:**
- **SAME** if the band matches the Pantheon+ result.
- **CHANGES to <band>** otherwise.

**Expectation, written in advance:** DESI found the late signal stronger with DES Y5 than with Pantheon+, so the late
gain should grow. How the early term responds is not predicted.

## Order and cost

1. These runs start after the three Late Twist fits finish.
2. R1 (2 fits) and the A3 part of R2 (3 fits) run first, 3 threads each.
3. The Late Twist part of R2 (3 fits) runs next, 5 threads each.

About 2–4 hours in all. If a fit crashes only while saving, it is recovered from Cobaya's minimum file (`save` mode),
and this is logged.
