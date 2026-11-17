# PREREG A2i — SERAPIS-E 0.66 TeV wino vs H.E.S.S. IGS, bracketed (Djl C) — locked 2026-11-17
Quoted IGS line limits: 9.8e-29 (~440 GeV, the curve minimum) and 2.3e-28 (1 TeV).
ASSUMPTION (labelled): the limit is monotonic between 440 GeV and 1 TeV, so lim(0.66 TeV) ∈ [9.8e-29, 2.3e-28]. Both ends are used as pessimistic/optimistic bounds; there is no interpolation.
σv_line = 2|s₊₋|²πα²/M² × (1 + α₂c_W²/α) × R_NLL, with M = 660 GeV, v = 1e-3, R over the D1124 scale band (μ_m ∈ {m, 2m, 4m}, μ_Z ∈ {m_Z/2, m_Z, 2m_Z}), LO and NLO.
Haloes: IGS J ratios (D1126: 1, 0.494, 0.325).
f_max range = [√(9.8e-29/(σv_max·jr)), √(2.3e-28/(σv_min·jr))] vs f = 0.14.
Verdict: PASS if the pessimistic end ≥ 0.14; FAIL if the optimistic end < 0.14; else UNDETERMINED.
Script theory/wiring/a2i_066_igs.py (written after this lock).
