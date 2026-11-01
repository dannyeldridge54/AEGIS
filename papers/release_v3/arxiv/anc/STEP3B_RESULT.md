# Step 3b: can geometry derive the lock (the energy peak at matter–radiation equality)?

31 October 2026, about 21:00 CT. Code: `step3b_trigger.py` plus the inline check below. Symbolic algebra in sympy 1.14;
numbers with scipy.

## Answer in one line

**Not from the minimal twist action.** The simplest geometric addition fires *near* equality but needs a tuned
strength. A trigger that fires *only* at equality needs a non-polynomial curvature function, which the twist action
does not supply. **The lock stays a well-motivated choice, not a derivation.**

## What was checked

### 1. The minimal action gives no trigger
- The Holst-type contraction ε^{abcd} R_{abcd} of the ordinary curvature is **exactly 0** in an expanding (FRW) universe
  (computed symbolically from the metric).
- After the torsion is solved, the Barbero–Immirzi field keeps only its kinetic term (Taveras & Yunes 2008). There is
  no coupling to curvature at all.
- Its coupling to particle spin (the fermion axial current) averages to zero in the hot, unpolarised early universe.
  The spin–spin contact energy is about 10⁻⁵⁷ of radiation (paper §2).

**So nothing in the minimal theory knows when equality happens.**

### 2. Curvature *does* know when equality happens
- The Ricci scalar is **R = 0 in the radiation era** (a ∝ t^½) and **4/(3t²) in the matter era** (a ∝ t^⅔).
- With both present, **R / H² = 3 Ω_m(a) = 3 / (1 + a_eq / a)**, which reaches half its final value exactly at
  equality.

### 3. The smallest addition, ξ R φ²/2 ("early modified gravity"), fires near equality but not automatically

The switch is soft: R/H² grows ∝ a long before equality. So the field's start depends on the coupling strength.

| ξ | Field starts moving at a/a_eq | z / z_eq |
|---|---|---|
| ±10 | 0.007 | ~145 |
| ±3 | 0.022 | ~44 |
| ±1 | 0.07 | ~14 |
| ±0.3 | 0.24 | ~4 |

- Starting at equality needs |ξ| ≈ 0.07–0.1. That trades the onset time z_c for a coupling ξ, so it is not a free
  derivation.
- ξ ~ 0.1 is a natural size, so this is "near equality without fine-tuning", but not "exactly at equality".
- **A known cost:** a field coupled to R changes the strength of gravity over time. That is constrained by
  gravitational-wave propagation (Gao et al. 2026 bound exactly this kind of non-minimal term) and by Big Bang
  nucleosynthesis / G-variation limits.

### 4. No simple curvature combination fires *only* at equality
- In FRW with matter and radiation (units 8πG = 1):
  - R = ρ_m;
  - R_μν R^μν = ρ_m² + 2ρ_mρ_r + (4/3)ρ_r²;
  - Gauss–Bonnet = −(4/3)(ρ_m² + 3ρ_mρ_r + 2ρ_r²).
- A trigger that vanishes in both pure eras must be ∝ ρ_m ρ_r.
- **Requiring the ρ_m² and ρ_r² parts to vanish forces the ρ_mρ_r part to vanish too.** The only such combination of
  R², R_μνR^μν and Gauss–Bonnet is identically zero in FRW (the 4D conformal-flatness identity).
- So a clean equality-only trigger needs a *non-polynomial* function of curvature, which is what Jing, Tian & Zhu (PRD
  109, 044016, 2024) use. Nothing in the Holst / Nieh–Yan action produces such a function.

## What this means for the theory

- **The lock:** keep it as a phenomenological choice, described honestly. The data say "the energy peak is no later
  than equality" (DEEP_DIVE §2). The combined-telescope fit **passed** with it (COMBINED_CMB_RESULTS.md).
- **The best geometric story available:** a small curvature coupling, ξ ~ 0.1, places the onset near equality. It
  costs one parameter and brings gravitational-wave and G-variation tests. That could become a pre-registered model
  variant ("Twist + ξR"), testable with the existing pipeline plus a modified-gravity code.
- **Unchanged:** step 2 (deriving the potential's cos³ shape) remains the main derivation target. Step 3b closes as
  "not derivable from the minimal action".
