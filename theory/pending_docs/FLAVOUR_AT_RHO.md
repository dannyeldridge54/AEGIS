# Flavour at ρ — the Weave's second strand (run 1, 19 Nov 2026, D1595)

Goal (Danny 12:12): extend the Weave to a unified field τ, where V(τ) gives inflation, Y(τ) gives masses and mixings, and θ(τ) gives strong CP, all with the vacuum at the inflation endpoint ρ = e^{iπ/3}. Start with charged leptons and Koide.

Target Lagrangian:
    L = ½R − |∂τ|²/(4 Im τ²) − V(τ) + ψ̄ Y(τ) H ψ + θ(τ) G G̃ /(32π²)

## Section map
| § | content | status after run 1 |
|---|---|---|
| F1 | modular A4 (Γ₃) weight-2 triplet Y(τ), validated | DONE |
| F2 | minimal constructions exactly at ρ | DONE: all FAIL (locked) |
| F3 | the Koide theorem: Z₃ structure ⇔ Brannen form; Q = 2/3 ⇔ equipartition | DERIVED |
| F4 | data: amplitude √2 and phase δ = 2/9 | MEASURED |
| F5 | what ρ explains, and what it does not | VERDICT |
| F6 | "same τ" question (dilaton versus flavour modulus) | OPEN |
| F7 | next runs | LISTED |

## F1. Setup [lit + der]
A4 weight-2 modular triplet built from Dedekind η (Feruglio, arXiv:1706.08749). Validation: Y(ω)/Y₁ = (1, ω, −ω²/2) holds to 5e-31. At ρ = ω + 1, Y(ρ)/Y₁ = (1, ω², −ω/2) with |Y| = (1, 1, ½), the same moduli as at ω (T-image). At τ = i, |Y| = (1, 0.732, 0.268).

## F2. Exactly at ρ (locked PREREG_FLAV_RHO): FAIL
Q from the four fixed constructions:
| construction | at ρ | at i |
|---|---|---|
| C1: √m_i ∝ |Y_i| | 0.360 | 0.402 |
| C2: m_i ∝ |Y_i| | 0.341 | 0.355 |
| C3: √M = circ(Y₁,Y₂,Y₃) | 0.3333 (one nonzero mass) | 0.500 |
| C4: √M = circ(Y₁,Y₃,Y₂) | 0.3333 | 0.500 |
None is within 1e-3 of 2/3. At ρ, Y is an eigenvector of the residual Z₃, so the circulants collapse to a single nonzero mass (Q = 1/3). This matches the known result that exact fixed points give degenerate or vanishing masses, and hierarchies need a small departure from the fixed point (Novichkov–Penedo–Petcov; Feruglio 2211.00659).

## F3. The Koide theorem [derived; algebra exact — NOT new: Foot's 45° reading; Parseval form in preprints.org 202606.2124 (D1602). New here: ρ supplies the Z₃ dynamically]
Let √M be any matrix covariant under a Z₃ acting by cyclic permutation (a circulant): √M = a·1 + b·C + b̄·C². Its eigenvalues are the Z₃ Fourier modes:

    √m_k = a + 2|b| cos(φ + 2πk/3),   k = 0, 1, 2

This is exactly the Koide/Brannen parametrisation √m_k = μ(1 + A cos(δ + 2πk/3)), with μ = a, A = 2|b|/a, δ = φ. Then

    Σm = 3a² + 6|b|²,   (Σ√m)² = 9a²   ⇒   Q = 1/3 + (2/3)(|b|/a)²

So **Q = 2/3 ⇔ |b|² = a²/2 ⇔ A = √2**. The norm of the Z₃-singlet part of √M (3a²) equals the norm of the Z₃-doublet part (6|b|²): an **equipartition** between the two representations of the residual symmetry. Koide's mystery number 2/3 is the statement that the trivial and non-trivial Z₃ components of the square-root mass matrix carry equal weight.

