# PREREG JMF1 — JANUS-MF step 1: Janus two-field δN vs MultiModeCode (independent code; exact multi-field MS + its own δN)
Locked 2026-11-17 before any JMF1 number. MultiModeCode release 2.0.0 (github laynep/MultiModeCode @641153c), built with gfortran in /home/claude/ext/mmc.
Model: V = ½(m₁²φ₁² + m₂²φ₂²) (MMC potential_choice = 1, m² = 10^vparams(1,:)), m₁² = 1e-11, mass ratio R = m₂/m₁ ∈ {1, 3, 9}; φ_init = (12, 12) (MMC ic_sampling
= reg_samp); N_pivot = 55 before ε = 1 (slowroll_infl_end); k_pivot 0.002, dlnk 0.4 (MMC defaults). Janus: background from the same φ_init with slow-roll start
velocity (tools.serapis_calc.multifield.run), φ* at 55 e-folds before ε = 1, then twofield.observe_multi (δN; n_s VW Eq. 17, r NLO, f_NL).
Claims: C1 (implementation check) |n_s^Janus δN − n_s^MMC δN-SR| ≤ 2e-4 for all three R; C2 (reported) |n_s^δN − n_s^MMC exact| per R — the δN
approximation error; C3 (reported) r Janus NLO vs MMC exact. C1 pass → JANUS δN AGREES WITH AN INDEPENDENT CODE; else NOT. Results: field_tests/results/janus_jmf1_mmc.txt.
