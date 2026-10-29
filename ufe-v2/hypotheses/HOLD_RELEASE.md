# Hypothesis: hold and release, and the missing parameter (2026-10-29)

Tier: **hypothesis** (open). Nothing here is evidence; every number below either comes from our own fits or was
checked numerically in this session. Danny's prompt: "I suspect a missing parameter or axis, undiscovered. Use your
own math, examine similar structures and how it will fit."

## 1. The two loose ends it targets
1. **The start (θ_i).** Every Twist best fit starts the field at θ_i ≈ 2.78 rad ≈ 0.886π, near the top of its hill
   (π), where it would normally roll off at once. Today θ_i is simply fitted.
2. **The switch-on (z_c).** It sits at matter–radiation equality (free fit: z_c / z_eq = 1.005 for edeP). Today that
   is either fitted (free Twist) or imposed (Locked Twist). It is chosen, not derived.

## 2. The idea: a hold term that radiation feeds and matter drains
Potential (our model, n = 3, units Λ⁴, θ = φ/F): V(θ) = (1 − cos θ)³. Add one hold term W(θ) = −κ (1 − cos θ),
whose strength κ depends on the universe's contents.

**Checked numerically (finite differences):**
- V''(π) = −12 exactly, so the hilltop is unstable on its own.
- With W added, the curvature at π is −12 + κ. The field is **held at the top while κ > 12**.
- Below the threshold the resting point slides off the top to u = 1 − cos θ* = √(κ/3):

| κ | curvature at π | resting point θ* |
|---|---|---|
| 13 | +1 (held) | π |
| 12 | 0 (threshold) | π |
| **11.25** | −0.75 | **2.784 rad = 0.886π, our fitted θ_i** |
| 8 | −4 | 0.718π |
| 3 | −9 | 0.500π |

- So a start at 0.886π is what you get if the field tracks its resting point and is let go when the hold has fallen
  to about **94% of the threshold** (11.25 / 12). The fitted θ_i is then not a free choice but a *release snapshot*.

**The release clock.** Suppose radiation feeds the hold and matter drains it: κ ∝ α ρ_r − β ρ_m (plus Λ⁴-scale terms).
- While radiation dominates, κ is large and the field sits still on the hilltop: "a normally unstable shape held still".
- κ falls through threshold near ρ_r / ρ_m = β / α, so the switch-on happens at (1 + z_c) / (1 + z_eq) ≈ β / α.
- **The missing parameter is β/α, the balance of the two couplings.** Our free fit measures it as ≈ 1.005 (edeP),
  i.e. **consistent with 1**. If torsion makes α = β (radiation and matter coupling equally, e.g. through the same
  spin/axial-current source), the lock (z_c = z_eq) is *derived* rather than chosen.

## 3. Similar structures (where the same mathematics already works in nature)
| System | What holds the unstable state | What releases it | Match |
|---|---|---|---|
| **Kapitza's pendulum** | fast shaking of the pivot adds +(a²ω²/4) sin²θ to the effective potential | shaking weaker than a²ω² = 2gl | same form: a sin² term turning a maximum into a minimum |
| **Thermal symmetry restoration** (the Higgs field in the early universe) | thermal mass ∝ T² holds the field at the symmetric point | the universe cools below a critical temperature | the hold fed by radiation (T), release as T falls; standard physics |
| **QCD axion** | the potential switches on only when QCD confines (temperature-dependent mass) | the temperature falls below about 150 MeV | an oscillating field released by a cosmic event; also carries an integer N (domain-wall number) |
| **Inflation's hilltop and waterfall (hybrid inflation)** | a second field holds the first at the top | the second field crosses a critical value | release triggered by another quantity crossing a threshold, like ρ_r/ρ_m here |
| **Laplace resonance (Io:Europa:Ganymede = 1:2:4)** | resonant forcing | (stable) | resonance holding an arrangement still |
| **Tensegrity** | tension balancing compression | removing the tension | balance of two opposing contents, like α ρ_r vs β ρ_m |

The thermal-restoration analogy is the strongest: it is textbook early-universe physics, and it already does
"hold while hot, release when the contents change".

## 4. The other suspected missing pieces
- **An integer N in the field width.** The data want F ≈ 0.14 M_Pl, about 1/8.9 of the pure torsion value 1.2247 M_Pl.
  Similar structure: the QCD axion's effective width is f / N_DW, with N_DW an integer set by how many fermion
  species couple. A torsion field coupling through an anomaly (Nieh–Yan or axial) would get its N from counting
  fermions. Fits allow N = 8, 9 or 10 (7.7–10.1).
  - **Trap:** many fermion counts give numbers near 9 (3 generations × 3 colours = 9; SU(3) has 8 gluons). Any
    choice must be derived and pre-registered before checking, or it is numerology.
- **An axis.**
  - In an exactly uniform universe torsion can only have a "time" (axial-vector) part. A *spatial* axial-torsion
    vector would pick a direction in the sky: an axis.
  - Known real anomalies point at possible axes: the low-multipole quadrupole–octupole alignment ("axis of evil")
    and the hemispherical power asymmetry, both in Planck. They are not proven physical, and they are partly
    look-elsewhere effects.
  - A torsion axis would predict a direction-dependent effect and possibly direction-dependent birefringence.

## 5. What it predicts (each needs its own pre-registration before checking)
1. **θ_i is not free.** It follows from how fast κ falls through threshold relative to the field's mass. Integrate the
   field equation with κ(a) ∝ α ρ_r − β ρ_m in an expanding universe: does the release snapshot land at
   0.88–0.89π for physical rates? (Code: about an hour; it shares tools with ranked test #2, the Mathieu check.)
2. **One fewer free setting.** With θ_i derived and z_c locked (α = β), the Twist keeps only f_EDE: one extra setting
   instead of three. If that "Twist-1H" still gets Δχ² < −2 vs ΛCDM, it beats the AIC penalty. That would be a much
   stronger result than today's tie.
3. **The hilltop test (queued now, PREREG_THETA.md)** is this hypothesis's first check: the data must *require* a
   near-peak start. If starts far from π fit just as well, the hold mechanism loses its motivation.
4. **An axis (if spatial torsion exists):** a preferred direction shared by the low-ℓ anomalies and any birefringence
   map. Testable with Planck maps; needs a stated direction before looking.

## 6. Honest limits
- The hold term is postulated. Its physical origin (which torsion coupling makes κ ∝ α ρ_r − β ρ_m) is the actual
  Great Work II.
- Hilltop starts near π for n = 3 are common in early-dark-energy fits, so test 3 passing would mostly confirm known
  behaviour.
- The release-snapshot argument assumes the field tracks its resting point until let go. That has to be shown by
  integration (prediction 1), not assumed.
- If prediction 2 is pursued, the Twist-1H rule must be written before running, like PREREGISTRATION_ZEQ.md.
