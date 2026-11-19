# THE WEAVE — full equation (v1, 19 Nov 2026, D1527–D1597)

Tags: [der] derived and checked · [lit] literature · [P] principle, assumed · [EMP] empirical, not yet derived · [OPEN] missing term.
Nothing here is published. Ladder entry only with Danny's yes.

## The equation

    L = ½ M_P² R
        − Σ_a |∂τ_a|² / (4 (Im τ_a)²)                              (thread fields: τ₁ = string coupling, τ_f = flavour modulus)
        − V(τ₁)                                                    (SERAPIS-Λ, inflation)
        − [ ē_L √M_ℓ(τ_f)² e_R  +  quarks Y_u, Y_d(τ_f)  +  neutrinos ]   (flavour)
        + (θ̄ / 32π²) G G̃                                         (strong CP)
        + Λ_obs                                                     (dark energy, OPEN)

### 1. Inflation — SERAPIS-Λ
    V(τ₁) = V∞ ( ⅔ y∂_y ln E(τ₁, 3/2) )² [ 1 + C (E − E_ρ) ],   E = 2ζ(3)y^{3/2} + 4ζ(2)y^{−1/2} + …,   y = e^{β_D ψ/2}, β_D = √(D−2)
- Plateau 1 − 7.30 e^{−β_D ψ}; identity V₀ = V∞(⅓ + (4/3)∇² ln Λ_QG). [der]
- Founding rule: V₀ = V∞|∇ln Λ_QG|²/λ_sp² (Zhinü). [P]
- Tilt C = wχ/(4(2π)³𝒱). [lit + est]
- Predictions: D = 10: n_s 0.97065, r 5.41e-4; D = 6: n_s 0.97056, r 1.069e-3 (both exact Mukhanov–Sasaki). [der]

### 2. Endpoint — every thread tied off at ρ
- τ₁ → ρ = e^{iπ/3} exactly: V(ρ) = 0 and a strict quadratic minimum, so ε = 0. [der: V(ρ) = 2e-22; V(ρ ± 10⁻³) ≈ 8.3e-8 isotropic]
- τ_f → ρ by the same rule acting on the flavour modulus (P-F2). [P]
- At ρ a residual Z₃ survives. [lit]

### 3. Charged leptons — Koide from the Z₃ at ρ
    √M_ℓ = a·1 + b·C + b̄·C²   (C = cyclic shift; forced by the residual Z₃)          [der]
    √m_k = a + 2|b| cos(δ + 2πk/3)                                                    [der]
    Q = ⅓ + ⅔ |b|²/a²
    |b|² = a²/2  (Z₃ equipartition, P-F1)  ⇒  Q = 2/3                                  [P]
    δ = 2/9                                                                           [EMP]
Check (m_τ as the only input; A = √2, δ = 2/9):
| m_τ input (MeV) | predicted m_μ | predicted m_e |
|---|---|---|
| 1776.93 (PDG, recalled) | 105.6561 | 0.510983 |
| 1777.09 (Belle II 2023) | 105.6657 | 0.511029 |
| observed | 105.6584 | 0.510999 |
Agreement is within the m_τ uncertainty. The two numbers √2 and 2/9 are not derived yet.

### 4. Neutrinos — the second tie-off point (D1598, D1599)
V₀ vanishes at BOTH SL(2,Z) fixed points, i and ρ. [der] With charged leptons tied off at ρ (residual Z₃) and the neutrino modulus at i (residual Z₂; P-F3), A4 makes the second PMNS column exactly trimaximal, (1/3, 1/3, 1/3): this is TM2. [der]
- θ₁₃ is free, which removes the −38σ failure of exact-ρ tribimaximal mixing.
- sin²θ₁₂ = 1/(3cos²θ₁₃) = 0.3408 vs NuFIT 0.307: +2.8σ (passes the 3σ rule, in tension). [der]
- sin²θ₂₃ ∈ [0.395, 0.605] (data 0.561 / 0.470: consistent). [der]
- **Prediction:** δ_CP = 236° or 125° (if sin²θ₂₃ = 0.561), 287° or 74° (if 0.470). Scored on DUNE / Hyper-K. [der]

### 5. Strong CP
    θ = 2π Re τ = π at ρ;   θ̄ = π − arg det(Y_u Y_d)(ρ)
θ̄ = 0 ⇔ arg det(Y_u Y_d)(ρ) = π (mod 2π). [der condition] θ̄ = π alone is excluded (m_π ratio 0.60). Needs an explicit quark sector. [OPEN]

### 6. Vacuum energy
The inflation sector gives exactly 0 at ρ. [der] The observed Λ_obs ≈ 10⁻¹²⁰ M_P⁴ is not explained. [OPEN]

## Derivation status

| piece | status |
|---|---|
| inflation shape, identity, plateau, endpoint, ε = 0, r-by-dimension, predictions | derived and checked |
| Koide form (Z₃ circulant), Q ⇔ equipartition, θ̄ condition | derived |
| Zhinü rule (inflation) | principle P |
| equipartition √2 (flavour) | principle P-F1 |
| same principle on the flavour modulus | principle P-F2 |
| δ = 2/9 | empirical; holds as δ = Q/3 to ~1σ (D1598), so one principle (equipartition) would fix both Koide numbers |
| neutrino modulus at i | principle P-F3 |
| quark sector (θ̄ condition), Λ_obs | open terms |
| neutrino mixing | derived (TM2) given P-F3; sin²θ₁₂ in +2.8σ tension |

The equation is complete as a statement: every term is written, every number that can be computed has been computed, and the data checks are passed or failed on the record. It is not yet fully derived: three principles and one empirical number carry it, and three terms are open. The next derivation targets, in order of leverage:
1. one rule that gives both Zhinü and equipartition (both are equalities of norms at the symmetric point);
2. δ = 2/9 from the geometry at ρ;
3. the θ₁₃ correction and the quark-phase condition.
