# KAPPA-ALPHA1: the late slope fixed by the α = 1 geometry

**Status: LOCKED** on Danny's word ("Start trsting them", 12 Nov 2026, 18:14 CT, replying to the pending draft rules), before any of its numbers were computed. Drafted:, written 12 Nov 2026 after the TOURNAMENT score, during the plan Danny asked for ("Keep going").
AI-assisted. Cloud.

**Why.** The α = 1 field-space geometry (Twist inflation; Dimopoulos & Owen, arXiv:1703.00305) fixes the late
exponential slope at κ = 2/√(6α) = √(2/3) = 0.81650, with no fitting. The flagship uses κ = 1.

**Not blind.** Known at writing: SIMPLIFY-L (κ = 0.8165 within 0.69 of κ = 1 on summed SN score); TOURNAMENT free-κ
SPIRAL chose κ 0.85 (with DESI) and 0.79 (no BAO), and predicted DESI with Δχ² −6.27 but SDSS with +0.39 vs ΛCDM.
So this rule tests whether a version with **zero extra parameters beyond FLAG-1** keeps the free-κ prediction.

## Model (frozen now)
Version K816: the TOURNAMENT FLAG-1 model with κ = 0.81650 fixed (k = 1: β only). Same code path as SPIRAL in
`tournament.py` with p[4] fixed; same starts as FLAG1; same likelihood, data and configs FULL / NOBAO / SDSS.

## Readings (same definitions as PREREG_TOURNAMENT.md)
- **Gate:** the stored ΛCDM rows reproduce within 0.05.
- **K-PRED (decides):** K816 **PREDICTS** if dP_DESI ≤ 0, dP_SDSS ≤ 0 and d_SDSS ≤ 1 (vs ΛCDM). **PREFERRED** if it
  also has ΔAIC_FULL < 0. Otherwise **NOT PREDICTIVE**.
- **K-VS-FLAG1 (reported):** ΔAIC_FULL and the two prediction χ² against FLAG-1 (κ = 1).

## What may not happen
No change of κ, priors, data or bands after any number is computed. A different κ needs its own rule.
Counted +1.

## Code
`field_tests/missing_piece/kappa_alpha1.py` (after the lock) → `field_tests/results/kappa_alpha1.json`.
