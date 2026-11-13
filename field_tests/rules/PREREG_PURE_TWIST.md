# PURE-TWIST: the supergravity-embedded Twist with no free dark-energy parameter

**Status: DRAFT**, written 12 Nov 2026 (20:45 CT) during the theory work Danny asked for ("Keep going plan out our next
steps research and hypothesize and continue"). LOCKED only on Danny's word. AI-assisted. Cloud.

**Why.** In the plateau -> cliff -> tail supergravity model (matter doc, Developments 19–22), the late slope is fixed at
κ = √(2/3) by the α = 1 geometry, and the natural coupling of dark matter to the field is **zero** (matter masses do not
depend on the field when K_Z = 0, Akrami, Kallosh, Linde & Vardanyan, arXiv:1712.09693; a modular-weight coupling would
give β = 0.41 k, and the fitted β ≈ 0.034 would need an unnatural k ≈ 0.08). So the theory's own prediction for the late
universe is κ = √(2/3), β = 0: no parameter beyond ΛCDM's.

**Not blind.** Known at writing: TOURNAMENT (SPIRAL0, κ = 1, β = 0: ΔAIC +1.1, fails prediction) and KAPPA-ALPHA1
(κ = √(2/3) with β free: β 0.020–0.034, ΔAIC −4.30, NOT PREDICTIVE by 0.9 on SDSS).

## Model (frozen now)
Version K816B0: the TOURNAMENT SPIRAL code path with κ = 0.81650 and β = 0 fixed (k = 0). Same likelihood, data,
configs FULL / NOBAO / SDSS and starts as LCDM in `tournament.py`.

## Readings (TOURNAMENT definitions)
- **Gate:** stored ΛCDM rows reproduce within 0.05.
- **P-PRED (decides):** **PREDICTS** if dP_DESI ≤ 0, dP_SDSS ≤ 0 and d_SDSS ≤ 1 vs ΛCDM; **PREFERRED** if also
  Δχ²_FULL < 0 (k = 0, so ΔAIC = Δχ²). Otherwise **NOT PREDICTIVE**.
- **P-VS (reported):** the same numbers against SPIRAL0 (κ = 1, β = 0) and K816 (β free).

## What may not happen
No change of κ, β, data or bands after any number. Counted +1.

## Code
`field_tests/missing_piece/pure_twist.py` (after the lock) -> `field_tests/results/pure_twist.json`.
