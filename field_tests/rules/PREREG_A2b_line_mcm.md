# PREREG A2b-line — wino γγ at 1 TeV with the McMillan17 halo (Djl A) — locked 2026-11-17
Geometry: jfactor.J_route_B (ψ ≤ 1°, |b| ≥ 0.3° masked), the A7a/D1055 H.E.S.S. inner-Galaxy approximation, unchanged.
Reference halo: the A7a H.E.S.S. benchmark, Einasto r_s = 20 kpc, α = 0.17, ρ_⊙ = 0.39 at r_⊙ = 8.5.
Model halo: McMillan17's NFW component as in galpy, r_s = 2.38733 × 8.21 = 19.60 kpc, normalised to its own ρ(R0 = 8.21) = 0.385 GeV/cm³ (D1112).
f_max(M17) = f_max(A2, Einasto) × √(J_Ein/J_M17), using A2's tree-SE f_max 0.355 (LO) and 0.391 (NLO, post hoc).
Also reported: MWPotential2014's NFW (r_s 16 kpc, ρ_⊙ 0.286 at 8 kpc), for the bracket.
Verdict per halo: PASS if f_max ≥ 0.26 (SERAPIS-E at 1 TeV). Also reported with the one-loop ×√3–2.
Script theory/wiring/a2b_line_mcm.py (written after this lock).
