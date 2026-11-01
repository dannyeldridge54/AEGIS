# Pre-registration: Late Twist on DES-Dovekie (LD) and the grid look-elsewhere rule (LEE-G)

**Locked:** 2026-11-01 13:25:13 (time from Get-Date).

**Written and locked before:** any Late Twist Dovekie run, and before the Pantheon+ grid, the DES Y5 grid and the edge
scan are complete.

**State at lock:** Pantheon+ grid at 12 fits plus 10 non-viable points (best +0.96 vs ΛCDM halofit). DES Y5 grid at
4 of 24 (best −5.32). Edge scan: 0 results. The DES Y5 number is known and is the reason for this test, which is
disclosed. Neither rule depends on which point wins.

## Why

- The DES Y5 sample has a known ≈ 0.04 mag calibration offset. DES-Dovekie is the corrected sample.
- For A3, Dovekie cut the late gain from −20.67 to −14.20 (ROBUSTNESS_RESULTS.md).
- A Late Twist gain seen only with DES Y5 could therefore be a supernova systematic.
- Picking the lowest of about 32 grid and edge points is a search, and the significance must count it.

## LD: the Late Twist with DES-Dovekie

**Points (chosen by rule, after both grids and the edge scan are complete):**
1. The official DES Y5 best: the lowest χ² over the DES Y5 grid and edge points (the edge points count, as locked in
   PREREGISTRATION_EDGE_SCAN.md).
2. The official Pantheon+ best: the lowest χ² over the Pantheon+ grid points only (the edge points are post-hoc there).
3. If both are the same (F, m), it is run once.

**Runs:**
- Each point is run as `ax_spa_latetwist_gF<log10 F>m<log10 m>_dovekie`, with F and m fixed at that point's values
  and all standard parameters fitted (best of 2, as for the grid).
- References: `ax_spa_lcdm_halofit_dovekie` and `ax_spa_w0wa_halofit_dovekie`.
- Same code, settings and likelihoods as the grid, with only the supernova sample swapped.

**Statistic:** Δ_D = (lowest χ² over the LD points) − χ²(ΛCDM halofit, Dovekie).

| Δ_D | Verdict |
|---|---|
| ≤ −4 | **CONFIRMED**: the Late Twist gain survives the corrected supernovae |
| between −4 and −1 | **WEAKENED** |
| > −1 | **NOT CONFIRMED**: the DES Y5 gain is not robust to the calibration fix |

**Reporting rules:**
- These are the same thresholds as the A3 bands.
- The halofit offset-corrected value (Δ_D − 1.35, LATE_TWIST_NULL_MIRROR.md) is reported beside it but does not set
  the verdict.
- L2 on Dovekie (Late Twist vs w0–wa halofit, Dovekie) is reported too, with no new verdict band.
- **Any DES Y5 Late Twist headline must be stated together with the LD verdict.**

**Known bias (accepted):** the points are fixed at the (F, m) chosen on DES Y5 or Pantheon+, not refitted on Dovekie.
This can only make Δ_D less negative, so the test leans slightly against confirmation.

**A failed or non-finite LD run** counts as NOT CONFIRMED (code-limited). It is not retried with new settings.

## LEE-G: look-elsewhere for the grid

Applied separately to the official Pantheon+ best and the official DES Y5 best.

1. **Local:** Δχ²_loc = χ²(official best) − χ²(ΛCDM halofit, same SN set), as written, with no offset correction.
   This applies only when Δχ²_loc < 0; otherwise the result is NOT SIGNIFICANT.
2. **Local p-value:** p_loc = P(χ²₂ ≥ −Δχ²_loc), with 2 degrees of freedom (F and m).
3. **Trials:**
   - N_eff = the number of distinct F values with at least one finite, viable point in that set's official fit.
   - The official fit is grid plus edge points for DES Y5, and grid only for Pantheon+.
   - The reason: as m → 0 the field freezes and F is unidentified (the Davies problem), so F is the searched direction.
4. **Global:** p_glob = 1 − (1 − p_loc)^N_eff (Šidák).
5. **Significance:**
   - Z = Φ⁻¹(1 − p/2) (two-sided, the same convention as converting χ² to σ).
   - Report both Z_loc and Z_glob.

| Z_glob | Reading |
|---|---|
| ≥ 2 | **HOLDS** after look-elsewhere |
| 1 to 2 | **WEAK HINT** |
| < 1 | **NOT SIGNIFICANT** |

**What this rule does not change:**
- It changes no existing verdict. L1, L2 and L3 stay as pre-registered.
- It is reported beside them, and quoted with any Late Twist significance.
- The offset-corrected Δχ² may be shown as a second line, labelled post-hoc.
- An independent (F, m) refit or posterior sampling (Phase D) supersedes LEE-G when available.

## Implementation (written with this file)

- `axiclass/pick_late_dovekie.py` applies the point-choice rule above to the result files.
- `axiclass/run_late_dovekie.sh` waits until the edge scan has finished and no Late Twist grid fit is running. It then
  starts the references and the chosen points, with at most 8 fits running.
- `rank_models.py` prints the LD and LEE-G results.
