# Pre-registration: all three CMB telescopes together, early vs late new physics

**Written:** 31 October 2026, 18:50 CT. At this time:
- none of the runs below had been written as code, run or queued;
- no combined Planck + ACT + SPT-3G fit of any model existed;
- no fit of evolving dark energy (w0–wa) had been run on any data in this project.

**Authors:** Danny Lee Eldridge, with Claude. Danny asked for both tests; Claude proposed them and wrote the rules.

**Locking:** SHA-256 hashed and git-committed when written. It must not be edited afterwards. Deviations go in
PREREGISTRATION_SPT3G_DEVIATIONS.md with a date.

## Why

On Planck and ACT the Locked Twist is mildly preferred (Δχ² −4.70 and −7.23). On SPT-3G no version is (best −1.27).
DESI DR2 publications report a preference for late-time evolving dark energy. These tests ask, on all the data at
once:
1. does early energy at equality still help;
2. does late-time evolving dark energy help;
3. which of the two does the data prefer?

## Data (one combination, "SPA")

- **Planck + ACT:** P-ACT exactly as in the P-ACT test (`cmbfit_compare._pact`):
  - Planck PR3, cut where ACT takes over;
  - Planck low-ℓ TT and EE (these set τ, so there is no τ prior);
  - ACT DR6 CMB-only;
  - ACT DR6 × Planck PR4 lensing;
  - ACT's calibration prior.
- **SPT-3G D1 TT/TE/EE lite**, as in the SPT-3G tests: the candl likelihood with Tcal and Ecal, Tcal ~ N(1, 0.0036).
- **DESI DR2 BAO + Pantheon+.** No SH0ES.
- **Overlap, disclosed:**
  - The SPT-3G Main field and the ACT DR6 footprint overlap on part of the sky, and the likelihoods are treated as
    independent.
  - The SPT-3G collaboration's own combination with Planck and ACT does the same.
  - This slightly overcounts shared sky; it is accepted and stated here, not corrected.

## Models (each minimised with bobyqa, best of 4, the same settings for all)

| Run | Model | Extra settings k |
|---|---|---|
| `spa_lcdm` | ΛCDM | 0 |
| `spa_edelock` | Locked Twist: onset at equality, f_EDE and θ_i free, width free | 2 |
| `spa_w0wa` | ΛCDM with w(a) = w0 + wa(1 − a) (CAMB PPF); priors w0 in [−3, 1], wa in [−3, 2], w0 + wa < 0 | 2 |

## Rules

**Test 1, the Locked Twist on all CMB data:** Δχ² = χ²(spa_edelock) − χ²(spa_lcdm), ΔAIC = Δχ² + 4.

| Outcome | Rule |
|---|---|
| PASS | Δχ² < −4 and ΔAIC < 0 (the P-ACT rule) |
| FAIL | Δχ² ≥ 0 |
| INCONCLUSIVE | anything in between |

**Test 2, late evolving dark energy:** the same rule for spa_w0wa against spa_lcdm.

**Test 3, early vs late:** compare ΔAIC(spa_edelock) with ΔAIC(spa_w0wa).
- If one is lower by more than 2, the data prefer that one.
- Otherwise, no preference.

**Reported beside the verdicts:** H₀, S8, f_EDE and θ_i (Twist), w0 and wa (w0–wa), and the χ² split by data set.

## Forecast (Claude's, written down so it can be wrong; not part of the rules)

- **Test 1:** INCONCLUSIVE, with f_EDE between 0.02 and 0.06 and H₀ between 68.8 and 69.8.
- **Test 2:** INCONCLUSIVE or PASS, with w0 > −1 and wa < 0, in the direction DESI reports.
- **Test 3:** no preference, or a slight preference for late.

## What each result would mean

- **Test 1 PASS:** early energy at equality survives all three telescopes together. That would be the strongest
  support so far.
- **Test 1 FAIL:** the early-burst Locked Twist is not supported by the combined CMB. The idea would need a different
  form, for example a late-time role for the same field.
- **Late preferred:** the data point to new physics today rather than near equality. Any torsion-field model should be
  rebuilt to act late.
