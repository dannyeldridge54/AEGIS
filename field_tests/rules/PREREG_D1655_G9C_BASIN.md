# PREREG_D1655_G9C_BASIN — basin map of the dark thread's end point (Janus genesis G9c; locked 2026-11-19 ~23:15Z before any number)
Same model, code and classification as D1653 (PREREG_D1653_G9B_TAU_PLANE; script g9b_tau_plane.py imported unchanged), same start height (D1638 best amp, y₀ = 4.99) and V_Λ re-shot per run.
Starts: x₀ = ½ + δx, δx ∈ {0.05, 0.1, 0.2, 0.3, 0.4, 0.5} (δx = 0.5 is the x = 0 line, also SL(2,Z)-symmetric).
Outputs per start: end class (i / ρ / other), fundamental-domain end point, late ⟨w⟩, a where acceleration ends, and the w₀–w_a CPL fit over a ∈ [1/3, 1] with the D1627 DESI Δχ² (worst of three) so any start that changes today's fit is visible.
Reading (locked): if every start ends i-class → "i is the universal end point (for this start height)"; if some end ρ-class → report the basin boundary in δx; "other" → report. No pass/fail on physics; R0 is inherited (δx = 0 already validated in D1653).
Script: field_tests/scripts/janus_g/g9c_basin.py → field_tests/results/D1655_G9c_basin.json
