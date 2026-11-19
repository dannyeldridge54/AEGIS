# SERAPIS P3-S — the full equation and its derivation (19 Nov 2026, D1527–D1582)

Status tags: [lit] literature · [der] derived/computed here · [est] estimate · [POSTULATE] not derived.
P3-S remains a candidate — it does not enter the ladder without Danny's yes.

## 1. The full equation

Action (4D Einstein frame, M_P = 1, axio-dilaton τ = x + iy, inflation on the x = ½ line):

    S = ∫ d⁴x √−g [ ½R − ∂τ∂τ̄ /(4y²) − V(τ) ] ,   canonical field φ = (ln y)/√2   (y = e^{√2 φ})

Potential:

    V(τ) = V∞ · ( (2/3) · y ∂_y ln E(τ, 3/2) )² · [ 1 + C · ( E(τ,3/2) − E(ρ,3/2) ) ]

    E(τ,3/2) = 2ζ(3) y^{3/2} + 4ζ(2) y^{−1/2} + (D-instanton terms e^{−2π|n|y})      (IIB R⁴ coefficient)
    ρ = e^{iπ/3} (y_ρ = √3/2),   C = w·χ / (4(2π)³ 𝒱),   w = 1 (F-term) or 2/3 (D7 D-term)

Same thing in species language (Λ_QG = M_P · E(τ,3/2)^{−1/6}, λ_sp = 1/√8):

    V = V∞ · |∇ln Λ_QG|² / λ_sp² · [1 + C(Λ_QG^{−6} − Λ_QG(ρ)^{−6})]
      = V∞ · ( 1/3 + (4/3) ∇² ln Λ_QG ) · [1 + C(…)]

Large-field form (the inflationary plateau):

    V ≈ V∞ [ 1 − (16ζ(2)/3ζ(3)) y^{−2} ] = V∞ [ 1 − 7.30 · e^{−2√2 φ} ]  (+ the C tilt)

## 2. Derivation, step by step

1. Kinetic term — IIB axio-dilaton on the SL(2,Z)/U(1) upper half-plane. [lit]
2. Species scale — the R⁴ coefficient E(τ,3/2) sets the quantum-gravity cutoff Λ_QG = M_P E^{−1/6}; its asymptotic slope is
   |∂_φ ln Λ| → 1/√8 = λ_sp (checked: 0.3070, 0.3503, 0.3531, 0.3535 at y = 5, 20, 55.6, 200). [lit 2310.07708; der D1527]
3. Plateau shape — V₀ = V∞ |∇ln Λ|²/λ_sp²: the vacuum energy is set by how fast the cutoff runs, normalised to its asymptotic rate. [POSTULATE P3-L]
   Every supergravity route to derive it is obstructed (D1541, D1543, D1544, D1547, D1548, D1550). This is the one missing link.
4. Identity — because Δ_hyp E = ¾E and ∂_x E = 0 on x = ½:
   ∇² ln Λ = −(1/3)[¾ − (y∂_y ln E)²]  ⇒  1/3 + (4/3)∇² ln Λ = (4/9)(y∂_y ln E)² = V₀/V∞. [der]
5. Plateau limit — expand E: y∂_y ln E = 3/2 − 4(ζ(2)/ζ(3)) y^{−2} + … ⇒ V₀/V∞ = 1 − (16ζ(2)/3ζ(3)) y^{−2} = 1 − 7.30 y^{−2}. Approach exponent k = 2 (the "rung"). [der]
6. Anchor (end of inflation / vacuum) — ρ is a fixed point of SL(2,Z), so ∂E(ρ) = 0 ⇒ V₀(ρ) = 0 exactly. No tuning of the minimum. [der]
7. Tilt thread — the BBHL α'³ correction K = −2 ln(𝒱 + ξ̂/2), ξ̂ ∝ χ E(τ,3/2), makes the plateau's prefactor depend on τ by exactly the
   E_{3/2} tilt, with C = wχ/(4(2π)³𝒱). Blue (needed) for χ > 0. [est D1566, D1565a]
8. Lens / helix duality — the 10D gradient strand E_{3/2} and the 8D ratio strand E_2 give identical untilted inflation (Δn_s 3e-5, Δr 0.2 %);
   λ₈ = 3ζ(3)/(32ζ(2)ζ(4)) = 0.063298; only rung 1 (3/2 ↔ 2) is in band. [der D1552, D1559]
9. Dimension twin ladder — across all 13 lenses (6 type II, 6 heterotic, 4D centre) plus E₈/E₉/E₁₀, the string-coupling (species) direction is the
   ONLY direction carrying the k = 2 rung with tree/one-loop gap g_s² — the P3-S direction. [lit + est D1568–D1582]

## 3. Numbers

| quantity | value | source |
|---|---|---|
| plateau coefficient | 16ζ(2)/(3ζ(3)) = 7.30 | der |
| tilt band | C = 6.8–9.4 × 10⁻⁷ | der (engine F) |
| at C = 8 × 10⁻⁷ | n_s = 0.97065, r = 5.41 × 10⁻⁴, α_s = −9.68 × 10⁻⁴, N* = 50.37 | exact Mukhanov–Sasaki, D1532 |
| volume for the band | 𝒱 ≈ 1.4 × 10⁴ – 3 × 10⁵ (χ = 20–200) | est D1566 |
| string / KK scales | M_s ≈ 2–10 × 10¹³ GeV, M_KK ≈ 1.7–13 H | est D1566 |

Data check: n_s 0.97065 sits between CMB-SPA (0.9684 ± 0.0030) and CMB-SPA+DESI (0.9728 ± 0.0027); r far below 0.036.
Untilted rough guide: n_s ≈ 1 − 2/N, r ≈ 8/(8N²) = 1/N².

## 4. What is still open (honest list)

1. Step 3 (P3-L) — the plateau form is postulated, not derived. Main gap.
2. Andriot-type flag — |∇ln Λ|/|∇ln V| ≈ 42 at horizon exit vs his proposed bound (a proposal, not a theorem; must be answered in the paper). D1527.
3. Tilt sign — needs a compactification with χ > 0 and the D7 D-term prefactor (estimate level).
4. 4D one-loop coefficient at the edge s = 2 — sign open on both lenses (D1579).
