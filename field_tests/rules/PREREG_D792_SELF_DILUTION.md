# PREREG D792: the self-dilution ρ history (no mediator P5)
Locked 2026-11-16 before computing. Script: theory/modular/self_dilution_d792.py. Output: field_tests/results/self_dilution_d792.txt.
Bookkeeping [derived]: φ → 2N with ΔB = ±2, so n_B = 2η·n_φ and n_N = 2n_φ, i.e. B per N = η. The N dominate until they decay at T₂, giving s = (4/3)·M·n_N/T₂. Final: Y_B = (28/79)(3/4)(T₂/M)·η, with the sphaleron factor applied if T₂ > 130 GeV (else 1, flagged).
Isocurvature (D791): |Δx| ≥ 0.15, so η ≥ 0.30. Grid: η ∈ {0.3, 0.6, 1.0}, M ∈ {4.3e11, 1e12}.
Solve T₂ for Y_B = 8.75e-11.
Observables: interpolate D781's table (C = 1.0, 1.15, 1.3e-6) linearly in log₁₀T₂ between T₂ = 3e2 and 3e4 (extrapolate below 3e2 with the same slope, flagged). Report n_s, r, and whether they fall inside the frozen D693 band.
Λ needed: from T₂ = (90/π²g*)^{1/4}√(ΓM_P), Γ = M⁵/(192π³Λ⁴) (D783), compared with M_s ≈ 0.6–3e16.
Decision:
- CONSISTENT (a post-hoc alternative ρ history) if T₂ ≥ 130 GeV and Λ ≤ M_P for some grid point. Then P5 is RETIRED (not needed).
- Also state whether it is inside the frozen band.
