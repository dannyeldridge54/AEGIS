# THE WEAVE — full equation (v2, 19 Nov 2026 14:45 CT, D1527–D1616; adjusted after a review of all sources)

Tags: [der] derived and checked · [lit] literature · [P] principle, assumed · [EMP] empirical, not yet derived · [OPEN] missing term.
Published preprints (19 Nov 2026): inflation part doi:10.5281/zenodo.24377930 (v1.1: 24378141); flavour part doi:10.5281/zenodo.24377945 (v1.1: 24378142; v2: 24379357); Dimension Ladder doi:10.5281/zenodo.24378259. Ladder entry only with Danny's yes.

## The equation

    L = ½ M_P² R
        − Σ_a |∂τ_a|² / (4 (Im τ_a)²)          (threads: τ₁ = string coupling/inflaton; τ_ℓ = charged-lepton modulus; τ_ν = neutrino modulus; τ_q = quark modulus)
        − V(τ₁)                                                    (SERAPIS-Λ, inflation)
        − [ ē_L √M_ℓ(τ_ℓ)² e_R  +  ν: M_ν(τ_ν)  +  quarks Y_u, Y_d(τ_q) ]   (flavour)
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
- Lepton moduli feel the same potential (P-F2). Slow moduli drain to i for 69% of the domain and to ρ for 31% (D1610), so τ_ν → i is the natural outcome; τ_ℓ → ρ needs a start near the line x = ½. [der given P-F2]
- Smooth modular-invariant terms cannot move these minima, since every invariant function is stationary at i and ρ (D1614). A small offset, such as the fitted τ = 1.0685i of arXiv:2609.09262, needs a hidden term just past a SUPERCRITICAL bifurcation threshold (Δ ~ 10⁻³); the simplest candidate, −κy^{1/2}|η|², is subcritical and jumps to ρ instead (D1612, D1614a); the opposite sign, +κy^{1/2}|η|², IS supercritical: τ = 1.048i at 0.1% and 1.168i at 1% past threshold, |u| ≈ 0.77√Δ, so the fitted 1.0685i needs Δ ≈ 0.2% (D1618; CP-conserving, tuned, not predicted); the SM top loop cannot supply it, because that would need a ~10⁻⁵ eV modulus excluded by fifth-force tests (D1613). [der/est]
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
**Adjustment (D1615, D1616): pole masses.** Koide's 2/3 holds for pole masses to ~10⁻⁵ but is 0.6678 for running masses at M_Z (arXiv:2609.09262). Read the √M_ℓ above as the low-energy (pole-mass) matrix. If it comes from Yukawas at the modular scale, running corrections of ~10⁻³ must cancel, which is an open requirement. δ = 2/9 rad has no π, so it cannot come from the fixed-point symmetry; it must be dynamical. Chance level of the match ≈ 7 × 10⁻⁴ (look-elsewhere over simple fractions and π-multiples).

### 4. Neutrinos — the second tie-off point (D1598, D1599)
V₀ vanishes at BOTH SL(2,Z) fixed points, i and ρ. [der] With charged leptons tied off at ρ (residual Z₃) and the neutrino modulus at i (residual Z₂; P-F3), A4 makes the second PMNS column exactly trimaximal, (1/3, 1/3, 1/3): this is TM2. [der]
- θ₁₃ is free, which removes the −38σ failure of exact-ρ tribimaximal mixing.
- sin²θ₁₂ = 1/(3cos²θ₁₃) = 0.3408 vs NuFIT 0.307: +2.8σ (passes the 3σ rule, in tension). [der] Adjustment: near i, mixing angles move linearly with the offset x ~ |(τ − i)/(τ + i)| (Feruglio 2211.00659), so a small offset of τ_ν (the bifurcation above) is the natural place to relieve this tension. [OPEN] Locked test (D1621): the minimal A4 Weinberg operator FAILS at and near i (χ² > 2000; degenerate m₁ = m₂ at i). TM2 holds only for a generic S-invariant M_ν with non-degenerate masses, which needs extra operators with free coefficients.
- sin²θ₂₃ ∈ [0.395, 0.605] (data 0.561 / 0.470: consistent). [der]
- **Prediction:** δ_CP = 236° or 125° (if sin²θ₂₃ = 0.561), 287° or 74° (if 0.470). Scored on DUNE / Hyper-K. [der]

