# PREREG B2 — Chronos → BBN wiring (Djl B) — locked 2026-11-17
Code (written after this lock): theory/wiring/b2_chronos_bbn.py, using tools/janus_astro/bbn.py (B1) and janus_lt.background.omega_gamma_h2.
ΔN_eff sources per SERAPIS branch:
- (a) Dark radiation from the heavy-neutrino sector: ρ branch 2⊕1 = 0 (D725). The τ=i branch has no ΔN_eff computation in the D-notes; it is treated as 0 and flagged OPEN.
- (b) Primordial GW background (A7c, D1057): bound ∫Ω_GW h² d ln f ≤ max(listed Ω_GW h²) × ln(f_end/f_min), with f_min = 1e-18 Hz and f_end from A7c.
  The conversion is derived from the N_eff definition: ρ_GW = ΔN·(7/8)(4/11)^{4/3} ρ_γ, so ΔN_GW = ∫Ω_GW h² d ln f / [(7/8)(4/11)^{4/3} Ω_γ h²], with Ω_γ h² from omega_gamma_h2(2.7255). The literature coefficient 5.6e-6 is reported as a check only.
Branches (A7c): τ=i (T_R 1e6, 3e6 GeV), ρ (T_R 3.2e8, 3.0e9 GeV).
Tests:
- T1 (wiring lossless): bbn.Yp/DH at ΔN = ΔN_GW + ΔN_DR reproduce the direct calls bit-identically.
- T2 (scored): for every branch, ΔN_total inside D1082's BBN window [−0.04, +0.41] AND |pull| < 2 for Y_p and D/H with PRIMAT. Labels: as in B1.
- R: ΔN_GW values, the coefficient check, and the shifts δY_p and δ(D/H) relative to ΔN = 0.
B2 VALIDATED iff T1 passes; T2 is the physics verdict (CONSISTENT/TENSION/EXCLUDED).
