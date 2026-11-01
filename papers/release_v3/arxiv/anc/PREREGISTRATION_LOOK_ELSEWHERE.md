# Pre-registration: how significant is the combined-data Twist preference, after the look-elsewhere effect? (ROUTE.md A2)

**Written:** 2026-10-31 21:39 CT (time from the clock), before any fixed-angle combined run was written, queued or run.
**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Why this method instead of full simulated skies

The combined Twist result (Delta chi^2 = -5.63) was turned into ~1.9 sigma using a chi^2 distribution with 2 degrees of
freedom. That is not valid here:
- when f_EDE = 0, the angle theta_i has no meaning (the Davies / look-elsewhere problem);
- f_EDE >= 0 is a boundary.

Full simulated skies (fake data for all six likelihoods, both models fitted to each) would cost about 100 hours for 50
skies, so they are deferred. Instead this uses the standard asymptotic method of **Gross & Vitells (Eur. Phys. J. C 70,
525 (2010))**, as used for the Higgs discovery.

## Runs

The Locked Twist on Planck + ACT + SPT-3G + DESI DR2 + Pantheon+, as `spa_edelock` (n = 3, lock, best of 4), with
theta_i **fixed** and f_EDE free:

theta_i = 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 2.9, 3.05 (runs `spa_edelock_th<value>`).

## Calculation (rule)

1. **Local statistic.** At each fixed angle: q(theta) = max(0, chi2(spa_lcdm) - chi2(spa_edelock_th<theta>)). With
   chi2(spa_lcdm) = 2402.40, q >= 0 because f >= 0 nests LCDM. Also include the free-angle fit spa_edelock (q = 5.63
   at theta = 2.741).
2. **Local p-value.** For fixed theta, under LCDM, q follows a half chi^2_1 (boundary): p_local(u) = 0.5 * P(chi^2_1 > u).
   Report the maximum q, u = q_max, and its p_local and Z_local.
3. **Upcrossings.** Linearly interpolate q(theta) on the grid, extended to theta = 0.1 and 3.1 with q -> 0 at
   theta -> 0.1 (where the field barely moves). Count the upcrossings N0 of the reference level u0 = 0.5, and also
   u0 = 1.0 as a check.
4. **Global p-value** (Gross-Vitells, 1 degree of freedom): p_global = p_local(u) + N0 * exp(-(u - u0)/2). Report
   Z_global for both u0 values; the larger p is quoted as the conservative answer.

## Verdict bands (on the conservative Z_global)

| Z_global | Verdict |
|---|---|
| >= 2 | Mild evidence survives the look-elsewhere correction |
| 1 to 2 | A weak hint |
| < 1 | Consistent with noise |

**Stated plainly beside it:** the earlier "1.9 sigma" was an upper estimate, and how much it shrinks.

**Caveats, written in advance:**
- The method is asymptotic.
- N0 comes from one realisation, the data themselves, and is noisy.
- The 8-point grid can miss narrow structure.
- The full simulated-sky check stays on the route for later.
