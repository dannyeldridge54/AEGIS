# PREREG D777: light-neutrino ordering and Σm_ν at ρ from the 2⊕1 type-I seesaw
Locked 2026-11-16 before computing. Script: theory/modular/rho_seesaw_d777.py. Output: field_tests/results/rho_seesaw_d777.txt.
Γ₂ ≅ S₃ at ρ, with the weight-2 doublet Y ∝ (1, i) and A(Y) = [[Y₂, Y₁], [Y₁, −Y₂]] (nilpotent at ρ).
- M_R = [[A(Y), cY], [cYᵀ, 0]] (D724, b = 0), c ∈ {0.6, 1, 3}.
- Dirac (L as 2⊕1, N as 2⊕1, weight-2 couplings only; L₃N₃ needs a weight-2 singlet, none exists, so it is 0, as for b):
  M_D = [[A(Y), βY], [γYᵀ, 0]], with the A coefficient normalised to 1 and complex β, γ (P1).
- m_ν = −M_D M_R⁻¹ M_Dᵀ (overall scale free). Charged leptons diagonal (only eigenvalues are used).
Grid: |β|, |γ| ∈ {0.1, 0.2, 0.5, 1, 2, 5, 10} × phases {0, π/3, 2π/3, π, 4π/3, 5π/3} each ⇒ 1764 points per c.
Classification of the sorted singular values a < b < c₃:
- NO-like if (b² − a²)/(c₃² − a²) is within ±10% of 0.0297;
- IO-like if (c₃² − b²)/(c₃² − a²) is within ±10% of 0.0297.
Normalise c₃² − a² = 2.5e-3 eV² and report Σm_ν. K4: M_R reproduces D725's singular values (0.2745c ×2 and 0.38817) up to normalisation.
Decision:
- PASS if some NO point has Σm_ν ≤ 0.064 eV.
- TENSION if there are NO points but all have Σ > 0.064 eV, or only IO points exist.
- FAIL if neither ordering is reproduced.