### 5. Strong CP and the CKM phase (D1600)
    θ = 2π Re τ = π at ρ;   θ̄ = π − arg det(M_u M_d)
At ρ the A4 Yukawa determinant is exactly real: det = 27/8. [der] ρ and i are CP-symmetric points. With CP-symmetric (real) couplings, θ̄ ∈ {0, π}; θ̄ = 0 is selected by a discrete sign choice, so the strong-CP angle is quantised, not tuned. [der]
But the same setting gives a CKM Jarlskog invariant J ≤ 5e-15, against the observed 3.1e-5: quark moduli at the tie-off points give no CP violation. [der, FAIL]
Resolution (D1601, imported from Feruglio–Strumia–Titov 2305.08908): take the quark sector on a third field τ_q with anomaly-free weights, A = Σ(2k_Q + k_u + k_d) = 0. Then det M_q is a real constant for any τ_q, so θ̄ = 0, and the CKM phase comes from a generic ⟨τ_q⟩ (off the CP-symmetric lines; their fit τ_q = 1/8 + i). [lit] The quark field is therefore NOT tied off at ρ or i; P-F2 holds for the lepton fields only. What fixes τ_q, and why A = 0, are open within the Weave. [OPEN] Structural no-go (D1619): any split at the tie-off points stays on a CP-symmetric line, so a CP-violating τ_q needs partial breaking of SL(2,Z) or a CP-odd moduli–matter coupling (cf. arXiv:2405.18813) — an input from outside the Weave's single principle.

### 5b. The Y-fork — "Genesis split" (D1605)
Along the inflaton line x = ½ the Zhinü potential is a valley near ρ (y < 0.954) but a ridge for 0.96 ≲ y ≲ 1.5–1.9: the thread splits at the end of inflation into two exits — stay on x = ½ → ρ, or fall to x = 0 → i. [der] The fork is in the last e-fold, so the CMB predictions are unchanged. If the thread exits to i: θ = 2π Re τ = 0 directly, and the endpoint symmetry is Z₂. Two-field dynamics (D1606, locked): the inflaton itself takes the ρ exit for every kick tested (δx up to 3e-2, far above its quantum spread). It crosses the ridge band at speed, so the inflaton endpoint stays ρ (θ = π, resolved by the anomaly-free quark weights, D1601). [der] The fork remains the natural place where a slower field, such as the neutrino modulus, can split off to i (a candidate mechanism for P-F3). [OPEN]

### 6. Vacuum energy
The inflation sector gives exactly 0 at ρ. [der] The observed Λ_obs ≈ 10⁻¹²⁰ M_P⁴ is not explained. [OPEN] Candidate P-Λ (D1622): the "reverse thread" — one dark dimension (R ≈ 7.4 μm today) whose Casimir energy λ_C/R⁴ with λ_C = 3ζ(5)/(2π)⁶ gives Λ_obs (Montero–Vafa–Valenzuela). Flag: H_inf ≈ 10⁴ × today's species scale, so R must have been far smaller during inflation (radion history needed). See WEAVE_RESEARCH_DE.md.

## Observables — where the equation meets data (source review, 19 Nov 2026)

