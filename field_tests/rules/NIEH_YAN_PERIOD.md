# The Twist's decay constant from the Nieh–Yan index (derivation, 2 Nov 2026)

**Units:** reduced Planck units, κ = 8πG = 1/M_Pl² = 1. **Numbers:** `nieh_yan_period.py`, output in
`nieh_yan_period.json`. **Tier:** the algebra is a derivation; whether nature realises it is a HYPOTHESIS.

## Steps

1. **Action** (Mercuri & Taveras, 0903.4407 eq. 6): S ⊃ (1/2κ) ∫ β(x) N, with the Nieh–Yan 4-form
   N = Tᵃ∧T_a − eᵃ∧eᵇ∧R_ab = d(eᵃ∧T_a).
2. **The index** (Chandía & Zanelli):
   - Combine the spin connection and the tetrad into an SO(5) connection A = (ω^{ab}, eᵃ/ℓ), with ℓ a length.
   - Its curvature has R^{ab} − eᵃ∧eᵇ/ℓ² and Tᵃ/ℓ components, so tr_{SO5}(R∧R) − tr_{SO4}(R∧R) = (2/ℓ²) N.
     The (e∧e)² term vanishes because eᵃ∧e_a = 0.
   - Pontryagin integrals of R^{ab}∧R_{ab} are 8π² × integer, so **∫N = 4π²ℓ² ν, with ν an integer**.
3. **Periodicity:**
   - For constant β the term equals (β/2κ)·4π²ℓ²ν.
   - The quantum weight e^{iS} is unchanged when S shifts by 2πν, so β is an angle with period
     **Δβ = κ/(πℓ²)**.
   - This matches the η-vacuum picture of Kaul & Sengupta and Sengupta, where the BI parameter is the vacuum angle of a
     superposition over integer Nieh–Yan numbers.
4. **Canonical field:**
   - Torsion supplies the kinetic term (3/4κ)(∂β)², so φ = √(3/(2κ)) β (eq. 22).
   - The period of φ is 2πF, which gives

   **F = √(3/2) / (2π² ℓ²) M_Pl** (ℓ in reduced Planck lengths), divided by ν_min if the smallest allowed charge
   exceeds 1.

## Results

| Nieh–Yan length ℓ | F (M_Pl) |
|---|---|
| reduced Planck length 1/M_Pl | 0.062 |
| **Planck length √G** | **(4/π)√(3/2) = 1.559** |
| 2 × Planck length | 0.39 |

| Fitted F | ℓ needed (in Planck lengths √G) |
|---|---|
| late, DES Y5 best (1.00) | 1.25 |
| late, Pantheon+ best (2.51) | 0.79 |
| early role (0.14) | 3.34 |

## Reading

- **Late role:** if the Nieh–Yan length is the Planck length, the late Twist's decay constant is fixed at about
  1.56 M_Pl. Both late fits correspond to ℓ within ±25% of the Planck length.
- **Early role:** it would need ℓ ≈ 3.3 Planck lengths, a different scale. This is consistent with the early and late
  roles being separate (T1).
- **Status:** it is a consistency, and becomes a test with TF-P (locked 14:55:36, before any F-fixed result):
  F = 1.5594 fixed on DES Y5, Pantheon+ and Union3.

## Assumptions (each can change the number)

1. **The coupling normalisation** (1/2κ) of Mercuri & Taveras. Their Appendix A shows the matter coupling does not
   depend on an extra scale, but the topological coefficient's normalisation is a convention of that action.
2. **The minimal charge ν_min = 1.** On spin manifolds Pontryagin numbers can be restricted to multiples (for example,
   p₁ is a multiple of 48 for closed spin 4-manifolds). The relevant ν here is a difference of SO(5) and SO(4)
   classes, so the true minimum needs a careful topological argument; ν_min > 1 divides F.
3. **True periodicity.** The angle is periodic only if the physics (e.g. an instanton-generated potential ∝ cos)
   respects it. Sengupta's tunnelling vacuum energy ∝ e^{−S} cos η supports this.
4. **ℓ = √G** is a natural choice, not a derived one. This is the one free choice left. Picking the Planck length is
   the minimal-assumption option.
