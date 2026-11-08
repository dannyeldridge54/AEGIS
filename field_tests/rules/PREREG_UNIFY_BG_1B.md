# PRE-REGISTRATION UB-1b: the derived supergravity potential with a non-constant superpotential (background only)

Written and locked 7 Nov 2026 with AI assistance, at Danny's request ("Both"), **after UB-1's results were seen** and
**before this code was run on any search** (only a timing smoke test and a b = 0 check against UB-1 variant A).
Code: `theory/unify_hyperbolic_bg_ub1b.py`, SHA-256 `bea8c6b8fac66bbb1389cb5ea2909ff0dfb58d82c28cc07c938354afc9e7a974`.

## Why
UB-1 (D1) passed only with an ad hoc exponential dilaton (variant B, extra slope κ); the derived potential with
constant superpotential (variant A, b = 0) failed in both versions. The standard supergravity generalisation, already
written down before UB-1 in `theory/dilaton_running_F.py`, is W = W0 exp(bΦ), which turns the derived potential into
V = A (|φ| − 1) e^{(6 − 2b)|φ|} / |φ|². UB-1b asks whether that family, not an ad hoc shape, can do both jobs.

## What changes from UB-1 D1 (nothing else does)
- One variant, **C**: U = (p − 1) e^{(6 − 2b) p} / p², p = |φ|, with **b ∈ [0, 2.9]** as a fifth search dimension.
  b = 0 reproduces UB-1 variant A exactly (checked).
- Same fields, metric, λ, F_P, n = 3, no cosmological constant, same box for ln A, ln L, θ_i, |φ|_i, same requirements
  R2–R5, same search (seed 20261107, 20 000 samples, Nelder–Mead from the best 40), same integrator (DOP853).

## Rule
- **PASS:** some point meets R2–R5. Reported as "the derived family passes with one extra superpotential parameter b",
  i.e. the same parameter count as variant B, with the value of b stated. It is **not** a pass for the b = 0 derived
  potential, which stays FAILED (UB-1).
- **FAIL:** no point meets all four; reported at full size with the closest point and its missed requirements.
- Either way, UB-1's verdicts are unchanged. Neither outcome is evidence about data.
