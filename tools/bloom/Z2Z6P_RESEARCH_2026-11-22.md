# Z₂ × Z₆′ with discrete torsion: research pass (Danny 09:02–09:03; null at round 3)

## What exists (where others got to)
| work | result | where it stopped |
|---|---|---|
| **Honecker et al. 1209.3010** ("The Importance of Being Rigid"), T⁶/(Z₂×Z₆′×ΩR), discrete torsion η = −1, all tori tilted, Z₆′ twist w′ = (−2, 1, 1)/6 | **A global SUSY Pati-Salam model (Table 27):** a, b, c = U(4) × U(2)_L × U(2)_R on the **same bulk cycle** (0,1; 1,0; 1,−1), hidden U(2)_d × U(2)_e. **No chiral exotics** (one vector-like SU(4) pair). All U(1)s massive (Green–Schwarz). **Tree-level gauge unification automatic** (equal 3-cycle volumes). One-loop unification for v₁ = v₂ = 4v₃ + 168 ln2/π | Only **one generation** has a perturbative Yukawa; the other two need instantons or higher order. **MSSM and L-R models fail globally on twisted tadpoles.** The hidden stack d has adjoints (not on a shortest cycle) |
| **Gmeiner–Honecker 0806.3039** (Z₆′, no torsion) | 4.4e15 three-family SM models; 7.1e6 with no chiral exotics | α_s/α_w ≠ 1 at tree level (6, 4, 12); no-exotic models carry 12–21 Higgs candidates and a forced U(1)_{B−L} |
| **Ecker–Honecker–Staessens 1409.1236, 1509.00048** (Z₂×Z₆) | 2 PS prototypes, mild vector-like exotics; SU(5) GUTs excluded | Z₆/Z₃ exceptional cycles are outside CFT tools; 3 exotic O6 planes give no SUSY |
| **Deformations 1511.03549, 1702.08424** | twisted (blow-up) moduli of U(N) stacks are **frozen at the orbifold point by FI D-terms**; USp/SO stacks constrain none | unfrozen flat directions shift tree-level couplings |
| **Li–Sun–Sun–Wu 2511.16565** (Z₂×Z₂, generalised PS) | 4 new classes; unification at 2.6e16 – 5e17 with vector-like matter | Z₂×Z₂ only; hidden USp sometimes non-confining |

## The hints for the UFE
1. **Rigidity cures the exotics wall.** Discrete torsion removes adjoints and, in the global PS model, every chiral exotic. This is exactly where the Z₂×Z₂ Seed stalled (D2096–D2107).
2. **Unification comes from geometry, not tuning.** Three visible stacks on one bulk cycle, differing only in fixed-point data, have equal volumes, so g₄ = g_L = g_R at tree level. Our α_s chain then gives 0.1167 (one loop) and **0.1181 with v4's spectrum at μ = 0.55 m₃/₂** (D2100 P6), or the KL + GM branch (D2091).
3. **The Yukawa gap points to instantons.** Two generations need non-perturbative masses. That is the same D-instanton machinery as B4's μ_W (D2102) and the natural source of a generation hierarchy.
4. **Twisted tadpoles select PS over MSSM.** PS is the fork the geometry allows, which fits Seed v4's PS choice.
5. **The orbifold point is held fixed by D-terms** for U(N) stacks: no blow-up modulus for the visible sector.

## Folding in Danny's twist picture (labelled)
- **PHYSICS:**
  - Z_N is a twist (clock arithmetic), and Z₂ × Z₆′ is two twists.
  - **Discrete torsion is a twist between the twists** (a phase on the commutator). It is what makes the branes rigid and removes the exotics.
  - Fractional branes sit at the Z₂ fixed points, the cone tips. The **FI D-terms hold those "hourglass necks" shut** (the twisted moduli are frozen at the orbifold point).
- **ANALOGY:**
  - the three visible stacks are **three hands on one clock face**: one bulk cycle, three fixed-point settings. Their equal length is why they unify.
  - The Yukawas the twist forbids at tree level must come "through the neck", from instantons.

## Next build: Seed v6 on Z₂×Z₆′ (to be locked)
- **Implement for the AAA lattice:**
  - bulk X, Y (formula above);
  - SUSY: Y = 0 and 2X + Y > 0;
  - bulk tadpole Σ N(2X + Y) = 4(η_ΩR + 3Σ η_ΩRZ₂⁽ⁱ⁾);
  - fractional cycles with Z₂ eigenvalues, displacements σ and Wilson lines τ;
  - twisted tadpoles;
  - χ = ¼(XY′ − YX′ − Σ exceptional).
- **Positive control:** reproduce Table 27's PS model.
- **Owed before coding:** the exceptional-wrapping tables (1209.3010 Tables 7, 8, 36; past the fetched text) and the twisted-tadpole forms for α = 4, 5 and k = 2, 3.
