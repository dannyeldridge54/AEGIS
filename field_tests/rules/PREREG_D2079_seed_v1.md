# PREREG D2079: Seed engine v1. The tiniest branch first, then rings spinning outward, with goalposts at every level. Locked before any ring runs.

## Rings (each expands the lenses and the radii grid)
| ring | lens range \|n\| ≤ | radii grid χ |
|---|---|---|
| R0 (seed) | 1 | {1} |
| R1 | 2 | {½, 1, 2} |
| R2 | 3 | {⅓, ½, 1, 2, 3} |
| R3 | 4 | {¼, ⅓, ½, 1, 2, 3, 4} |
| R4 | 6 | {⅕, ¼, ⅓, ½, 1, 2, 3, 4, 5} |

**Forks** (all rings): β¹, β² ∈ {1, ½}; ρ ∈ {1, ⅓}; ε = ±1.
- From R2 on, only the forks that **earned** expansion spin: those with at least one joint hit in the previous ring, or all of them if none earned. This is the "outward only where it pays" rule, and it is recorded.

## Hard filters (consistency, never data)
- n_c¹ integer (massless U(1)_Y);
- tadpole ≤ 16 (hidden branes fill the rest);
- three families automatic (D2067);
- **SUSY:** each stack's angle sum satisfies \|Σᵢ arctan(mᵢχᵢ/nᵢ)\| ≤ 0.05 rad (mod 2π).

## Fit (2 numbers)
- 1/α₂(M_Z) = 29.59 and 1/α_Y(M_Z) = 98.37, giving K and L = ln(M_s/M_Z).
- Physical only if K > 0 and 0 < L < 38.8.

## Held-out goalposts (all three needed for a JOINT hit)
- **G1:** α_s(M_Z) within 2σ (0.1180 ± 0.0009);
- **G2:** proton decay, M_s ≥ 4e15 GeV (dimension-6 estimate, stated);
- **G3:** SUSY, already a filter (so every survivor passes it).

## Evidence rule, per ring
- **chance** = (fraction of physical configs passing G2) × (the G1 window's share of the local α_s density, ±0.02 around 0.118, as in D2078);
- **SIGNAL** if the joint-hit fraction ≥ 3 × chance and there are ≥ 5 joint hits;
- otherwise NULL.

## Hand-tuned knobs
These are fixed here. Changing them later requires a DEVIATIONS file first.
- SUSY tolerance 0.05 rad;
- proton bound 4e15 GeV.
