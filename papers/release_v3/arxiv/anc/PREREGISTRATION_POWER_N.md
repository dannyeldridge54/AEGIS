# Pre-registration: does the combined data need the n = 3 shape?

**Written:** 2026-10-31 21:02 CT (time from the clock). At this time no n = 1 or n = 2 fit on the combined data had been written,
queued or run.
**Why:** STEP2_RESULT.md shows that the shapes geometry or particle physics produce most naturally (an instanton series,
or a chiral potential from an anomaly) have a mass term at the minimum. They behave like n = 1 near the bottom.
The n = 3 shape needs two exact cancellations (sum k^2 a_k = 0 and sum k^4 a_k = 0). So the question is how much the data
penalise n = 1 and n = 2.
**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Runs

The same data and settings as `spa_edelock` (Planck + ACT + SPT-3G + DESI DR2 + Pantheon+, best of 4), with only the
power n changed:

| Run | n |
|---|---|
| `spa_edelock_n1` | 1 |
| `spa_edelock_n2` | 2 |

The reference is `spa_edelock` (n = 3, chi2 = 2396.77) and `spa_lcdm` (chi2 = 2402.40).

## Rule

Let D_n = chi2(spa_edelock_n) - chi2(spa_edelock), the cost of using power n instead of 3. All have the same number of
settings.

| D_n | Meaning |
|---|---|
| D_n < 2 | n = 3 is **not required**: a natural (n = 1 or 2) potential fits about as well |
| D_n > 4 | the data **require** a flat-bottomed potential like n = 3, so geometry must explain two exact cancellations |
| 2 to 4 | not decisive |

Also reported: dchi2 against LCDM for each n, with f_EDE, H0 and theta_i.
