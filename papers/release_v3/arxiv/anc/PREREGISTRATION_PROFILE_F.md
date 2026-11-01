# Pre-registration: profile likelihood in the early-energy fraction f_EDE on all CMB data combined

**Written:** 2026-10-31 21:12 CT (time from the clock), before any fixed-f fit on the combined data was written or run.
**Why:** the combined pass (Delta chi^2 -5.63) is a best fit. When f = 0 the angle theta_i means nothing, so the usual
translation of Delta chi^2 into sigma is unreliable. Best-fit EDE results also suffer from prior-volume effects. The
profile likelihood is the field's standard answer, and it gives an allowed range to compare with the SPT-3G team's
f_EDE < 0.070 (95%).
**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Runs

Locked Twist on Planck + ACT + SPT-3G + DESI DR2 + Pantheon+, exactly as `spa_edelock` (n = 3, onset locked, best of
4), with f_EDE fixed at:

0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12 (runs `spa_edelock_fde<value>`).

theta_i and all other parameters are refitted at each point. Also used: `spa_edelock` (free f, chi2 2396.77) and
`spa_lcdm` (f = 0, chi2 2402.40).

## What is reported

- The profile: chi2_min(f) - chi2_min over all f, including the f = 0 point (LCDM).
- **The 68% and 95% ranges for f:** where the profile rises 1 and 3.84 above its minimum (Wilks, one parameter),
  interpolated on the grid.
- **The profile significance:** sqrt(chi2(f = 0) - chi2_min).

## Rule

| Outcome | Rule |
|---|---|
| **Early energy preferred** | f = 0 lies outside the 95% range (profile rise > 3.84 at f = 0) |
| **Not preferred** | the rise at f = 0 is below 1 |
| **Mild** | anything in between |

**Comparison:** state plainly whether our 95% upper end agrees with the SPT-3G team's f_EDE < 0.070 (posterior), allowing
for the known difference between profiles and posteriors.

**Caveat, written in advance:** Wilks' thresholds assume regular conditions. f = 0 is on the boundary and theta_i is
undefined there, so these ranges are approximate. The simulated-sky check (ROUTE.md A2) is the full calibration.
