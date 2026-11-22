# PREREG D2037: Bloom steps B0a and B0b (written before computing)

## B0a: mirage soft spectrum, and what it does to α_s (estimate, one-loop)
- **Gaugino masses** (one loop, RG-invariant form, CFNO/mirage, hep-th/0503216 + hep-ph/0504037):
  - M_a(μ) = g_a²(μ)·[M₀/g_G² + b_a·m₃/₂/(16π²)], with M₀ = m₃/₂/(at).
  - Inputs: at = 21.10, m₃/₂ = 2.58e5 GeV, α_G = 1/28.0 (v4), b = (33/5, 1, −3), g² at 1 TeV = (0.211, 0.42, 1.106).
  - Both relative signs of M₀ are reported.
- **α_s shift** from moving the gluino and wino thresholds, holding α₁ and α₂ fixed under unification:
  - δα₃⁻¹(M_Z) = −(1/2π)·Σ_p [(b₃ᵖ − b₂ᵖ) − (b₂ᵖ − b₁ᵖ)·(4/5.6)]·Δln m_p
  - gluino: b₃ᵖ = 2; wino: b₂ᵖ = 4/3; the bino has zero weight.
- **Verdict rule:** B0a is **PASS** only if the mirage spectrum keeps α_s within 2σ of PDG and the wino inside its bar. Otherwise **FAIL**, recording the direction.

## B0b: can a Kallosh–Linde racetrack on T_vis hold the volume during inflation?
- **Rule:** the KL barrier scales with the non-perturbative scale. Estimate m_T ~ a²·A·e^{−aσ}·M_P/(2σ)^{1/2} at the visible value aσ = x = 21.10, with A = 0.54 (v4). This is generous: no volume suppression.
- **Pass:** m_T ≥ H_inf = 5.69e12 GeV within ×10. Otherwise **FAIL**: no racetrack on the visible cycle can protect it, because the gauge coupling fixes σ.
