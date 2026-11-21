# PREREG L5 — genesis and the τ_q window after the brane repair (U11 C-magD7, D1758). Locked BEFORE computing.
Inputs: x = g² Re S/α⁻¹ with g = 3, Re S = √3/2, α⁻¹ ∈ {24.3, 40} ⇒ x ∈ {0.321, 0.195}; T_R = x · 1.34e9 GeV (T_R ∝ √Γ ∝ x; D1665 was x = 1).
(1) Non-thermal leptogenesis (D1648 method): ε_needed = 1.8e-6 · (9e8 GeV / T_R) (η_B ∝ ε T_R / m_φ, m_φ = 5e12 GeV fixed); Davidson–Ibarra M_N,min = ε / [3 m₃ / (16π v²)], m₃ = 0.0501 eV, v = 174 GeV; M_N,max = m_φ/2 = 2.5e12 GeV; also need M_N ≫ T_R (factor ≥ 10).
PASS (genesis survives) if max(M_N,min, 10 T_R) < M_N,max for both x.
(2) τ_q window (PREREG_Q4 rules with Q4 DEVIATIONS D1: N* = 50.37): allowed if T_dec ≥ 5 MeV, D ≤ 1e3, |Δn_s| ≤ 0.003, with D = T_R φ0²/(6 T_dec); report the lowest allowed mass for φ0 ∈ {0.1, 1} at both T_R (4000-point log grid 1e4 GeV – 5.23e12 GeV).
(3) N* and r: ΔN* = ⅓ ln x (reheating-history shift), r ∝ N*⁻² ⇒ r_new = 5.41e-4 · (50.37/(50.37 + ΔN*))², report only (E).
Code theory/tests/l5_genesis.py. One run.
