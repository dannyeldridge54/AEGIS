# PREREG D753: can a small number the model already has produce ε (τ = i: 1.3–1.6e-4; ρ: ≈ 6e-5)?
Locked 2026-11-16 before computing. Script: theory/modular/eps_candidates_d753.py. Output: field_tests/results/eps_candidates_d753.txt.
## Candidate list (fixed now; physical quantities only, no free O(1) factors, products of at most two)
Single quantities:
- L = 1/16π² (one loop); L².
- Instanton factors e^{−2π Im τ} and e^{−4π Im τ} at τ = i and at ρ.
- C_BHK = 1.15e-6 (SERAPIS-E).
- H_inf/M_P (V*^{1/4} = 4.8e15 GeV); √A_s.
- m_φ/M_P for τ = i (1.9e11 GeV) and for ρ (2.2e13 GeV).
- |η(i)|²⁴ and |η(ρ)|²⁴.
- 1/E(ρ,2) and 1/E(i,2).
Products: L × each single quantity.
## Rule
A candidate "lands" if it is within a factor 2 of the target (τ = i: 1.45e-4; ρ: 6e-5).
Look-elsewhere statement: with N candidates spread over ~20 decades, the chance that one lands within ×2 of a given target by accident is ≈ N·log10(4)/20. Report it next to any hit.
A hit counts as a LEAD only if, besides landing, its functional form matches the term it would replace (I₁ at i, L at ρ); otherwise it is numerology. No refitting.
