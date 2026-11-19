# SERAPIS P3 — the full equation and its derivation (v2, clean pass, 19 Nov 2026 11:35 CT; D1527–D1590)

Status tags: [lit] literature · [der] derived/computed here · [est] estimate · [POSTULATE] not derived.
P3-S and P3-D are candidates. Neither enters the ladder without Danny's yes.

## 1. The equation (one form, one free dimension label D)

Fields: the D-dimensional string coupling φ_D at horizon exit; in 10D variables this is the axio-dilaton τ = x + iy on the line x = ½.
Canonical inflaton ψ = 2φ_D/√(D − 2), from the Einstein-frame kinetic term R/2 − (2/(D−2))(∂φ_D)².

    V = V∞ · ( (2/3) · y∂_y ln E(τ,3/2) )² · [ 1 + C · ( E(τ,3/2) − E(ρ,3/2) ) ] ,   y = e^{β_D ψ / 2},  β_D = √(D − 2)

    E(τ,3/2) = 2ζ(3) y^{3/2} + 4ζ(2) y^{−1/2} + (D-instanton terms) ,   ρ = e^{iπ/3}

Species form: Λ_QG = M_P E^{−1/6}, λ_sp = 1/√8:

    V = V∞ · |∇ln Λ_QG|²/λ_sp² · [1 + C(…)] = V∞ · ( 1/3 + (4/3)∇² ln Λ_QG ) · [1 + C(…)]

Plateau limit:  V ≈ V∞ [ 1 − 7.30 · e^{−β_D ψ} ]  (+ tilt),  7.30 = 16ζ(2)/(3ζ(3)).

- D = 10 → β = 2√2: candidate **P3-S** (10D lens; the original).
- D = 6 → β = 2: candidate **P3-D** (6D at horizon exit; the loop prefactor is exactly flat there, §3 step 3b).

## 2. Clean-pass checks (run 11:35 CT, repo E function)

| check | result |
|---|---|
| identity V₀ = 1/3 + (4/3)∇² ln Λ (∇² = 2y²(∂ₓ² + ∂ᵧ²)) | equal to 6 decimals at y = 1.2, 3, 10, 40 ✓ |
| ∂ₓ ln E on x = ½ | 0 ✓ (symmetry x → 1 − x) |
| plateau coefficient | 7.2983 ✓ ; 1 − V₀(40) = 0.004548 vs 7.30/1600 = 0.004561 ✓ |
| anchor V₀(ρ) | 3e-19 ✓ (exact zero) |
| species slope | 0.35342 (y = 100), 0.355352 (y = 1000) → 1/√8 = 0.353553 ✓ |
| kinetic normalisation 2/(D−2) | 10D: ¼ ✓ (our φ = ln y/√2); 4D: 1 ✓ (= K = −ln(S + S̄), s = e^{−2φ₄}) |
| r scaling 8/((D−2)N²) | 6D locked run / 10D run = 1.98 vs 2 ✓ (D1589) |

## 3. Derivation chain

1. Kinetic term — string coupling of the D-dimensional theory; normalisation checked above. [lit + der]
2. Cutoff — Λ_QG = M_P E^{−1/6}, slope → 1/√8. [lit 2310.07708; der]
3. Plateau form — V ∝ g²·m_3/2²·|∇ln Λ|²: the Casas–Ibáñez one-loop tower potential (2507.05345; review 2604.27835 eq. 29). [lit]
   3a. Its prefactor must be flat along the inflaton (|q| ≲ 0.03, D1541). In 4D it is not: constant W ⇒ bump; flux W ⇒ rises y^{1/2} (D1543, D1583). Correlated volume–dilaton paths (P3-V) fail: LVS volume is exponential in 1/g_s, KKLT logarithmic (D1583a, D1584).
   3b. The loop factor scales as g_s^{(D−2)/4} [der D1586]; with the flux gravitino mass the prefactor goes as y^{(6−D)/4}: flat **exactly at D = 6** [est — mixes a 4D m_3/2 scaling with a 6D loop factor; needs a 6D supergravity treatment].
   ⇒ The plateau form is now "one-loop tower potential with a prefactor that is flat if horizon exit happens in a 6D phase". Still a POSTULATE (P3-L/P3-D) until 3b is done properly.
