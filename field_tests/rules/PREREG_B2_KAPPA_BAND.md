# PREREG B2 — honest rung probabilities for the up quarks including O(1) coefficient spread (locked 2026-11-20, before computing)
Model: g_q = κ_q · ε(m_q), κ_q = √(κ₂·√κ₁), κ₁, κ₂ independent log-uniform in [1/3, 3] per sector. Down fixed at rung 1.
Observed r = g_u/g_d = 0.1312 (input B, D1742; input error negligible here).
Likelihood p(ln r | m_u) by MC (2e6 draws per rung, seed 5, Gaussian KDE in ln r, bandwidth 0.05); flat prior over m_u = 1…32.
Report posterior P(m_u) for every rung and the 68% / 95% credible rung sets.
Rule: L1's "rung 8" is SHARP if P(8) ≥ 0.5; BROAD if the 68% set has ≥ 4 rungs (then L1 cannot pick the rung; only the ladder-band statement stands).
No reruns.
