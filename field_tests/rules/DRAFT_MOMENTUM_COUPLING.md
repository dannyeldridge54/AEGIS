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
