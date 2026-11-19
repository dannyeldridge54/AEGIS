# PREREG_D1637_G1_REHEAT — reheating from the final SERAPIS equation (Janus genesis G1; locked 2026-11-19 ~22:25Z, before any number)
Question: the P3-S forecaster takes T_R = 8.94e8 GeV as an INPUT to the N_* matching (tools/serapis_calc/p3s.py point(); nstar.py). Is that number consistent with the inflaton of the final equation v3 itself?
Model: V(φ) of SERAPIS_FINAL_EQUATION v3 as coded in p3s.V (D = 10, C = 8.0e-7), canonical φ, y = e^{√2 φ}. Inflation ends at ρ (y = √3/2) where V = V' = 0.
Steps:
1. φ_* and r from p3s.point(C=8e-7, D=10, TR=8.94e8) [the default point].
2. V∞ from the CMB amplitude: V_* = (3π²/2) A_s r M_P⁴ (A_s = 2.1e-9, M_P = 2.435e18 GeV, values as in nstar.py), V∞ = V_*/V(φ_*).
3. m² = V''(φ_ρ) (mpmath derivative of p3s.V at φ_ρ = ln(√3/2)/√2), m in GeV.
4. [estimate] Planck-suppressed decay Γ = κ m³/M_P² with κ ∈ [1/(8π), 1] (κ = 1/(8π) central-low, 1 high); T_R = (90/(π² g*))^{1/4} √(Γ M_P), g* = 106.75.
5. N_* shift: rerun p3s.point with TR set to each T_R from step 4; report ΔN_*, Δn_s, Δr.
Pass rule (locked): CONSISTENT if 8.94e8 GeV lies inside the step-4 T_R band widened by ×10 on each side; otherwise TENSION (state the factor). Secondary (reported, no verdict): |Δn_s| from the T_R change vs the SO σ(n_s) = 0.002.
Caveats stated now: κ (the decay coupling) is not derived from v3; the potential near ρ is the perturbative Eisenstein form (no extra fields); m is the mass along the real-τ = 1/2 line only (axion direction not included).
Script: field_tests/scripts/janus_g/g1_reheat.py → field_tests/results/D1637_G1_reheat.json
