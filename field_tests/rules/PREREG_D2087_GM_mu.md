# PREREG D2087: the Giudice–Masiero μ for v4's torus Higgs, tested against the D2086 feasible region. Locked before computing.

**Formula** (Brignole–Ibáñez–Muñoz hep-ph/9707209, quoted):
- Eq. 28: μ̂ = [m₃/₂ Z − F̄∂̄Z](K̃₁K̃₂)^{−1/2}
- Eq. 67: untwisted Higgs, Z = K̃₁ = K̃₂ = 1/[(T₃ + T̄₃)(U₃ + Ū₃)]
- Eq. 68: μ̂ = m₃/₂[1 + √3 C cosθ (e^{iγ₃}Θ₃ + e^{iγ₆}Θ₆)]
- Eq. 69: Bμ̂ = 2m₃/₂²[…]
- Eq. 72: m²_H + |μ̂|² = Bμ̂, so tan β = 1 at the boundary scale.

**v4 input:**
- U is fixed by flux, so F^U = 0.
- KKLT gives |F^T/(T + T̄)| ≈ m₃/₂/x with x = 21.10 (D2051a).
- So c = μ/m₃/₂ = 1 ± 1/x, i.e. c ∈ [0.953, 1.047], with **sign +**. Bμ and μ have the same phase as m₃/₂, so L = +|μ| sin2β, the PGM positive-L case.

**Tests (no new fit; tools/seed/wino_mu.py functions):**
1. Inside v4's m₃/₂ band [250, 700] TeV with c ∈ [0.953, 1.047] and tan β ∈ {1.5, 2, 3, 4}: report the predicted wino range and α_s range, and whether any point meets all three D2086 goalposts.
2. In the whole D2086 feasible set: the points with c ∈ [0.953, 1.047], with their m₃/₂ and tan β.

**Verdict:**
- **CONSISTENT** if test 1 has ≥ 1 feasible point.
- **TENSION** if test 1 has none but test 2 does: GM works, but only at an m₃/₂ outside v4's band.
- **FAIL** if neither has a feasible point.

**Caveat (stated):** Eq. 72 gives tan β ≈ 1 at M_SUSY; the tan β grid starts at 1.5, so tan β ≈ 1 is reported separately as an extra row.
