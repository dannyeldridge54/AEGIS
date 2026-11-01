# Pre-registration: the Late Twist (twist field as all of today's dark energy)

**Written:** 2026-10-31 22:00 CT (time from the clock), before any Late Twist fit on any data was written or run. Theory:
LATE_TWIST.md.
**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Model and settings

V = Lambda^4 [1 - cos(phi/F)] (n = 1), no cosmological constant, the field is all the dark energy. The starting angle is
fixed by the energy budget.

| Free | Prior |
|---|---|
| log10(F / M_Pl) | uniform in [-1.3, 0.5] |
| log10(m / H0) | uniform in [-0.5, 1.5] |

That is 2 extra settings over LCDM.

Engine: AxiCLASS, with the same data, calibration priors and fitting as PREREGISTRATION_EARLY_LATE.md (bobyqa, best of
2): Planck low-l + PR3 (ACT cut) + ACT DR6 + ACT x Planck lensing + SPT-3G D1 lite + DESI DR2 + Pantheon+.

Run: `ax_spa_latetwist`. References from the same engine: `ax_spa_lcdm` and `ax_spa_w0wa` (ROUTE A3).

## Rules

**Test L1 (against LCDM):** dchi2 = chi2(ax_spa_latetwist) - chi2(ax_spa_lcdm); dAIC = dchi2 + 4.

| Outcome | Rule |
|---|---|
| PASS | dchi2 < -4 and dAIC < 0 |
| FAIL | dchi2 >= 0 |
| INCONCLUSIVE | anything in between |

**Test L2 (against w0-wa, same settings count):** D = chi2(ax_spa_latetwist) - chi2(ax_spa_w0wa).

| Outcome | Rule |
|---|---|
| Late Twist PREFERRED | D < -2 |
| AS GOOD AS w0-wa | -2 <= D <= 2 |
| WORSE | D > 2 |

**Test L3 (natural range, the twist-specific prediction):** the best-fit F lies in 0.1-3 M_Pl (the range the
Barbero-Immirzi construction gives naturally), and the best-fit mass in 0.5-10 H0.
- CONSISTENT if both hold.
- INCONSISTENT if F < 0.05 or > 3, or m is outside 0.3-30 H0.

**Reported beside the verdicts:** H0, S8, the field's w today and the CPL-equivalent (w0, wa) from the background (a
fit of w(a) over z < 2), and the chi2 split by data set.

## Written in advance

- The phenomenology (quintessence axion) is published (Lin, Visinelli & Yanagida, JCAP 10 (2025) 023). This test checks
  whether the twist field's *natural* version of it fits. It does not claim a new mechanism.
- Thawing models fit DESI but often less sharply than w0-wa, because they cannot cross w = -1 (no phantom phase). An
  "AS GOOD AS" or "WORSE" L2 result is entirely possible.
- A trans-Planckian F would weaken the "natural" claim; L3 states this up front.
