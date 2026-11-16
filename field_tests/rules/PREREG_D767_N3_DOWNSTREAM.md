# PREREG D767: what changes downstream when SERAPIS-E's stuck branes are 3/3/3 + 1 (D766)
Locked 2026-11-16 before computing. Script: theory/modular/n3_downstream_d767.py. Output: field_tests/results/n3_downstream_d767.txt.
(1) Tilt: D696 gives C = (15/64π⁶)·N_eff/(Im S Im ρ), with N_eff = N − N0 and tadpole 3N + N0 + N_flux = 16 (N_flux = n_flux/2 in 2405.18813 units). Compute Im S·Im ρ for C ∈ [1.0, 1.3]e-6 (the n_s 0.970–0.975 band, D692/D696) for (N, N0) = (5, 1) [K4: must reproduce D696's 750–975] and (3, 1) with N_flux = 6. Also give the ×½ stuck-brane-unit variant.
(2) The wino chain: check by inspection of D732/D735 inputs that T_R (heavy-ν sector, D725), m₃/₂ (phenomenological window, D6416-block) and M₂ = 2.7e-3 m₃/₂ (anomaly mediation) do not depend on N or Im S·Im ρ. If so, rerun D732 and D735 unchanged as a regression (outputs must match the committed files byte for byte).
Decision:
- If (1) differs from D766's stated 225–732, write a D766a correction.
- The wino window is UNCHANGED if (2) holds.
