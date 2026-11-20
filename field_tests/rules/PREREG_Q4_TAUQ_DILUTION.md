# PREREG Q4 — can the quark modulus τ_q live with the Weave's early universe? (locked 2026-11-20, before computing)
Inputs (fixed, earlier notes): T_R = 1.34e9 GeV (D1665), inflaton mass 5e12 GeV (D1641), r = 4.46e-4, A_s = 2.1e-9 → H_inf = π M_P √(A_s r/2), M_P = 2.435e18 GeV.
Standard moduli formulas: Γ = c m³/(4π M_P²) with c = 1; T_dec = (90/(π² g*))^{1/4} √(Γ M_P), g* = 10.75 (if T_dec < 1 GeV) else 80;
 if τ_q is displaced by φ0 during inflation (only possible if m < H_inf) and oscillates before reheating ends, D = (1/6) T_R (φ0/M_P)² / T_dec (only when D > 1).
 ΔN* = −⅓ ln D; for the plateau n_s ≈ 1 − 2/N*, Δn_s = 2 ΔN*/N*² with N* = 55.
Scan m from 1e4 GeV to H_inf, φ0 ∈ {0.1, 1} M_P.
Rules:
- LIGHT route (m < H_inf) PASS if some m gives T_dec ≥ 5 MeV, D ≤ 1e3 (F2) AND |Δn_s| ≤ 0.003 (one CMB-SPA σ). Report the allowed m window.
- HEAVY route (m ≥ H_inf, no displacement): automatically safe for cosmology; flagged "needs stabilisation outside the Weave (flux)".
Verdict = the routes that pass. No reruns.
