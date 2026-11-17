# PREREG A1b — wino LO resonance position vs literature (Djl A) — locked 2026-11-17
Source: Beneke, Szafron, Urban 2020 (arXiv:2009.00640). First χ⁰χ⁰ ¹S₀ resonance at 2.282 TeV with the LO potential and 2.419 TeV at NLO. Relic mass 2.886 TeV (LO) and 2.842 TeV (NLO).
Their inputs (quoted): α = 1/128.943 at m_Z; α₂ = α/s_W²; c_W = m_W/m_Z; m_W = 80.385 GeV; m_Z = 91.1876 GeV; δm = 164.1 MeV.
Their LO potential is Coulomb plus Yukawa, the same form as sommerfeld.wino_s.
Method: run sommerfeld.wino_s (unchanged code) with module constants S_W2, M_W, M_Z set to their values, and alpha_w = α/s_W², dm = 0.1641.
Locate the peak of σv_tot = 2 sΓsᵀ at v = 1e-6: golden-section search on [2.1, 2.5] TeV after a coarse 0.01 TeV scan.
- T1: |M_peak/2.282 − 1| ≤ 0.01. PASS/FAIL.
- R (reported): the peak with our default parameters (α_W 0.0335, s_W² 0.231, δm 0.1645); the NLO shift (+0.137 TeV, quoted), and what it does to D1081's CMB band (shift by the quoted amount, labelled estimate).
Script theory/wiring/a1b_resonance.py (written after this lock). Fixes only via DEVIATIONS.