## F4. Data [computed]
| m_τ source | Q | amplitude A (√2 = 1.414214) | phase δ (2/9 = 0.222222) |
|---|---|---|---|
| Belle II 2023: 1777.09 ± 0.14 MeV | 0.6666735 | 1.414228 | 0.2222136 ± 0.0000095 (−0.91σ) |
| PDG (recalled): 1776.93 ± 0.09 MeV | 0.6666645 | 1.414209 | 0.2222248 ± 0.0000063 (+0.41σ) |
Both A = √2 and δ = 2/9 (Brannen's observation) hold to within 1σ of current τ data. They are correlated: the two numbers together fix both mass ratios.

## F5. Verdict for run 1
- ρ's residual Z₃ **explains the form** of Koide's formula: the cosine-of-thirds structure is the Z₃ Fourier spectrum. [derived]
- It does **not** explain the two numbers. Nothing at ρ forces A = √2 (equipartition) or δ = 2/9, and the minimal modular constructions exactly at ρ fail.
- Candidate principle, the analogue of Zhinü for flavour [POSTULATE P-F1, candidate only]: the square-root mass matrix sits at Z₃ equipartition, ‖singlet‖ = ‖doublet‖. This mirrors the inflation principle, where V₀/V∞ = |∇ln Λ|²/λ² is an equality of norms at saturation. Not derived.

## F6. Same-τ question [open]
In modular-flavour models τ is usually a complex-structure modulus; in the Weave it is the axio-dilaton. Using one field for both needs Yukawas that depend on the dilaton covariantly under SL(2,Z): S-duality-covariant D-brane Yukawas. A literature search is needed before any claim.

## F7. Next runs
1. Departure from ρ: τ = ρ + ε along the inflaton's final approach. Does any ε (with C3/C4-type structures, or with weight-4/6 forms) give A = √2 and δ = 2/9 together with the correct ratios? This must be locked as a prediction with ε fixed by inflation (e.g. from reheating oscillation amplitude), not fitted, or it is only a fit.
2. Search for a dynamical reason for equipartition (an extremum of a modular-invariant function of √M).
3. Neutrinos and mixing angles at ρ (A4 with τ ≈ ρ is known to give near-tribimaximal patterns: check against current θ₁₂, θ₂₃, θ₁₃).
4. Strong CP: θ(τ) at ρ (Re τ = ½ ⇒ θ = 0 or π): which one, and whether it is acceptable.
5. F6 literature: S-duality-covariant Yukawas.

---

## Run 2 (D1596, locked PREREG_FLAV_RHO2) — F7 items 1, 3, 4, 5, plus 2 by search

### F7.1 Endpoint offset: ε = 0 [derived + computed]
V(ρ) = 2e-22 (numerical zero), and V(ρ ± 1e-3) ≈ 8.3e-8 in all four directions: ρ is a strict, nearly isotropic quadratic minimum. Because V₀ ∝ |∇ln E|² has a double zero at the fixed point, the tilt factor cannot move the minimum. Once the oscillations decay, inflation leaves τ **exactly** at ρ. So the Weave predicts ε = 0, and any flavour structure must work at exact ρ, where F2 showed the minimal A4 constructions fail. Masses need a second source of symmetry breaking; it cannot be a leftover offset from inflation.

### F7.3 Neutrinos: tribimaximal at ρ — FAIL (locked)
Residual Z₃ of the charged leptons at ρ with A4 gives tribimaximal mixing. Pulls against NuFIT 6.0 (normal ordering):
| angle | TBM | NuFIT 6.0 | pull |
|---|---|---|---|
| sin²θ₁₂ | 1/3 | 0.307 (+0.012/−0.011) | +2.2σ |
| sin²θ₁₃ | 0 | 0.02195 (+0.00054/−0.00058) | **−38σ** |
| sin²θ₂₃ | 1/2 | 0.561 (IC19) / 0.470 (IC24) | −4.1σ / +1.8σ |
Exact-ρ A4 neutrino mixing is excluded by θ₁₃. A correction sector is required, the same conclusion as in the modular-flavour literature.

### F7.4 Strong CP: θ = π at ρ — FAIL as it stands (locked)
If the QCD θ-angle is 2π Re τ (gauge kinetic function f = τ), then ρ (Re τ = ½) gives θ = π, which is CP-conserving. But leading-order chiral perturbation theory gives m_π(π)/m_π(0) = 0.616, 0.600, 0.585 for m_u/m_d = 0.45, 0.47, 0.49. Lattice QCD at θ = 0 already reproduces the observed pion, so θ̄ = π is excluded.
Rescue condition [derived]: θ̄ = θ − arg det(Y_u Y_d) = 0 requires **arg det(Y_u Y_d)(ρ) = π (mod 2π)**. This is a sharp, checkable condition on the quark Yukawas at ρ. If it holds, the strong CP problem is solved by the inflation endpoint. It must be tested on an explicit quark sector.

### F7.5 Same-τ question: obstructed in known constructions [literature]
In explicit string realisations of modular flavour (e.g. fluxed F-theory GUTs, arXiv:2407.06618), the flavour modulus is a complex-structure modulus of the matter curves, not the axio-dilaton. That paper also notes that "S-duality symmetry is broken by the Yukawa lagrangian" unless the wavefunctions carry the right g_s dependence.
⇒ Revised unification route [POSTULATE P-F2, candidate]: the flavour modulus is a separate SL(2,Z) field, and the **same Zhinü principle** acts on it, so it also ends at its own ρ. "Unified" then means one principle and one endpoint shared by all SL(2,Z) moduli, not one field.

### F7.2 Equipartition dynamics [literature]
Sumino's family-gauge-symmetry mechanism (arXiv:0812.2090, 0903.3640) protects Koide's relation against radiative corrections. It does not by itself derive A = √2. No derivation of equipartition was found.

### Overall verdict after runs 1–2
- **Derived:** the Koide form as the Z₃ spectrum; the condition Q = 2/3 ⇔ equipartition; ε = 0 at the inflation endpoint; the strong-CP rescue condition arg det(Y_u Y_d)(ρ) = π.
- **Failed (locked):** minimal A4 masses at exact ρ; tribimaximal mixing (θ₁₃, −38σ); θ = π without a quark-phase compensation.
- **Open:** a source for equipartition and δ = 2/9; a correction sector for θ₁₃; an explicit quark sector to test arg det = π; P-F2, the shared principle across moduli.
Flavour is NOT fully derived. The parts that are derived are listed above, and the minimal "everything at exact ρ" version is ruled out by data in two places.
