# PREREG A2f-line — NLL line scale variation at 1 TeV (Djl D) — locked 2026-11-17
Code: the D1121 script (theory/wiring/a2d_line_nll.py) logic, unchanged except that μ_m ∈ {m, 2m, 4m} and μ_Z ∈ {m_Z/2, m_Z, 2m_Z} (the 1409.8294 band, quoted in PREP_A). m = 1000 GeV, LO and NLO s.
Output: the range of R and of f_max for the three haloes over the 9 scale pairs. Verdict vs f = 0.26 per halo: robust PASS or FAIL if every scale pair agrees, else SCALE-DEPENDENT.
Script theory/wiring/a2f_line_scale.py (imports Sig from a refactored copy, written after this lock).
