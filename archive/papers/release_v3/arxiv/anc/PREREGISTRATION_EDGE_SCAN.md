# Pre-registration: Late Twist edge scan (adds points near the viability edge to the (F, m) grid)

**Written:** 2026-11-01 12:34:01 CT. The time is from the clock, inserted by the command that hashes and commits this file.

**What existed at this time:**
- **DES Y5:** no Late Twist grid result existed (0 files).
- **Pantheon+:** 8 of the 24 grid points had finished (best +1.15 against ΛCDM), so for Pantheon+ this scan is
  **post-hoc** and labelled as such.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Why

- The best Late Twist fits sit in a thin band just above the viability edge, m²F² ≈ 1.2–2: the field is nearly frozen
  at the hilltop, so it behaves almost like a cosmological constant.
- The 0.2 dex grid has only one or two points near that band (m²F² = 1.58 at F = 2.5, m = 0.5), so it can miss the
  true best by a few units of χ².

## Points

On the curves m²F² = c, for c ∈ {1.3, 1.6} and log10 F ∈ {0, 0.2, 0.4, 0.5}:

| log10 F | log10 m (c = 1.3) | log10 m (c = 1.6) |
|---|---|---|
| 0.0 | +0.057 | +0.102 |
| 0.2 | −0.143 | −0.098 |
| 0.4 | −0.343 | −0.298 |
| 0.5 | −0.443 | −0.398 |

That is 8 points each for Pantheon+ and for DES Y5 (16 runs). The settings are those of the grid (deviation 08:58):
F and m fixed, the 11 standard parameters minimised, best of 2, the guard on. A point ending at the 1e5 penalty is
non-viable.

## Rules (verdict bands unchanged)

- **DES Y5 (blind, pre-results):** the Late Twist fit is the **lowest χ² over the 24 grid points and these 8 edge
  points**. L1, L2, L3 and shared F are judged on it, with the bands of PREREGISTRATION_LATE_TWIST.md.
- **Pantheon+ (post-hoc):** the official verdict stays the grid-only one (deviation 08:58). The edge-scan minimum is
  reported beside it, and labelled **post-hoc**.
- **The Coupled Twist** stays centred on the best Pantheon+ *grid* point, as already locked, whatever the edge scan
  finds.

## Expectation, written in advance

- The edge points will match or slightly beat the best grid points (+1.15 for Pantheon+), staying **close to ΛCDM**.
- With DES Y5, the edge band is where any gain will appear.
- The null mirror (run in parallel; LATE_TWIST_NULL_MIRROR.md) will show whether about +1 is a numerical offset.
