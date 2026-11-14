# Deviations for PREREG_D360_TESTS (written before any run)

D1 (07:55 CT, before running T2): the locked T2 script would integrate ~10²⁰ field oscillations (m/Γ = 8πM_P²/m² for m = 10⁹ GeV), which is
not feasible. T2 is replaced by the standard averaged system, starting when oscillations begin (H = m) with ρ_φ = ½m²(A M_P)², the rest
radiation: dρ_φ/dN = −3ρ_φ − (Γ/H)ρ_φ, dρ_r/dN = −4ρ_r + (Γ/H)ρ_φ. Δ = (a³ρ_r^{3/4})_final/(ρ_r^{3/4})_initial. Same cases, same pass criterion
(within ×10 of D359). This tests D359's growth-and-decay arithmetic; the frozen-field phase before H = m is assumed, as in D359. Script:
theory/review/modulus_dilution_d360b.py.
