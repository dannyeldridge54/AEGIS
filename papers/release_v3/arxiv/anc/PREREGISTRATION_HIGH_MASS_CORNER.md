# Pre-registration: the Late Twist high-mass corner (HC)

**Locked:** 2026-11-01 13:31:40 (time from Get-Date).

**Written and locked before:** any run in this corner. No point below has ever been evaluated.

**Why:** DEEP_DIVE_HINTS_2026-11-01.md, H2.
- Lin, Visinelli & Yanagida (arXiv:2504.17638) find the data prefer a sub-Planckian decay constant with a relatively
  large mass, starting near the hilltop.
- Shiu, Tonioni & Tran (arXiv:2604.09141) push the mass ≫ H₀ once f < M_Pl is imposed.
- The locked grid (F ≥ 0.4 M_Pl, m ≤ 2.5 H₀) never reached that corner. Every small-F grid point ended
  non-viable, possibly because of a code limit.

## Points (Pantheon+, the reference SN set)

- **F** ∈ {10^−0.6, 10^−0.4, 10^−0.2} M_Pl.
- **m** is chosen so that m²F² ∈ {2, 8, 32}, which gives log10 m = ½ log10(m²F²) − log10 F.

| log10 F | log10 m (m²F² = 2) | (8) | (32) |
|---|---|---|---|
| −0.6 | 0.751 | 1.052 | 1.353 |
| −0.4 | 0.551 | 0.852 | 1.153 |
| −0.2 | 0.351 | 0.652 | 0.953 |

**Runs:**
- Each point runs as `ax_spa_latetwist_gF<lf>m<lm>`, with the same code, settings, best-of-2 and penalty guard as the
  grid.
- All 9 points sit inside the original priors (log10 F ≥ −1.3, log10 m ≤ 1.5).
- A point ending on the penalty, or with no finite χ², is **non-viable (code-limited)** and is not retried.

## Statistic and verdict

- HC_best = the lowest finite χ² over the 9 points.
- G_best = the official Pantheon+ grid best (grid points only, as locked).
- Δ_HC = HC_best − G_best.

| Outcome | Verdict |
|---|---|
| No finite point | **NOT REACHABLE (code-limited)**: the corner stays untested by this pipeline, and this is said in the paper |
| Δ_HC ≤ −1 | **BETTER CORNER**: the literature corner fits better. A refit there (and DES Y5) needs its own pre-registration |
| −1 < Δ_HC < +1 | **SIMILAR** |
| Δ_HC ≥ +1 | **WORSE**: the super-Planckian grid region is preferred |

**Also reported, with no verdict:**
- HC_best − χ²(ΛCDM halofit), as written and offset-corrected (−1.35, LATE_TWIST_NULL_MIRROR.md);
- the field's w0 and wa at HC_best, from `latetwist_cpl.py`.

## What this does not change

- HC is **separate** from the locked grid, the edge scan, LD and LEE-G.
- The official L1–L3 verdicts, the LEE-G trial count and the LD point choice are all unaffected. The LD picker uses
  only grid and edge points.
- Even if HC finds a better point, it is reported beside the official verdicts and never replaces them.

## Implementation (written with this file)

- `axiclass/run_hc.sh` starts after `run_late_dovekie.sh` prints "LD finished", with at most 8 fits running.
- `rank_models.py` recognises HC points (off the grid with m²F² ≥ 1.9) and keeps them out of the grid, the
  Pantheon+ edge line and LEE-G. It prints the HC line.
