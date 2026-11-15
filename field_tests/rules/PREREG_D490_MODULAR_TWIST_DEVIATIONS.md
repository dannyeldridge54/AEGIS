# D490 DEVIATIONS (written before rerunning)
D1. Control (0) failed (n_s = 0.33, r = 5.3): my script used V = |F|²/(T+T̄)³, which is not the Twist's potential. The repo's inflation code (theory/inflation/cliff_v2.py,
used by D419) has V = |F|²/(4x²) on the real line, F = T/√(1+T/μ)·exp[−n(1 − e^{−T/m₂})], n = 125.0 (NN in cliff_v2; the '124.1' I carried in my summary is
the older value). Fix: (a) V = |F|²/(4x²); (b) the duality condition becomes F(1/x) = F(x)/x², so F_sym = G(x) + x² G(1/x) (V_sym(1/x) = V_sym(x) exactly);
(c) control uses n = 125.0. Everything else (tests (i)–(iii), N* = 57.2, pass criteria) unchanged. The failed first output is kept as results/modular_twist_d490_run1_bug.txt.
D2. Edit bug in applying D1: the inline comment swallowed the rest of the F_sym line (TypeError, no numbers produced for the symmetric case). Fix: move the comment. Control (0) already passed in that run (n_s 0.9651 / 0.9736).
