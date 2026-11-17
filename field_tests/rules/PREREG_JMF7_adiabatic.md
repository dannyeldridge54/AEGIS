# PREREG JMF7 — adiabatic-limit check: has P_R stopped evolving by the end of inflation?
Locked 2026-11-17 before any JMF7 number. Janus-MF (tools/janus_calc/mfms.py, unchanged) evaluates P_R at ε = 1. If isocurvature modes still source
ζ there, the numbers in JMF2–JMF6 are not final. Test: spectra_mf with end_back = 5, 3, 1, 0 e-folds (evaluation that many e-folds before ε = 1),
same pivot (55 e-folds before ε = 1), same stencil. Models: Q9 (JMF2, R = 9, the most two-field case), N2' and N1 (JMF6 definitions, φ_init (12, 12)
and (12.5, 12.5)).
Claims per model: C1 |P_R(end_back=1)/P_R(0) − 1| ≤ 1e-3 and |Δn_s| ≤ 1e-5 between end_back 1 and 0 → ADIABATIC LIMIT REACHED (results final);
otherwise P_R still evolving at the end → the multi-field results need a reheating/uniform-density treatment (finding, not a failure of the code).
Also reported: the full end_back sequence (how fast isocurvature decays). Results: field_tests/results/janus_jmf7.txt (+ stamp).
