# PREREG D773: does P4's pure-NS flux superpotential have a SUSY Minkowski vacuum with the inflaton free?
Locked 2026-11-16 before computing. Script: theory/modular/p4_susy_d773.py (sympy). Output: field_tests/results/p4_susy_d773.txt.
Basis (read off D772's fetched Model I, where F₃ = 2α₀ − 3β³ and H₃ = −2α₃ − 3β⁰ give W = (τ₃ − S)(2τ₁τ₂ + 3)): α₀ ↔ τ₁τ₂τ₃, α_i ↔ τ₁τ₂τ₃/τ_i, β^i ↔ τ_i, β⁰ ↔ 1, W = ∫F₃∧Ω − S∫H₃∧Ω.
Checks:
(1) P4: H₃ = c¹α₁ + d₀β⁰, F₃ = 0 ⇒ W = −S(c¹τ₂τ₃ + d₀) (up to signs). Solve W = 0 and ∂_S W = ∂_{τ₂}W = ∂_{τ₃}W = 0 (the SUSY Minkowski conditions in GVW). Report the solutions with Im S > 0 and Im τ > 0.
(2) The general statement: for a GVW W linear in S and multilinear in τ₁, τ₂, τ₃, a SUSY Minkowski vacuum with W and every ∂W zero, where τ₁ appears in NO relation (W independent of τ₁), needs W = h(S, τ₂, τ₃) with h = ∂h = 0. Enumerate by sympy over all flux vectors with entries in {−3, …, 3} on the 8 components not involving τ₁ (b₀-type, β², β³, α₁ for F and H). Count solutions with Im > 0 for every field.
K4: Model I's W = (τ₃ − S)(2τ₁τ₂ + 3) must have the solution τ₁τ₂ = −3/2, τ₃ = S.
Decision:
- P4 RETIRED if (1) has no admissible solution.
- If (2) has none either: "flux-relation CP sources in untwisted T⁶/(Z₂×Z₂) GVW vacua always involve the inflaton torus" (within the enumerated range) ⇒ revert to explicit CP (reopen P1).
