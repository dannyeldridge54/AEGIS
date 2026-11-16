# PREREG D791: the inflaton-AD window at ρ under the Planck isocurvature bound
Locked 2026-11-16 before computing. Script: theory/modular/ad_isocurv_d791.py. Output: field_tests/results/ad_isocurv_d791.txt.
Inputs:
- Planck 2018 X, Table 14, uncorrelated axion-type ("axion I") CDI: 100β_iso < 3.8 at k = 0.05 (95%).
- The baryon isocurvature maps to effective CDI S_c = (Ω_b/Ω_c)·S_b, with Ω_b/Ω_c = 0.0493/0.265 (Planck 2018 values, from memory, estimate).
- S_b = δη/η = (∂ ln η/∂x₀)·δx, with η = 2|Δx| (D790 valid read-outs) ⇒ S_b = δx/|Δx|, δx = 7.4e-6 (D769).
- P_R = 2.1e-9.
Compute:
(1) |Δx|_min from β = P_S/(P_S + P_R) < 0.038;
(2) η = 2|Δx|_min;
(3) Y_B = (28/79)(3/4)(T_R/m_φ)·⟨ΔB⟩·η, with T_R = 3.2e8, m_φ = 2.2e13, ⟨ΔB⟩ = 2 (all inflaton channels carry B-triality, D780). The sphaleron factor 28/79 applies because the asymmetry is in B with L = 0, so B − L ≠ 0.
(4) The over-production factor relative to 8.75e-11, i.e. the dilution needed.
Decision:
- WALL if the dilution needed exceeds 10 with no in-model entropy source.
- VIABLE if ≤ 10.
