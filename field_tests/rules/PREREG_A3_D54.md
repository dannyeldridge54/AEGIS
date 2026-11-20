# PREREG_A3_D54 — the one-loop R⁴ thread at D = 5 and D = 4 (locked D1681, 2026-11-20 00:45 UTC)
Same method as PREREG_A3_D6 (validated code, D1680): I_d(R) = RN∫_F Γ_{d,d} dμ with Γ_{d,d} = Γ_{1,1}(R)^d, d = 5 (D = 5) and d = 6 (D = 4). Γ_{d,d} → τ₂^{d/2}, so the Zagier subtraction is L^{α−1}/(α−1) with α = d/2 (L^{3/2}/1.5 and L²/2).
R ∈ {1, 1.25, 1.5, 2, 3}. Also the convergent-scheme shift S_d = RN∫ τ₂^{α} dμ = −∫dx (1 − x²)^{(α−1)/2}/(α − 1).
Reading as in A3_D6: report min I and the zero crossing; positivity for large R is expected (volume term).
Script: field_tests/scripts/a3d6/run54.py