| observable | Weave value | data / test | status |
|---|---|---|---|
| n_s | 0.97065 (D = 10), 0.97056 (D = 6) | SPA 0.9684 ± 0.0030 (Camphuis et al. 2506.20707): +0.75σ; SPA+DESI 0.9728 ± 0.0027: −0.80σ; SPA+BK 0.9682 ± 0.0032 (2512.10613): +0.77σ; SPA+BK+DESI 0.9728 ± 0.0029: −0.74σ | consistent |
| r | 5.41e-4 (D = 10), 1.069e-3 (D = 6) | r < 0.036 (BK); CMB-S4/LiteBIRD σ(r) ~ 5e-4 – 1e-3 | future test; reads D |
| α_s | −9.7e-4 / −9.6e-4 | far below current σ | future |
| TCC (r < 1e-30) | violated | conjecture (1909.11106) | flag |
| Koide Q (pole) | 2/3 (P-F1) | 0.6666735 ± 0.0000077 (Belle II m_τ) | consistent; running caveat |
| Koide δ | 2/9 (EMP) | 0.2222136 ± 0.0000095 | consistent; σ(m_τ) → 0.05 MeV sharpens to 3.5e-6 |
| sin²θ₁₂ | 0.3408 (TM2) | 0.307 (+0.012/−0.011) NuFIT 6.0 | +2.8σ tension |
| sin²θ₂₃ | 0.395–0.605 | 0.561 / 0.470 | consistent |
| δ_CP | 236° or 125° (s²₂₃ = 0.561); 287° or 74° (0.470) | DUNE, Hyper-K | prediction |
| θ̄ | 0 (quantised at ρ; FST weights) | |θ̄| < 1e-10 | consistent by construction |
| CKM J | from generic τ_q (FST) | 3.1e-5 | imported |
| Λ_obs | not explained | 10⁻¹²⁰ M_P⁴ | open |

Sources reviewed: Camphuis et al. 2506.20707; 2512.10613; 2510.18656; NuFIT 6.0 2410.05380; Belle II 2305.19116; arXiv:2609.09262; Feruglio 2211.00659; Novichkov–Penedo–Petcov 2101.08718 and 2102.07488; Feruglio–Strumia–Titov 2305.08908; Casas–Ibáñez 2507.05345; Ibáñez 2604.27835; Castellano–Herráez–Ibáñez 2310.07708; van de Heisteeg et al. 2310.07213; Andriot 2305.07480; TCC 1909.11106/2001.00043; Green–Russo–Vanhove 1001.2535, 1004.0163; Obers–Pioline hep-th/9903113; Fleig–Kleinschmidt 1204.3043; Conlon–Pedro 0704.0737; SLED hep-th/0504004; 2606.19440.

## Derivation status

| piece | status |
|---|---|
| inflation shape, identity, plateau, endpoint, ε = 0, r-by-dimension, predictions | derived and checked |
| Koide form (Z₃ circulant), Q ⇔ equipartition, θ̄ condition | derived (the Q ⇔ 45°/equipartition algebra is known: Foot; preprint 202606.2124 — ours is the dynamical Z₃ from ρ) |
| Zhinü rule (inflation) | principle P |
| equipartition √2 (flavour) | principle P-F1 |
| same principle on the flavour modulus | principle P-F2 |
| δ = 2/9 | empirical; δ = Q/3 is the same statement; cannot come from fixed-point symmetry (D1616); chance ≈ 7e-4 |
| neutrino modulus at i | NATURAL OUTCOME (D1607/D1610): a slow modulus on the same potential drains to i for 69% of the domain; P-F3 reduced to "the neutrino modulus is slow and obeys the same potential" |
| candidate unifier P-W: s = 3/2 gives Q = 1/s, δ = 1/(3s), and the 1/3 of the Zhinü identity | pattern only (numerology risk), D1603; tested D1604: five locked E(τ,3/2) orbit constructions do NOT produce N_eff = 3/2 at any distinguished point |
| CKM phase with θ̄ = 0: mechanism imported (anomaly-free weights, generic τ_q); its Weave origin open; Λ_obs open | open terms |
| θ̄ quantised to {0, π} at ρ | derived |
| neutrino mixing | derived (TM2) given P-F3; sin²θ₁₂ in +2.8σ tension |

The equation is complete as a statement and adjusted to the reviewed sources: every term is written, every computable number computed, and each data check recorded as passed or failed. Carried by: the Zhinü principle; P-F1 (equipartition, read for pole masses); P-F2 (lepton moduli feel the same potential, which makes neutrinos-at-i natural); FST anomaly-free quark weights with a generic τ_q; δ = 2/9 (empirical). Open: the small offsets from the fixed points (bifurcation, D1614); the sin²θ₁₂ tension (offset of τ_ν); what stabilises τ_q; Λ_obs. Closed routes this session: SM-loop offset (D1613); invariant-term offset (theorem, D1614); a single rule for Zhinü + equipartition via E(τ,3/2) orbits (D1604, D1615); δ from fixed-point geometry (D1616).
