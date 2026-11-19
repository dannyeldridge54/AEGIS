# SERAPIS — FINAL EQUATION (v3, 19 Nov 2026, D1527–D1593)

Tags: [lit] literature · [der] derived and checked here · [est] estimate · [PRINCIPLE] assumed founding statement.
This is the finalised form. It enters the model ladder only with Danny's yes. Nothing here is published (no Zenodo without "Publish").

---

## 1. The equation

    S = ∫ d⁴x √−g [ ½ M_P² R − ½ (∂ψ)² − V(ψ) ]

    V(ψ) = V∞ · ( (2/3) · y ∂_y ln E(τ, 3/2) )² · [ 1 + C · ( E(τ, 3/2) − E(ρ, 3/2) ) ]

    τ = ½ + i y,   y = e^{β_D ψ / 2},   β_D = √(D − 2),   ρ = e^{iπ/3}

    E(τ, 3/2) = Σ'_{(m,n)} (Im τ)^{3/2} / |m + nτ|³ = 2ζ(3) y^{3/2} + 4ζ(2) y^{−1/2} + (D-instanton terms)

Two numbers fix everything: C (the tilt) and D (the dimension of the effective theory when the CMB scales leave the horizon).
V∞ is set by the CMB amplitude.

Equivalent forms (Λ_QG = M_P E^{−1/6}, λ_sp = 1/√8):

    V = V∞ · |∇ln Λ_QG|² / λ_sp² · [1 + C(Λ_QG^{−6} − Λ_QG(ρ)^{−6})]
      = V∞ · ( 1/3 + (4/3) ∇² ln Λ_QG ) · [1 + C(…)]
    V ≈ V∞ [ 1 − 7.30 e^{−β_D ψ} ] + tilt,   7.30 = 16ζ(2)/(3ζ(3))

In words: **the inflaton is the string coupling; inflation is the cutoff of quantum gravity (the species scale) running at its maximal rate; the universe stops inflating at the self-dual point ρ where weak- and strong-coupling pushes cancel; the one-loop α′³ correction tilts it into the observed band; the dimension at horizon exit is written into r.**

## 2. Founding principle (the one assumed step)

**Species-gradient principle [PRINCIPLE]:** along the string-coupling direction, the vacuum energy is the squared running rate of the quantum-gravity cutoff, normalised to its asymptotic rate:

    V₀ = V∞ · |∇ ln Λ_QG|² / λ_sp²

Status: same form as the Casas–Ibáñez one-loop tower potential (2507.05345; 2604.27835 eq. 29); its prefactor is not flat along the dilaton in 4D N = 1 supergravity (D1541, D1543, D1583–D1584) and the 6D one-loop is Casimir-type (D1592). The principle is therefore assumed, as in any effective theory, and is the single statement a future string calculation must derive. Everything else follows from it.

## 3. Derivation (given the principle)

| step | statement | status |
|---|---|---|
| 1 | kinetic term R/2 − (2/(D−2))(∂φ_D)²; ψ = 2φ_D/√(D−2) | [lit, der; checked 10D and 4D] |
| 2 | Λ_QG = M_P E(τ,3/2)^{−1/6}; slope → 1/√8 | [lit 2310.07708; der: 0.355352 at y = 1000] |
| 3 | V₀ = V∞|∇ln Λ|²/λ_sp² | [PRINCIPLE] |
| 4 | V₀/V∞ = 1/3 + (4/3)∇² ln Λ (from Δ E = ¾E, ∂ₓE = 0) | [der; 6-decimal check] |
| 5 | V₀/V∞ → 1 − 7.30 y^{−2}; rung k = 2 | [der; 7.2983] |
| 6 | V₀(ρ) = 0 (SL(2,Z) self-dual point) | [der; 3e-19] |
| 7 | tilt C = wχ/(4(2π)³𝒱) from BBHL α′³ (blue for χ > 0) | [est D1566, D1565a] |
| 8 | 10D (E_{3/2}) and 8D (E_2) lenses give identical untilted inflation | [der D1552, D1559] |
| 9 | across 13 dimension lenses + E₈/E₉/E₁₀ the coupling direction is the only rung | [lit + est D1568–D1582] |
| 10 | r = 8/((D−2)N²), n_s = 1 − 2/N − 3/((D−2)N²) untilted | [der D1588; run D1589] |

## 4. Predictions

| | D = 10 (10D lens) | D = 6 (6D phase at horizon exit) |
|---|---|---|
| C | 8.0 × 10⁻⁷ | 2.64 × 10⁻⁶ |
| n_s | 0.97065 | 0.9706 |
| r | 5.41 × 10⁻⁴ | 1.07 × 10⁻³ |
| α_s | −9.7 × 10⁻⁴ | −9.4 × 10⁻⁴ |
| N* | 50.37 | 50.57 |
| status | exact Mukhanov–Sasaki (D1532) | exact Mukhanov–Sasaki (D1593): n_s 0.97056, r 1.069e-3, α_s −9.6e-4 |
| volume 𝒱 (χ = 20–200) | 1.4e4 – 3e5 | ≈ 4e3 – 9e4 |

Node ladder (r at n_s ≈ 0.9706, scaled 8/(D−2)): 10D 5.4e-4 · 9D 6.2e-4 · 8D 7.2e-4 · 7D 8.7e-4 · 6D 1.07e-3 · 5D 1.4e-3 · 4D 2.2e-3.

Data: n_s between CMB-SPA (0.9684 ± 0.0030) and CMB-SPA+DESI (0.9728 ± 0.0027); r ≪ 0.036. Test: a CMB-S4/LiteBIRD-class r measurement reads off D.

Default (the finalised choice): **D = 10** — the only case with an exact Mukhanov–Sasaki confirmation and a consistent end of inflation at ρ. D = 6 is kept as the alternative node: its end of inflation needs the 6D → 4D transition (the perturbative 6D slice stops at V₀ = 1/9, D1592) and its mechanism is open.

## 5. Checks passed

Identity (6 decimals, 4 points); 7.2983; V₀(ρ) = 3e-19; 1/√8 slope; kinetic normalisation (10D, 4D); r-scaling with D (ratio 1.98 vs 2); primary species bound Λ_s ≥ √V/M_P holds by ×7.7e4 at horizon exit; gap g_s² at every dimension lens.

## 6. Known limits (stated, not hidden)

1. Step 3 is a principle, not a derivation (§2).
2. The tilt needs a compactification with χ > 0 and 𝒱 ~ 10⁴–10⁵ (estimate level).
3. The gradient form of Andriot's bound is violated ×42 — the same tension every plateau has with the dS-slope conjecture (flag, not veto).
4. Heterotic lenses R3–R6 are by analogy; one-loop signs at 6D/5D/4D are regularised (D1572a, D1577a).
5. D = 6 exact-MS confirmation: DONE (D1593) — n_s 0.97056, r 1.069e-3; engine F agreed to 4e-5 in n_s and 0.1 % in r.
