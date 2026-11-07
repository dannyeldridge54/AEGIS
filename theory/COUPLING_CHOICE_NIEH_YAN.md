# The Twist couples through the Nieh–Yan term (decision, 7 November 2026)

**Decided by the author** after the 7 Nov audit (item G). Written with AI assistance (Claude). Tier: **HYPOTHESIS**
(claim `coupling_nieh_yan` in `ufe-v2/method/claims.json`). No locked rule, prediction or fit is changed by this file.

## The choice

A dynamical Barbero–Immirzi field β can enter Einstein–Cartan gravity through the **Holst** term or the **Nieh–Yan**
term. Solving for torsion, both leave torsion-free GR plus a scalar (Calcagni & Mercuri, arXiv:0902.0957), but:

| | Holst | **Nieh–Yan (chosen)** |
|---|---|---|
| Kinetic term | (3/4)(∂β)²/(1+β²) | (3/4)(∂β)² |
| Canonical field | φ = √(3/2) M_Pl arsinh β | **φ = √(3/2) M_Pl β** (linear) |
| A potential periodic in β is, in φ, | lopsided (the "Fingerprint") | **the plain cosine** |
| Shift symmetry β → β + c | no | **yes** (the term is topological) |

## Why Nieh–Yan

1. **The decay constant comes from it.** `NIEH_YAN_PERIOD.md` (release repository) derives the period from the
   Nieh–Yan index (Chandía–Zanelli: ∫N = 4π²ℓ²ν), giving Δβ = κ/(πℓ²) = 8 and F = (4/π)√(3/2) M_Pl at ℓ = √G. That
   derivation already uses the linear Nieh–Yan map.
2. **It matches the supergravity embedding.** The GKY Kähler potential depends only on Φ + Φ̄, so the BI axion is
   shift-symmetric, as a topological coupling requires; the Holst kinetic term is not shift-symmetric. At |φ| = 1 the
   GKY kinetic coefficient equals the Nieh–Yan 3/4.
3. **The fits are already Nieh–Yan.** Every fitted model uses V = Λ⁴[1 − cos(d/F)]ⁿ in the canonical displacement d,
   which is exactly the Nieh–Yan form. Only the Fingerprint and the rest-point label used the Holst map.

## What changes

- **The prediction is the plain cosine.** The Fingerprint (`PREREGISTRATION_SINH.md`, locked 26 Oct, not yet run)
  becomes the **Holst alternative**. Its locked rule now also tests the choice: a Fingerprint better by more than 2
  in χ² would favour Holst over Nieh–Yan.
- **The rest point loses observable content.** φ₀ = √(3/2) arsinh(1/γ₀) = 2.63 M_Pl is a Holst number. With the
  Nieh–Yan shift symmetry only the displacement d is physical, so γ₀ = 0.2375 is a label, not a prediction (it was
  already described as a numerical coincidence). The guardrail "Theory math" still checks the Holst algebra as
  mathematics; it is not evidence for either coupling.
- **Gravitational waves.** In Einstein–Cartan the Nieh–Yan field gives no tree-level GW birefringence; locked Q6's
  10⁻⁴³–10⁻⁴² GeV scale is from teleparallel gravity (Li, Rao & Zhao, arXiv:2007.08038). Q6 stays as locked; its
  null-result clause is the Nieh–Yan expectation.
- **Two roles, two scales.** Late role: F = 1.559 M_Pl at ℓ = √G. Early role (F ≈ 0.14) would need ℓ ≈ 3.3 √G, so the
  early field is not fixed by this derivation.

## Unchanged

λ = −2√(2/3); every locked rule and prediction; every stored fit; the four assumptions of the derivation (coupling
normalisation, ν_min = 1, true periodicity, ℓ = √G).

## What decides it

| Test | Status | Nieh–Yan expects |
|---|---|---|
| TF-P, F = 1.559 fixed (locked 2 Nov) | **ran 3 Nov: SUPPORTED on DES Y5** (D 0.00, G −7.42); Union3 DISFAVOURED (information) | D_F ≤ 1 on all samples; **Union3 is blind** |
| Fingerprint vs plain cosine (locked 26 Oct) | not run | within ±2, or cosine better |
| GW velocity birefringence | future (LISA, ET, CE) | none at tree level |
