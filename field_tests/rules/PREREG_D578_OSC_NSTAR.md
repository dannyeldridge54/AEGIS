# PREREG D578: post-inflation history and N* for the mass-completed SERAPIS models (D575, D577), locked before computing

Models:
- (K1) HS-Kairos + species term, κ = 1e-3, Ñ₀ = 25.
- (K2) The same with κ = 1e-2.
- (C1) Two-term ε = 1e-4 (Chronos-like). All p = 2.

Steps:
1. Near-vacuum coefficients, computed numerically at τ = i + iδ:
   - V ≈ c₈δ⁸ (from I²) + ½ m̂² φ² (mass term), with φ = δ/√2 (α = 1/3).
   - Crossover amplitude φ_x where c₈(√2 φ)⁸ = ½ m̂² φ²; crossover density ρ_x = V(φ_x).
2. Scales:
   - H_inf from r and A_s = 2.1e-9: V* = (3π²/2)A_s r M_P⁴, using each model's own (n_s, r) at N* = 54 from its D575/D577 script.
   - m = (m/H)·H_inf, with m/H recomputed in units of √(V*/3).
   - ρ_end = V(y_end) in V₀ units, scaled by V*/V(y*).
3. Decay: Γ = (c_Γ/8π)m³/M_P² with c_Γ ∈ {1, 10} (the D518 convention); T_RH = (90/(π²g*))^{1/4}√(ΓM_P), g* = 106.75; ρ_RH = (π²g*/30)T_RH⁴.
4. N*, using the D518 formula exactly: N* = 67 − ln(k*/a₀H₀) + ¼ ln(V*²/(M_P⁴ρ_end)) + Σ_phases (1 − 3w)/(12(1 + w)) ln(ρ_out/ρ_in), with ln(k*/a₀H₀) = ln(0.05 × 4282.7).
   - Phase A, from ρ_end to max(ρ_x, ρ_RH): bracketed by w = 3/5 (octic, the stiff bound) and w = 0 (the matter bound). Both reported.
   - Phase B, from ρ_x to ρ_RH, if ρ_x > ρ_RH: w = 0.
   - Iterate once: compute N*, recompute (V*, H, m) at that N*, recompute N*. One iteration only.
5. n_s and r at the resulting N* values: rerun the model's own infl().

Verdict:
- If both brackets give N* inside [52, 55.6], the D567 bands are unconditional again for that model (D567a is lifted for it).
- Otherwise, report the new N* range and the (n_s, r) values as D578 bands. They are post-hoc, scored only on future data, and they do NOT replace D567's locked numbers.
Fixes go in PREREG_D578_DEVIATIONS.md, written first.
