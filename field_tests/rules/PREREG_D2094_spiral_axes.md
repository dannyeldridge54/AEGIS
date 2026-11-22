# PREREG D2094: do the UFE's centres and steps sit on golden or silver spiral axes? (Danny 07:49.) Locked before computing.

**Facts to verify in code (exact geometry in the upper half-plane):**
- The golden hyperbolic element M_φ = [[2, 1], [1, 1]] has axis endpoints φ and −1/φ, and translation length 2 arccosh(3/2) = 2 ln φ².
- The silver element M_σ = [[2, 1], [1, 0]] has endpoints 1 ± √2. Its translation length is 2 arccosh(|tr|/2) with tr = 2, which makes it parabolic. So use M_σ² (tr = 6) and report it.
- Check: do i and ρ lie on these axes (distance to the geodesic < 1e-12)?

**Data-level tests (numerology lens, with a random control):**
- **T1:** the hyperbolic distance d(ρ, i) in units of ln φ and of ln(1 + √2).
- **T2:** the generation step d* = 2 artanh(u*) with u* = 0.052 (D1894), in the same units.
- **Hit rule:** a ratio within 1% of a simple fraction p/q (|p| ≤ 6, q ≤ 4).
- **Chance:** the same rule applied to 10,000 random log-uniform units in [0.3, 1.2] (seed 0), as the fraction of random units scoring a hit on each quantity.

**Verdict:**
- **EVIDENCE** only if the golden or silver hit rate beats the chance rate by ×3 on both T1 and T2;
- else **NO EVIDENCE**.
- The structural facts are reported as geometry, with no evidence credit.
