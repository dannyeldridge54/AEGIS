# PREREG A2k — upper edge of the SERAPIS-E thermal-wino window vs H.E.S.S. IGS (Djl) — locked 2026-11-17
Masses: 1.1, 1.2, 1.3, 1.5 TeV (off-resonance; the LO resonance with Beneke inputs is at 2.29 TeV).
Limit bracket (ASSUMPTION, labelled): the IGS line limit is monotonic between its quoted 2.3e-28 (1 TeV) and 6.5e-28 (2.9 TeV), so lim(M) ∈ [2.3e-28, 6.5e-28] for M in 1–2.9 TeV. No interpolation.
σv_line = 2|s₊₋|²πα²/M² × (1 + α₂c_W²/α) × R_NLL, with R over the D1124 scale band, at the NLO potential (√2 post hoc) and LO.
Haloes: IGS J ratios (D1126: benchmark 1, McMillan17 0.494, MWPotential2014 0.325) plus the Gaia DR3 central NFW (D1142: 0.427).
Thermal f bracket (D1152): (M/2.842)² to (M/2.207)².
Verdict per (M, halo):
- PASS if the pessimistic f_max (limit 2.3e-28, max R) ≥ the upper f.
- FAIL if the optimistic f_max (6.5e-28, min R) < the lower f.
- Else UNDETERMINED.
Output: the largest mass that PASSES for each halo = the window's upper edge (estimate).
Script theory/wiring/a2k_upper_edge.py (written after this lock).
