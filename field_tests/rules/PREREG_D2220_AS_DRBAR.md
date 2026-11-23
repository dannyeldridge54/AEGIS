# PREREG D2220 (ping-pong item 2 alpha_s, round 2; written before computing, 23 Nov 2026)
Referee finding (standing referee, round 2, #2): the Weave alpha_s engine (theory/tests/d1944_as_yukawa.py, = weave_rg2 + top Yukawa) runs SM
couplings (MS-bar) into the MSSM regime above m_scalar 4.7e5 GeV and imposes unification there WITHOUT the MS-bar -> DR-bar conversion.
Sourced fix (Martin & Vaughn 1993, hep-ph/9308222; already used in our D2123 K7 code, tools/seed/z2z6p_k7_robust.py:19):
1/alpha_i(DR) = 1/alpha_i(MS) - C_A(G_i)/(12 pi), C_A = (0, 2, 3), applied once at the SM->MSSM matching scale m_scalar (upward running).
Only change. Same betas, Yukawa term, spectrum (wino 686.5 GeV, gluino 4926.4 GeV, m_s 4.7e5 GeV, tan beta 2).
Report alpha_s(M_Z) MS-bar; pulls vs 0.1180 +- 0.0009 (exp only) and with the computed theory sigma of D1944 (0.00057).
Pass: |pull_with_theory| <= 2 -> IN-candidate; else OUT stays. The validation guard (no-conversion run reproduces 0.11401 with Yukawa) must hold.
Expectation stated by referee: likely to WORSEN alpha_s; a FAIL stays a FAIL.
