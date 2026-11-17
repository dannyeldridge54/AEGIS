# PREREG A3a (track X; manual Djl 17 Nov 05:41 CT): neutron stars with realistic EoS (written before running)
Code: tools/janus_astro/ns.py as committed with this lock (never run before it).
Source of every coefficient: Read, Lackey, Owen, Friedman 2009 (arXiv:0812.2163, ar5iv), Table 2 (SLy crust: K = 6.80110e-9, 1.06186e-6, 5.32697e1, 3.99874e-8; Γ = 1.58425, 1.28733, 0.62223, 1.35692; ρ = 2.44034e7, 3.78358e11, 2.62780e12 g/cm³) and Table 3 (SLy: log p1 = 34.384, Γ = 3.005, 2.988, 2.851, M_max 2.049, R_1.4 11.736 km; AP4: 34.269, 2.830, 3.445, 3.348, M_max 2.213, R_1.4 11.428 km). The Table 3 % columns are fit-vs-tabulated errors (≤ 1.08% for these entries).
Tests:
N1 tidal equation, weak-field limit: n = 1 polytrope (single piece K, Γ = 2, ε = ρ) at central compactness-scale ≲ 1e-5: surface y vs the Newtonian exact y = (2 − 6k₂)/(1 + 2k₂) with k₂ = (15 − π²)/(2π²) = 0.25991: |Δy| ≤ 1e-3. (Implemented as a PPEOS-free single polytrope in the check script.)
N2 SLy: M_max vs 2.049 M_⊙ and R_1.4 vs 11.736 km: relative ≤ 1.5% each.
N3 AP4: M_max vs 2.213 M_⊙ and R_1.4 vs 11.428 km: relative ≤ 1.5% each.
N4 TOV cross-check: ns.tov_tidal vs the A0-validated compact.tov (SI) for the same SLy EoS at log ρ_c = 14.8, 15.0, 15.2: M and R relative ≤ 1e-5.
Pass N1–N4 → A3a VALIDATED.
Reported (not scored): Λ_1.4 and k₂ for SLy and AP4; vs GW170817 Λ_1.4 = 190 (+390 / −120) at 90% (LVC 2018, arXiv:1805.11581); mass–radius table.
Script theory/janus_astro/a3a_check.py; output field_tests/results/janus_astro_a3a.txt. No reruns to chase; DEVIATIONS first.
