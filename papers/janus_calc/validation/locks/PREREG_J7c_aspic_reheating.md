<!-- AEGIS-FP VO34RTURYKCBBEE7 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J7c — Janus vs ASPIC through the reheating route (same ln R_rad), scored against an exact solution

Locked 2026-11-17 before any J7c number.

## Matching equation (fetched: Martin & Ringeval 1004.5525 via ar5iv, Eq. 15 "this equation is exact", Eq. 16 N_0)
ln R_rad = ΔN* + N_0 − ¼ ln(H*²/ε1*) + ¼ ln[(3/ε1*)(V_end/V*)(3 − ε1*)/(3 − ε1,end)].
[derived] (algebra, using H² = V/(3 − ε)): the bracket is 3H_end²/(ε1* H*²), so
ΔN* = ln R_rad − N_0 + ½ ln H* − ¼ ln(3 H_end²), in which the potential normalisation M⁴ cancels exactly
(H* and H_end may be computed with the normalised potential). N_0 = ASPIC's own constant Nzero (src/common/srreheat.f90,
printed by the driver), so both codes and the reference share all physical constants; only the method differs.

## Codes
- ASPIC @75400d2: foo_x_rrad(params, x_end, ln R_rad, P*, bfoldstar) → x*, ΔN* = −bfoldstar; spectra from srflow at x*
  (as J7b). P* = ASPIC's powerAmpScalar.
- Exact reference: exact background (ε_H = 1 end); solve N_end − N_piv = ln R_rad − N_0 + ½ ln Ĥ(N_piv) − ¼ ln(3Ĥ_end²)
  for the pivot (root find in N_piv); exact Mukhanov–Sasaki spectra there (J7b reference settings: 9 k-points on [−1, 1], bd = 1000).
- Janus: the same exact matching on its own background (tools/janus_calc core.Model), spectra3 at that ΔN*.
## Points: the 16 J7b models that ASPIC scored, at ln R_rad = 0 (radiation-like) and ln R_rad = −10 (32 points).
## Claims
C1 n_s: Janus median |Δn_s| ≤ ASPIC median/10 and Janus max < ASPIC max. C2 r: Janus median |Δr/r| ≤ ASPIC/3.
C3 α_s: Janus median ≤ ASPIC median. C5 (reported) ASPIC's ΔN* error vs the exact matching, median and max.
Verdict "JANUS MORE ACCURATE (reheating route)" iff C1–C3. Failures to produce a number are listed, not dropped.
Fixes only via PREREG_J7c_aspic_reheating_DEVIATIONS.md before any rerun.
