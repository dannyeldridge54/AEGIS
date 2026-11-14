# Twist-2: one no-scale field for inflation and the vacuum energy, with thermal capture, gauge-decay pinning and pre-registered null tests

**Danny Lee Eldridge** (independent researcher) · Version 1, 14 November 2026 · AI-assisted (see Acknowledgements)

## Abstract

We present Twist-2, a revision of the "Twist" model in which a single no-scale supergravity field T = x + iy, with K = −3 ln(T + T̄),
drives Starobinsky-class inflation and, after a kination phase, is captured at a point x_E ≈ 29.6 where its residual potential sets the
vacuum energy (w = −1). Capture uses light charged states χ that trap the field thermally as it rolls past the enhanced-symmetry point; a χ
condensate then gives the field a mass, and the field decays at gauge strength, so the capture costs no entropy (dilution D ≈ 1). The
remaining sectors are thermal leptogenesis, a separate light axion for cosmic birefringence, and gravity-only dark matter of 100–200 TeV.
Every computation was pre-registered (rule and hash committed before running). The main result is mixed and stated plainly. A joint fit of
CMB (Planck low-ℓ, ACT DR6, SPT-3G), DESI DR2 BAO and Pantheon+ rejects the undeformed model's spectral index n_s = 0.9651 by Δχ² = 7.95
(≈2.8σ), and letting dark energy thaw does not help: the preferred n_s stays at 0.9736. One tiny holomorphic deformation of the
superpotential (ε = 3.0×10⁻⁷, Kähler potential unchanged) fits n_s = 0.9736, after which every data block fits better than ΛCDM; n_s is then
a fit, and the inflation predictions become r = 0.0046 and α_s = −7.7×10⁻⁴, with r about twice the plain-Starobinsky value at the same n_s.
Other predictions: extra radiation ΔN_eff ≈ 0.05–0.10, a light gravitino ≤ 4.7 eV, no variation of α after capture, and a reionization-to-
recombination birefringence ratio below one for a birefringence axion heavier than ~20 H₀. We also list the model's string-theory weak
points (trans-Planckian censorship, a de Sitter minimum, control at small volume, and no derived origin for the capture coupling).

## 1. What changed from the Twist v5

The Twist v5 (Zenodo concept DOI 10.5281/zenodo.24202420) let the same field keep rolling today as thawing dark energy. That is excluded:
a field with K ⊃ −k ln(X + X̄) shifts the Standard Model gauge couplings at one loop, d ln α_em/d ln x = 7.0×10⁻³ (k/3), and a DESI-like
roll then violates clock and equivalence-principle bounds by ~10⁶ (companion paper, DOI 10.5281/zenodo.24232382). Twist-2 therefore stops
the field before nucleosynthesis and keeps one field only for inflation and the vacuum energy.

## 2. The model

K = −3 ln(T + T̄) + (matter with modular weights), W ⊃ S·F(T) + λ M_P (T − T_E) χχ̄ + ½ M_R N N + y_ν L H N, with
F(T) = (T + ε)/√(1 + T/μ) · exp[−n(1 − e^(−T/m₂))], μ = 1, m₂ = 4/π. The cliff factor gives a plateau for inflation at small x and an
exponentially small residual at large x; Λ = V(x_E) ∝ e^(−2n) with n ≈ 124.1. A light axion a with a photon coupling (c_γ α/8π)(a/f)FF̃ gives
birefringence; a gravity-only fermion ψ is the dark matter; SUSY breaking is in an x-independent sector with an eV-scale gravitino.

## 3. Cosmic history (all numbers from locked runs)

| Stage | Result | Ref. |
|---|---|---|
| Inflation (undeformed) | N* = 57.2 (instant 55.7 + kination 1.5), n_s 0.9651, r 0.0036 | D391 |
| Kination | x's kinetic share Ω_kin = 0.70 at T = 2×10¹³ GeV; dominates for ~3.5 e-folds; x ≈ 3 at matter freeze-out | D367c |
| Free roll | x stops by friction at x ≈ 29.81–29.83 | D367c, D390 |
| Capture | thermal χ trap at x_E ≈ 29.6, crossed at T ≈ 1.5×10¹¹ GeV; trapped in all scan points (kinetic/barrier 0.002–0.015); residual amplitude 10⁻¹⁴–10⁻¹⁰ M_P | D396 |
| Pinning and decay | χ condensate (v ~ 10⁹–10¹¹ GeV) gives m_x = g v; decay at gauge strength, T_d ≈ 10⁹–10¹³ GeV; dilution D = 1.000 | D407 |
| Leptogenesis | thermal N₁, M₁ ∈ [10⁹, 2.5×10¹³] GeV, ample room | D394, D411 |
| Dark matter | 100–200 TeV gravity-only fermion; cold (non-relativistic by T ≈ 1–2 TeV) | D112, D415 |
| Vacuum energy | Λ ∝ x_E^(−0.97): pinning point needs no tuning (29.6 → 29.83 changes Λ by 0.75%) | D413 |

Without the gauge decay the pinning would dilute everything by D ≈ 5–900 and shorten N* by ⅓ ln D, cancelling the kination gain (D406); the
gauge decay removes this (D407). The decay products, a hidden vector-like pair, are dark radiation.

## 4. Predictions

