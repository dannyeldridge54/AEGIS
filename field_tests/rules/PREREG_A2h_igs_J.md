# PREREG A2h — J-factors in the H.E.S.S. IGS geometry and the 1 TeV verdict (Djl B) — locked 2026-11-17
Geometry (quoted, 2608.07234): 25 annuli of 0.1° from 0.5° to 3.0° around the GC. The tabulated J are unmasked (masks reduce effective J; mask geometry is not given).
J_annulus = J_route_B(ψ_max = 3.0°, b_mask = 0) − J_route_B(ψ_max = 0.5°, b_mask = 0).
- S1 (sanity, scored): the IGS benchmark Einasto (α 0.17, r_s 20, ρ_⊙ 0.39 at 8.178 kpc) reproduces their total 2.5e22 to within 10%.
- Ratios: McMillan17 NFW (r_s 19.60, ρ 0.385 at 8.21) and MWPotential2014 NFW (r_s 16, ρ 0.286 at 8) vs the IGS benchmark.
- f_max(halo) = √(2.3e-28/(σv_line,NLL · J_ratio)), with σv_line,NLL from D1121 machinery at 1 TeV over the D1124 scale band.
  - Implemented as f_max_bench,IGS = f_max_bench(D1124 at 4e-28) × √(2.3/4) × √(J_bench,2018-geom/J_bench,IGS-geom normalised…)? NO.
  - Instead, compute directly: σv_line = 2|s₊₋|²πα²/M² × 4.486 × R, with R ∈ [0.658, 0.794] (D1124), at LO and NLO.
- Verdict vs f = 0.26 per halo.
Script theory/wiring/a2h_igs_J.py (written after this lock).
