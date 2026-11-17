# PREREG J7a — Janus vs ASPIC (the real library) head-to-head on the pivot-scale observables

Locked 2026-11-17 before ASPIC or Janus is run on these points.

## Codes
- ASPIC: github.com/cosmicinflation/aspic commit 75400d205ae23c8cea9cd9ef10fb807e8b1da05d (10 Feb 2026), built
  with gfortran, called from a small Fortran driver: x_end = foo_x_endinf, x* = foo_x_trajectory(−N*, x_end, p),
  epsV = (foo_epsilon_one, _two, _three)(x*), n_s = scalar_spectral_index(epsV), r = tensor_to_scalar_ratio(epsV),
  α_s = scalar_running(epsV) (srflow, second order, with slowroll_to_hubble). This is ASPIC's documented route
  (manual: leading-order εV on the leading-order slow-roll trajectory, then second-order Hubble-flow spectra).
- Janus fast: tools/janus_calc (anyV.from_formula / core.Model; core.spectra3: n_s, α_s third order, r second order).
- Reference ("truth"): exact Mukhanov–Sasaki, tools/serapis_calc/ms.spectra_fast (as D990), same exact background.
Pivot definition for all three: N* e-folds before the end of inflation. ASPIC uses its own end (ε1V = 1 on the
slow-roll trajectory); Janus and the reference use ε_H = 1 on the exact background. That difference is part of what
each code predicts for "N* e-folds before the end" and is counted as error.

## Points (14)
LFI p = 2, 4, 2/3 (V = x^p); SI (V = (1 − e^{−√(2/3)x})²); NI f = 5, 10 (V = 1 + cos(x/f)); ESI q = 1 (V = 1 − e^{−x});
each at N* = 50 and 60.

## Outcomes (recorded for every point): |Δn_s|, |Δr|/r, |Δα_s| vs the reference, and wall time per point.
## Claims to test
C1 (accuracy): Janus median |Δn_s| ≤ ASPIC median |Δn_s| / 10, and Janus max |Δn_s| < ASPIC max |Δn_s|.
C2 (r): Janus median |Δr|/r ≤ ASPIC median / 3.
C3 (α_s): Janus median |Δα_s| ≤ ASPIC median |Δα_s|.
C4 (speed): Janus fast median time per point ≤ 100 ms (ASPIC's time recorded for information).
Verdict per claim (TRUE/FALSE) reported as is; "JANUS MORE ACCURATE" only if C1–C3 are all TRUE.
Reference MS runs go to the cloud background (resumable jsonl); a crash is handled via DEVIATIONS written first.
