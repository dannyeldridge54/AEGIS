# PREREG D790: baryogenesis at ρ from the Z₃-charged inflaton, decay ε versus an Affleck–Dine-type orbit charge
Locked 2026-11-16 before computing. Script: theory/modular/inflaton_ad_d790.py. Output: field_tests/results/inflaton_ad_d790.txt.
(a) Decay CP asymmetry from interference of φ → N_nN_n and φ → N_Y N₃ with D725 couplings g = 8.2e-8 – 2.7e-6 (D725 table, M_H = 1e12 – 1e13): ε_φ ≲ g²/(8π) [estimate]. Requirement: Y_B = (3/4)(T_R/m_φ)·ε_φ·⟨ΔB⟩ with ⟨ΔB⟩ = 2, T_R = 3.2e8, m_φ = 2.2e13 ⇒ ε_φ ≥ 4.0e-6. WALL if ε_φ,max < 4e-6.
(b) AD-type orbit charge: near ρ, Z₃ forbids δτ² terms, so the quadratic potential is isotropic (approximate U(1) = rotations of w = (τ − ρ)/(τ − ρ̄), the disk coordinate), broken by cubic δτ³ terms. Starting off the CP line (x₀ ≠ ½) gives the orbit angular momentum.
- Use the D770 code path (two-field, cosmic time) from y = 3, x₀ ∈ {0.5, 0.499, 0.49, 0.45, 0.4}.
- Compute the charge asymmetry η = n_w/(ρ_tot/m) with n_w = Im(w*·ẇ)·(norm), where w is the disk coordinate around ρ, canonically normalised by the metric at ρ. Evaluate it at the D770 judgment time (ρ_tot = 1e-4·V_end).
- K4: x₀ = ½ gives η = 0 (to 1e-8).
- Requirement: η ≥ 4.3e-6/⟨ΔB⟩·2 = 4.3e-6 (from Y_B = (3/4)(T_R/m_φ)·2η).
- Report η(x₀) and the x₀ offset needed. Also report the baryon-isocurvature ratio δη/η = (∂η/∂x₀)·δx/η, with δx = 7.4e-6 (D769).
Decision:
- ROUTE VIABLE if some |x₀ − ½| gives η ≥ 4.3e-6 with δη/η ≤ 0.1 (an order-of-magnitude isocurvature allowance; the Planck baryon-isocurvature bound is to be checked in a later tick).
- The required x₀ offset becomes a postulate-free condition on initial data (not natural, which is labelled).
