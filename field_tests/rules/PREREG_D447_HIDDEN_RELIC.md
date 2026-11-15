# PREREG D447 — cloud run 2 (Danny 19:20 CT "Start another"): Boltzmann relic of the lightest D7-charged state (makes D445/D446 quantitative)
Locked before computing. Script theory/deep/hidden_relic_d447.py. Lightest charged state: complex scalar (g = 2), mass m, annihilating to light hidden
states with σv = λ⁴/(16π m²) (s-wave). Hidden bath temperature T_h = ξT, ξ fixed by the condensate energy share ε_h injected at capture
(T = 1.5e11 GeV): ξ = (ε_h·g*/g_h)^{1/4}, g* = 106.75, g_h = 10; cases ε_h ∈ {1e-5 (D444/D446 ceiling), 1e-3}. Thermalisation check:
Γ_th = n_h σv(T_h ~ m) ... reported as λ⁴T_h/(16π) vs H at capture (rough). Boltzmann: dY/dx = −(s σv/(H x))(Y² − Y_eq²), x = m/T,
Y_eq from n_eq(T_h) = g m² T_h K₂(m/T_h)/(2π²), s = (2π²/45)g*T³, H = 1.66√g* T²/1.22e19 GeV; Ω h² = 2.74e8 (m/GeV) Y∞ (Radau, rtol 1e-8).
Scan m ∈ {10, 100, 1e3, 1e4, 1e5} GeV; for each, λ giving Ω h² = 0.12 and = 0.0012 (root-find, λ ∈ [1e-4, 30]).
Readings: allowed region = λ ≤ √(4π) = 3.54. Report the largest m for which 1% (and 100%) is perturbative, per ξ. Also report Ω h² at λ = 1.
No reruns to chase; fixes via PREREG_D447_HIDDEN_RELIC_DEVIATIONS.md first.
