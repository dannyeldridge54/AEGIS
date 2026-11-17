# PREREG A2g-line — SERAPIS-E 1 TeV wino vs the H.E.S.S. Inner Galaxy Survey line limit (Djl A) — locked 2026-11-17
Source (fetched, arXiv:2608.07234, H.E.S.S. Collaboration):
- 95% limit on ⟨σv⟩_line = σv_γγ + ½σv_γZ: 2.3e-28 cm³/s at 1 TeV (Einasto α = 0.17, r_s = 20 kpc, ρ_⊙ = 0.39 at 8.178 kpc). This is a LINE limit, so γZ is included natively (fixes D1118's γγ-only caveat).
- Thermal wino excluded; wino excluded to ~10 TeV for non-thermal production; total J = 2.5e22.
Method: f_max(halo) = f_max_D1124(halo) × √(2.3e-28/4e-28). D1124's f_max were computed against the 2018 limit applied to the line. Use the D1124 scale band (NLL R ∈ [0.658, 0.794]) at LO and NLO.
ASSUMPTION (labelled): the model/benchmark J ratios (McMillan17 0.499, MWPotential2014 0.332) are taken from the 2018 geometry (ψ ≤ 1°, |b| ≥ 0.3°). The IGS ROIs are larger, and the cuspier benchmark's advantage typically shrinks with larger ROIs, which would raise these ratios and LOWER f_max. Stated as a direction-of-error note.
Verdict vs f = 0.26 per halo: PASS, FAIL, or BAND-DEPENDENT.
Script theory/wiring/a2g_line_igs.py (written after this lock).