4. Identity V₀/V∞ = 1/3 + (4/3)∇² ln Λ — from Δ_hyp E = ¾E and ∂ₓE = 0. [der, checked]
5. Plateau limit 1 − 7.30 y^{−2}: approach exponent k = 2 (the rung). [der, checked]
6. Anchor — ρ is SL(2,Z) self-dual ⇒ V₀(ρ) = 0; the weak- and strong-coupling pushes cancel there (D1585). [der, checked]
7. Tilt — BBHL α'³: C = wχ/(4(2π)³𝒱), blue for χ > 0. [est D1566, D1565a]
8. Lens/helix — 10D (E_{3/2}) and 8D (E_2) strands give the same untilted inflation; only rung 1 in band. [der D1552, D1559]
9. Dimension twin ladder — across 6 type II + 6 heterotic lenses + 4D centre + E₈/E₉/E₁₀, the coupling (species) direction is the only rung; tree/one-loop gap g_s² at every level. [lit + est D1568–D1582; heterotic R3–R6 by analogy]
10. Observer nodes — r depends only on the dimension at horizon exit: r = 8/((D−2)N²) untilted. [der D1588, run D1589]

## 4. Predictions

Untilted: n_s = 1 − 2/N − 3/((D−2)N²), r = 8/((D−2)N²).

| | P3-S (10D lens) | P3-D (6D at horizon exit) |
|---|---|---|
| tilt C for n_s = 0.9706 | 8 × 10⁻⁷ | 2.6 × 10⁻⁶ |
| n_s | 0.97065 | 0.9706 |
| r | 5.41 × 10⁻⁴ (exact MS) | 1.07 × 10⁻³ (engine F, proxy) |
| α_s | −9.7 × 10⁻⁴ | −9.4 × 10⁻⁴ (interp.) |
| N* | 50.37 | 50.57 |
| volume 𝒱 (χ = 20–200) | 1.4e4 – 3e5 | ≈ 4e3 – 9e4 [est] |
| prefactor flat? | no (needs P3-L as postulate) | yes at leading order (3b) [est] |

Node ladder (r at n_s ≈ 0.9706; 10D, 6D computed, others scaled 8/(D−2)): 10D 5.4e-4 · 9D 6.2e-4 · 8D 7.2e-4 · 7D 8.7e-4 · 6D 1.07e-3 · 5D 1.4e-3 · 4D 2.2e-3. Parent theory (all circles T-dualised) alternates IIB/IIA level by level; 6D is the only node with zero prefactor push and a chiral (IIB) parent (D1590).

Data: both n_s sit between CMB-SPA (0.9684 ± 0.0030) and CMB-SPA+DESI (0.9728 ± 0.0027). r = 5.4e-4 vs 1.07e-3 is a factor-2 split that a CMB-S4/LiteBIRD-class σ(r) ~ 5e-4 – 1e-3 can begin to separate.

## 5. Does it work? (verdict of the clean pass)

- The mathematics of the equation is consistent: every identity and limit checks numerically (§2), and the r-scaling with dimension is confirmed by a locked run.
- The phenomenology works for both candidates: in band with one tilt number.
- What changed today: the open step 3 now has a concrete route (3b, 6D phase) instead of only a no-go — that is the main improvement. P3-D makes the plateau's prefactor flat without tuning and gives a distinct, testable r.
- It does NOT yet work as a derivation, because:
  1. step 3b mixes levels (4D gravitino scaling × 6D loop factor) — needs a 6D (1,0) supergravity calculation of the tower loop;
  2. a 6D phase at horizon exit needs two internal dimensions with M_KK < H, i.e. an anisotropic compactification; consistency with the smaller P3-D volume is plausible at order of magnitude (M_s/H ≈ 7–31 ⇒ two dimensions ≳ 7–31 string lengths) but not shown;
  3. the 6D run used the 10D species function with 6D normalisation (proxy); the true 6D codon E^{SO(5,5)}_{3/2} has a one-loop coefficient whose sign is open (regularised; corrections D1572a/D1577a);
  4. the Andriot-type rate flag (D1527) applies to both candidates;
  5. chirality → parity-odd tensors is a lead only (D1590).

## 6. Corrections made today
D1583a (LVS volume exponential, not power-law), D1572a / D1577a (5D one-loop also regularised; sign open), L6 eigenvalue −42 (working figure −21/2 never filed).

## 7. Open items worked (D1592, 11:40 CT)
1. 6D tower loop — in 6D SUSY the one-loop is Casimir-type (M⁶, M⁴, M² terms cancel per supermultiplet; hep-th/0504004) ⇒ the 4D Casas–Ibáñez prefactor does not carry over; step 3b is downgraded to an observation. P3-D stands only as "6D phase at horizon exit ⇒ r ×2"; its mechanism is OPEN.
2. Anisotropic compactification — exists (LVS on K3-fibred CY, two large P¹-base dimensions; 2606.19440, 1105.2107); P3-D's volume overlaps it only at the low end (≈ 4–5e3) [est].
3. 6D one-loop sign — positive at large volume [est]; then the perturbative 6D slice never ends inflation (1 → 1/9): the end must come from non-perturbative terms or the 6D → 4D transition.
4. Andriot flag — the gradient bound inherits the dS-slope conjecture and is asserted only asymptotically; the primary bound Λ_s ≥ √V/M_P holds by ×7.7e4 at horizon exit.
