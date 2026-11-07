# PRE-REGISTRATION UB-1: can the coupled BI axion–dilaton do both dark-energy jobs? (background only)

Written and locked 7 Nov 2026 with AI assistance, at Danny's request, **before the code was run on any search**
(only a timing smoke test ran). Code: `theory/unify_hyperbolic_bg.py`, SHA-256
`b060820cf55617fae22a3eceb97e107bcc50a79b9792aca35fb557014fa0fbd5`.

## Why
Giarè & Sakstein (arXiv:2605.26116) show a single canonical scalar mostly cannot give early dark energy and late dark
energy together (matter-era scaling residue too large) and name non-canonical kinetic terms as an open way out. The BI
field is an axion–dilaton on a hyperbolic field space, which is that case. Our only unification check so far
(`theory/dilaton_running_F.py`, running F with constant W) did not include the coupled two-field motion. This test does.

## Model (fixed now; nothing here is fitted to data)
- Fields: canonical dilaton χ (|φ| = e^{√(2/3) χ}) and BI angle θ, kinetic metric diag(1, F(χ)²),
  F = F_P/|φ|, F_P = (4/π)√(3/2) = 1.559, kinetic mixing λ = −2√(2/3) (fixed).
- Potential V = A·U(χ) + L·(1 − cos θ)³ (n = 3 fixed). **No cosmological constant.**
  - **Variant A (derived):** U = (p − 1) e^{6p}/p², p = |φ| (GKY Kähler, constant W).
  - **Variant B (Spiral form):** U = e^{κχ}, κ ∈ [−3, 3].
- Radiation Ω_r = 9×10⁻⁵, matter 0.31 (fiducial), fields start at rest at a = 10⁻⁸.
- Free (energy scales and starting values the theory does not fix): ln A, ln L, θ_i ∈ [0.1, 3.0], |φ|_i ∈ [1.1, 60]
  (and κ for B). Box: ln A ∈ [−400, 5] (A) / [−60, 5] (B), ln L ∈ [0, 40].

## Requirements (f = field energy / total)
- **R2 early bump:** the largest f at z ≥ 1500 lies in 2000 ≤ z ≤ 6000 with 0.03 ≤ f_peak ≤ 0.15.
- **R3 fades:** f(z = 1090) ≤ 0.5 f_peak.
- **R4 quiet:** f ≤ 0.02 for all 20 ≤ z ≤ 500.
- **R5 late dark energy:** today −1 ≤ w0 ≤ −0.7 and 0.29 ≤ Ω_m ≤ 0.33 (the field supplies the rest).

## Search (fixed now)
Seed 20261107; 20 000 uniform samples per variant in the box, then Nelder–Mead (≤ 400 evaluations) from the 40 best,
minimising the summed fractional misses of R2–R5.

## Rule
- **PASS:** some point in either variant meets R2–R5 → write and lock UB-2 (a fit to CMB + BAO + SN data) before
  any data run. Which variant passed is reported; a pass in B only means the extra slope κ is needed.
- **FAIL:** no point meets all four → the coupled two-field route does not unify the roles within this box. Reported
  as a failure at full size, with the closest point and the requirements it misses. It does not prove impossibility.
- Neither outcome is evidence about data. Any change to the code, box or requirements after this lock is a logged
  deviation, and the original version is run and reported too.
