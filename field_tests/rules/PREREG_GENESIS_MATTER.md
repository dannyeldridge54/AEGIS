# PREREG_GENESIS_MATTER — matter-genesis toolkit, first simulation of P-M (locked D1632, 2026-11-19 15:40 CT)
Toolkit: tools/genesis/genesis.py (textbook-level physics; labels: [toy] = simplified physics).
Inputs (Planck 2018): Ω_b h² = 0.02237, Ω_c h² = 0.1200, T_CMB = 2.7255 K, τ_n = 878.4 s, Q = 1.2933 MeV, B_D = 2.2246 MeV.
Steps and pass rules, fixed in advance:
T1 (consistency, not a test): η from Ω_b h²; m_DM = (Ω_c/Ω_b)·m_p / s for sharing s = n_DM/n_B. Report s = 1 → expected 5.03 GeV.
T2 [toy BBN]: n/p from Bernstein–Brown–Feinberg weak rates λ_np = 255/(τ_n x⁵)(12 + 6x + x²) (x = Q/T), λ_pn = e^{−x}λ_np, plus free decay 1/τ_n; H from g* = 10.75 → 3.36 (smooth step at T = 0.3 MeV) plus 1.75·ΔN_eff; deuterium bottleneck T_D from Saha, η(T/m_N)^{3/2}·6.0·e^{B_D/T}… solved for X_D/X_n = 1 (simplified). Y_p = 2X_n(T_D). PASS if Y_p ∈ [0.235, 0.260] (observed 0.245 ± 0.003; toy tolerance).
T3 [toy]: hydrogen Saha recombination; z at x_e = 0.5. PASS if z ∈ [1250, 1500] (textbook Saha value ≈ 1380; the full Peebles answer is ≈ 1100, which Saha is known to overestimate).
T4 (P-M constraint): a mirror sector with temperature ratio ξ adds ΔN_eff = 7.4 ξ⁴ (mirror photon + 3 mirror neutrinos, (11/4)^{4/3} factor; approximation). Report ξ_max for ΔN_eff < 0.3 (Planck-class bound) and the Y_p shift from T2 at that ξ. Verdict P-M VIABLE if ξ_max > 0.3, i.e. the mirror sector is allowed to be at least modestly warm.
Output: field_tests/results/GENESIS_MATTER/out.json and a 4-panel figure; optional sonification of the ladder via tools/sound (label: art/analogy, no physical claim).
Script: field_tests/scripts/genesis_matter/run.py