| Observable | Twist-2 | Status / test |
|---|---|---|
| n_s | 0.9651 (undeformed) / 0.9736 fitted (ε = 3.0×10⁻⁷) | undeformed rejected at Δχ² 7.95 (§5) |
| r | 0.0036 (undeformed) / **0.0046** (deformed) | LiteBIRD: ~4.5σ detection; 2.5σ from plain Starobinsky at the same n_s |
| α_s | −6.1×10⁻⁴ / **−7.7×10⁻⁴** | future CMB |
| Bridge B1 = r − 3(1−n_s)² | −0.9×10⁻⁴ / **+2.5×10⁻³** | N*-free null test |
| w | −1 (baseline) | DESI/Euclid |
| ΔN_eff | **0.05–0.10** (hidden pair 0.034 + gravitino 0.047 at preferred g*) | ACT < 0.14; SO / CMB-S4 σ ≈ 0.03 |
| gravitino | m_3/2 ≤ 4.7 eV (SUSY breaking ≲ 140 TeV) | lensing / Lyman-α |
| α_em today vs early universe | identical after capture (Δ ln α ≲ 2×10⁻¹⁴) | clocks, quasars, Oklo: no drift |
| β (birefringence) | fitted by a separate axion: c_γ ≈ 1.6–3.9, f ≤ 0.1 M_P, Ω_a ≤ 3×10⁻³ | β_reio/β_rec < 1 if m_a ≳ 20 H₀ (LiteBIRD) |
| dark matter | 100–200 TeV, stable (gauged Z₂) or decaying with ξ ≲ 0.6 | IceCube / LHAASO only if decaying |

D-notes: D403, D404, D412, D414, D416, D417, D419.

## 5. Joint test of all data at once ("crown", D410)

Pre-registered: one parameter set must fit CMB + BAO + SNe together, with dark energy on the thawing line w_a = −1.58(1 + w₀); the Twist
passes only if fixing its n_s costs Δχ² ≤ 4 and no data block is worse than ΛCDM by more than 4.

| Fit | χ² |
|---|---|
| ΛCDM, n_s free | 2402.26 |
| thawing, n_s free | 2400.11 (n_s = 0.9736, w₀ = −0.956) |
| thawing, n_s = 0.9651 (undeformed Twist) | 2408.06 (w₀ = −0.971) |
| free w₀–w_a | 2392.30 |

The undeformed Twist **fails**: Δχ² = 7.95, with the CMB block worse than ΛCDM by +5.80 and BAO by +4.22. Thawing dark energy does not lower
the preferred n_s, and a single thawing field captures only Δχ² = −2.2 of the −10.0 that free w₀–w_a gains. With the deformation (n_s = 0.9736)
every block fits better than ΛCDM (CMB −2.77, BAO −0.41, SNe −2.48). This agreement is partly by construction, because ε is fitted to n_s; the
genuine tests move to r, α_s and B1. The ε window for n_s within ±0.003 is (1.8–3.7)×10⁻⁷, a mild tuning comparable to the R³ deformation of
no-scale Starobinsky inflation used for the same purpose (arXiv:2505.03608).

## 6. Weak points (stated, not resolved)

- Trans-Planckian censorship is violated (inflation scale 8×10¹⁵ GeV vs ≲ 6×10⁸ GeV), as for every plateau model with detectable r.
- The vacuum energy sits in a de Sitter minimum, which no controlled string construction provides and the refined dS conjecture disfavours.
- The field travels 15.1 M_P in total; the KK and string towers stay ≥ 2.4×10⁴ times above the temperature after inflation, but at x ≲ 1
  (inflation and the first ~2.5 e-folds after it) the volume reading is outside geometric control.
- No string origin of a local (T − T_E) coupling is known (IIB shift symmetry allows T only as e^(−aT); IIA fluxes give it only globally).
- Capture, pinning and the hidden-sector numbers are estimate-grade (order-one factors not fixed); the Higgs-branch field theory and the
  hidden U(1)'s D-term structure are open.
- n_s is fitted after the deformation, so the model makes no n_s prediction.

## 7. Method

Every number above comes from a short script whose rule (inputs, statistic, pass criterion) was written and hashed before it ran;
fixes were allowed only through dated deviation files. The model was developed with a two-sided procedure: an early-universe and a
late-universe line of work, each passing its results to a central balance check of shared quantities and null "bridge" tests. Several
cross-effects were found only at that centre (the pinning dilution shortening N*, D406; the shared ΔN_eff budget of the gravitino and the
hidden decay products, D416).

## 8. Relation to earlier work

Quintessential inflation (Peebles & Vilenkin 1999) and its no-scale supergravity realisation (arXiv:2008.09099); no-scale Starobinsky
inflation (Ellis, Nanopoulos & Olive, arXiv:1307.3537) and its R³-type deformation for ACT (arXiv:2505.03608); moduli trapping at enhanced
symmetry points (Kofman et al., hep-th/0403001), thermal trapping (Danos, Frey & Brandenberger, arXiv:0802.1557), the string Higgs effect
(Watson, hep-th/0404177) and trapped quintessential inflation (Dimopoulos, hep-ph/0702018); moduli vs axion quintessence (Choi,
hep-ph/9902292); hidden U(1)s in string theory (arXiv:0912.4206); axion birefringence and dark energy (arXiv:2504.17638, 2203.08560);
light-gravitino bound (arXiv:1601.07386); ACT ΔN_eff (via arXiv:2512.19633); data: DESI DR2 (arXiv:2503.14738), CMB-SPA and n_s
(arXiv:2609.19296, 2512.05108). Twist-2's specific contributions are the arrangement (one field; Λ fixed at a thermally trapped,
condensate-pinned, gauge-decaying point), the computed numbers, and the pre-registered test record.

## Code and data

Repository github.com/dannyeldridge54/AEGIS, branch unify-bg: rules in field_tests/rules/ (PREREG_D391 … D419), scripts in theory/twist2/,
theory/crown/ and theory/alpha_nogo/, results in field_tests/results/, notes in theory/pending_docs/D72_D75_weak_spots.md.

## Acknowledgements

This work was carried out with AI assistance (Anthropic's Claude) for literature search, calculations, code and drafting, under the
pre-registration rules above; the author is responsible for its content.
