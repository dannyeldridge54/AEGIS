# PREREG A1f — wino CMB band with the NLO potential (Djl A; A1e alternative) — locked 2026-11-17
Why: no blind A1e target exists in 2009.00640 (D1099) or in 2507.15934 (fetched; text quotes no σv or Sommerfeld numbers, only the NLO thermal mass 2.86 ± 0.01 TeV). So this recomputes D1081's CMB band at NLO.
Convention: off_factor = √2, POST HOC (D1095); labelled throughout. Annihilation uses tree-level Γ (as A1/D1081, with the A1c inputs: α₂ = 0.03479).
Grid: M = 2.00–3.00 TeV in steps of 0.02, v = 1e-7 (saturated).
p_ann = f_eff σv_tot/M; f_eff ∈ {0.14, 0.41} (D1081 bracket); limit 3.2e-28 cm³ s⁻¹ GeV⁻¹.
Reported:
- The excluded band edges for each f_eff.
- Whether the NLO thermal mass is excluded, using both 2.842 TeV (2009.00640) and 2.86 ± 0.01 TeV (2507.15934 quoting [48]).
- f_max at those masses.
Also an LO run with the same inputs (α₂ 0.03479), for a like-with-like shift.
No pass/fail: this is a physics update of D1081/D1087 (post-hoc convention).
Script theory/wiring/a1f_cmb_nlo.py (written after this lock).
