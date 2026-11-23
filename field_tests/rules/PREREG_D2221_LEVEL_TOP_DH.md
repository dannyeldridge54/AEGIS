# PREREG D2221 (ping-pong round 3 fixes; written before computing, 23 Nov 2026)
Two sourced omissions found by the standing referee (round 3), each a single change; pass criteria fixed here.
(A) alpha_s engine (theory/tests/d2220_as_drbar.py): no top decoupling - 6-flavour SM betas used from M_Z. Fix: below m_t = 172.6 GeV remove
the top from the ONE-loop SM betas, Delta b = (17/30, 1/2, 2/3) subtracted (textbook decoupling; two-loop matrix and finite threshold
pieces unchanged - stated approximation). Report alpha_s(M_Z); OUT unless |pull_with_theory| <= 2 (sigma_th 0.00057, exp 0.0009).
(B) D/H pull (hex.py Nuclear): the omega_b input error is not propagated. Fix: add sigma_wb = |dDH/d omega_b| x 0.00015 (Planck 2018
omega_b 0.02237 +- 0.00015; derivative by central difference of the locked PRIMAT table) in quadrature with obs 0.025e-5 and PRIMAT theory
sigma. Observed value stays the locked PDG 2.547 +- 0.025e-5 (Cooke 2018 2.527 +- 0.030 shown, not scored). Status rule: |pull| <= 2 IN,
2 < |pull| <= 2.2 EDGE (the stage map's last-10%-of-band rule), else OUT. Rates (PRIMAT) not switched.
