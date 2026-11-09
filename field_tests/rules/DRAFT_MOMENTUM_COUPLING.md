# Momentum coupling for the lensing problem (S8-M) (DRAFT, not locked; engine not built)

**Status: DRAFT** (8 Nov 2026). Not locked; nothing has been run. Needs an engine check first (below).

## Idea
In "pure momentum exchange" (dark scattering) models, dark energy and dark matter exchange momentum but not energy:
the expansion history is unchanged, while the growth of structure at late times is slowed, which lowers S8 and the
lensing signal. Literature (to check before locking): Simpson 2010, arXiv:1004.5023; Pourtsidou, Skordis & Copeland
2013, arXiv:1307.0458 (their "type 3" models).

**Honest label: CHOSEN, not derived.** The Twist's equation map has no momentum-exchange term today. If one can be
derived from the action (e.g. a derivative coupling ∂φ·u_c), it must be written in `theory/` before this rule is
locked; otherwise the rule says plainly that this is an add-on.

## Model (fixed when locked)
Spiral fit unchanged, plus one parameter ξ (momentum-exchange strength) acting on the dark-matter velocity equation
only. Background identical to the Spiral at the same parameters (checked as gate G-M1). +1 parameter vs the Spiral.

## Tools found (8 Nov)
- Linear: Dark Scattering CLASS, github.com/PedroCarrilho/class_public branch `IDE_DS` (commit 7a909f4), CPL fluid
  dark energy with the friction term; KiDS-1000 analysis: Carrion et al. 2024, arXiv:2402.18562 (positive A_ds lowers
  S8; KiDS+CMB+BAO prefers A_ds ≈ 10.6 (+4.5/−7.3) b/GeV at ~2σ).
- Nonlinear: ReACT / ACTio-ReACTio, github.com/nebblu/ACTio-ReACTio (commit a36dda0), model `ds` (w0, wa, ξh), with a
  CosmoSIS module; calibrated in arXiv:2111.13598. Valid for −1.3 < w0 < −0.7, −1.5 < wa < 0.6, z ≤ 2.5 (all
  Spiral-family CPL values are inside).
- The effect scales with (1 + w): the Spiral's thawing field (w0 ≈ −0.92) gives it something to act on; ΛCDM would not.
- Our Spiral's dark energy is a scalar field in the coupled AxiCLASS build, not a CPL fluid: the friction term must be
  ported into that build (θ_c' gets −a ξ (1+w_φ) ρ_φ (θ_c − θ_φ)), and checked against DS-CLASS run with the Spiral's
  own CPL (w0, wa) (gate G-M0). ReACT is given the Spiral's CPL fit; that approximation is stated with the result.

## Status 8 Nov (theory/MOMENTUM_COUPLING_NOTE.md)
Not derivable from the Twist's couplings (chosen add-on). DS-CLASS smoke test: σ8 only −0.45% at A_ds ≈ 10 and −1.07%
at A_ds ≈ 30 for the Spiral's w(z): a weak lever. Not locked; revisit only if KiDS and DES both show a real tension.

## Engine gates (before any data fit)
- **G-M0:** find a public, published implementation (CLASS or CAMB) and reproduce one figure/number from its paper;
  if none exists, write the patch and reproduce the paper's linear growth suppression within 2%.
- **G-M1:** ξ = 0 reproduces the stored Spiral fit's χ² within 0.05.
- **G-M2:** nonlinear power: a halo model or emulator calibrated for momentum exchange (e.g. a ReACT-type reaction)
  must exist and pass ξ = 0 → HMcode-2020 within 2%; if not, Part 2 (full shear) is not run and that is reported.

## Tests (fixed when locked)
1. Fits on the same three data combinations as the Spiral, best of 4 (ΛCDM refits with equal effort).
2. vs ΛCDM: **BEATS** if Δχ² ≤ −4 on at least 2 of 3; vs Spiral: ΔAIC reported.
3. Lensing A (DES Y6 S8 penalty, as S8-WL Part 1) and, if G-M2 passes, B (full DES Y3 shear, as Part 2), limit +2,
   at least 2 of 3. Verdict words as S8-L: LENSING FIXED / TRADE-OFF / NOT FIXED.
4. Counted as one more hypothesis in the V7 look-elsewhere inventory.

## Cost
Engine work in the cloud (cheap); 3 fits + 3 ΛCDM refits on the PC (about 5 h each, can run in parallel).
