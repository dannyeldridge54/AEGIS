# TWIST INFLATION: the α = 1 prediction from the Twist's field-space curvature

**Status: LOCKED** on Danny's word ("Start trsting them", 12 Nov 2026, 18:14 CT, replying to the pending draft rules), before any of its numbers were computed. Drafted:, written 12 Nov 2026 during the 10-hour plan Danny asked for ("Do them all", 17:49 CT). AI-assisted.

**Why.** The Twist fixes its field-space curvature (λ = −2√(2/3), so K = −λ²/4 = −2/3), which is the α = 1 attractor
geometry (Starobinsky class). Twist leptogenesis needs near-instant reheating (≳ 2 × 10¹³ GeV). Together they predict the
inflation observables with no free parameter beyond the e-fold number N, which reheating pins near 55–57.

**Not blind.** Known at writing: Planck 2018 n_s = 0.9649 ± 0.0042; Planck+ACT+SPT 0.9684 ± 0.0030; Planck+ACT+DESI
0.9743 ± 0.0034; BICEP/Keck r < 0.036 (arXiv:2510.18656 compilation). The leading-order Twist value (N = 56, n_s =
0.964) was computed before this rule: −0.1σ, −1.4σ, −2.9σ respectively. So the current-data readings below are
**reported, not decisive**; the decisive reading is the future r measurement, which nobody has.

## Prediction (frozen now)
- α = 1 (from the curvature, not fitted). N from instantaneous reheating, computed with the standard e-fold formula
  for the E-model plateau V ∝ (1 − e^{−√(2/3) φ/M_P})², and n_s, r to next-to-leading order in 1/N.
- Until that calculation is run, the leading-order band stands: n_s = 0.9636–0.9649, r = 0.0037–0.0040 (N = 55–57).

## Readings
- **R-FUTURE (decides; for the first published r measurement with σ(r) ≤ 0.002):** **SUPPORTED** if r is detected and
  consistent with 0.0037–0.0040 within 2σ; **RULED OUT** if r < 0.002 at 95% or r > 0.008 at 95%.
- **NS-NOW (reported):** pulls against the three n_s combinations above, after the next-to-leading-order N.
- **NS-FUTURE (reported):** pull against the next CMB n_s release (Simons Observatory, SPT-3G full, or ACT final),
  whichever is first.

## What may not happen
No change of α, the reheating assumption, the potential or the bands after any number is computed. A different
inflation potential needs its own rule. Counted +1 in V7 when R-FUTURE is scored.

## Code
`theory/inflation/alpha_attractor_check.py` (leading order); the next-to-leading-order N calculation goes in
`theory/inflation/twist_inflation_N.py` after the lock.
