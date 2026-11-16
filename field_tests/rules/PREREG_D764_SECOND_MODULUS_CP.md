# PREREG D764: CP violation from a second complex-structure modulus tied to U₁ = ρ by a flux relation
Locked 2026-11-16 before computing. Script: theory/modular/second_modulus_cp_d764.py. Output: field_tests/results/second_modulus_cp_d764.txt.
Literature mechanism (2405.18813): fluxes impose U₁U₂ = b₃/a⁰. With U₁ stabilised at the fixed point ω (≅ ρ), U₂ = (b₃/a⁰)/U₁ lies off the CP locus unless the ratio is special.
CP test: j(τ) is real exactly on the CP-conserving locus (imaginary axis, Re τ = ±½, unit arc, and their SL(2,Z) images), since j(−τ̄) = j(τ)*. CP-odd measure: s_CP = |sin arg j(U₂)| (0 means CP-conserving).
K4 regressions: s_CP(i) = 0 and s_CP(ρ) = 0 (j(ρ) = 0: report |Im j| instead), s_CP(0.1 + 1.3i) > 0. The paper's example a⁰ = 2, b₃ = −3 gives U₂ = 3/4 + (3√3/4)i, which must come out CP-violating.
Scan: a⁰ ∈ {1..6}, b₃ ∈ {−1..−12}, with |b₃/a⁰|·|1/ρ| giving Im U₂ ≥ 0.2 after reduction.
Report: the fraction of flux pairs with s_CP > 0.1, and the median s_CP.
Decision:
- P1 is REPLACED by a literature mechanism (new postulate P2: the heavy-ν couplings carry U₂ dependence) if the fraction is ≥ 0.5 and the median s_CP ≥ 0.3.
- Otherwise P1 stays.
