# PROM-1 deviations (R84: no MAJOR, 3 MINOR), written before the fixes
- DEV-1 the accept rule as locked needs P1 AND P2 to improve; test_prom1 compared the 500 MW distance only. Added the 400 MW distance
  (the FUSION-1 model falls to a cold root there, P_fus ~11 MW, so P2 improves trivially). Verdict unchanged: accepted.
- DEV-2 report tau_E and P_fus over Lux's own uncertainty band (C3 0.6 +- 0.1, rho_core 0.75 +- 0.05) instead of one point; the P1/P2
  verdicts are stated as band-dependent. No refit of C3 or rho_core (choosing after seeing would be tuning).
- DEV-3 synchrotron: the Albajar fit's profile factors assume parabolic profiles; it is fed the pedestal T0. Labelled "approximate (fit
  outside its profile family)"; carried to cycle 2.
- Note: the 400 MW column reuses P_line = 27 MW from the 500 MW column (not fully independent) — labelled.
