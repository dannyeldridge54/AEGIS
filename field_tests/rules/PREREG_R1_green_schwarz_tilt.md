# PREREG R1 — does the Green–Schwarz form reproduce the SERAPIS-ρ tilt? (follows D1009)

Locked 2026-11-17 before any R1 number.
Published SERAPIS-ρ: V_pub = P(y) + ε(L − L_ρ), P = a²/(a² + 1), a = I_ρ (tools/janus_calc/models.serapis_rho, ε = 6e-5).
GS form (D1009, e^K factor only; A(S,S̄) dependence NOT included — stated limitation): V_GS = P(y)/(1 − κ(L − L_ρ)).
Both on Re τ = ½, y = e^{√2 φ}, same splines and start. Janus core.spectra3 (n_s, α_s third order; r second order).
Points: N* = 46.09 and 49.49 (the D989 SERAPIS-ρ points) and N* = 55.
Test T1 (κ = ε = 6e-5, no tuning): |n_s,GS − n_s,pub| ≤ 3e-4 at all three N* (≈ 0.1σ of σ(n_s) ≈ 3e-3); also report Δr/r, Δα_s.
Test T2 (report): κ* that makes n_s,GS = n_s,pub at N* = 49.49 (root find), and κ*/ε.
Verdict: "GS FORM EQUIVALENT (at e^K level)" iff T1 passes; otherwise "NOT EQUIVALENT" with the numbers.
