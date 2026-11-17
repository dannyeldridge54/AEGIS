# PREREG A2c-line — wino line at 1 TeV including γZ (Djl A) — locked 2026-11-17
Sources:
- Hisano+ 2005 (hep-ph/0412403) Eq. 28, basis (χ⁺χ⁻, χ⁰χ⁰): Γ_γγ = (πα²/m²) diag(1, 0) and Γ_γZ = (παα₂/m²) diag(2c_W², 0). So σv_γZ/σv_γγ = 2α₂c_W²/α (their Eq. 62).
- Γ_γγ matches 1307.4082 Eq. B5 (cross-check).
- Line quantity: σv_line = σv_γγ + ½σv_γZ (1307.4082 Fig. 1 convention; photons per annihilation).
- Limit: H.E.S.S. 2018 γγ ≈ 4e-28 cm³/s at 1 TeV, applied to σv_line (the standard practice of 1307.4082). Labelled: H.E.S.S. 2018 itself quotes γγ only.
Inputs: on-shell α = 1/128.943; α₂ and c_W² as A1b/A1c (Beneke inputs).
Computation: σv_line = σv_γγ (A2, D1110) × (1 + α₂c_W²/α). Then f_max = f_max(γγ) / √(1 + α₂c_W²/α), for the H.E.S.S. benchmark, McMillan17 and MWPotential2014 (D1114 values), at LO and NLO (√2 post hoc).
Verdict per case: PASS if f_max ≥ 0.26 (SERAPIS-E at 1 TeV), at tree-level Sommerfeld. Also reported with the one-loop ×√3–2 (1307.4082 caveat).
Script theory/wiring/a2c_line_gz.py (written after this lock).
