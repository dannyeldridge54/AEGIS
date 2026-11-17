# PREREG D979: Project H with C refitted to the published n_s (follows D977): does r alone distinguish it from SERAPIS-E?
Model: V = P3(lambda' Ehat)(1 + C Ehat), paper convention, lambda' = 1/E(rho,2) = 0.1729 (the full-mass route's maximum, D947).
Target: n_s equal to the lambda' = 1 model's n_s at C0 = 1.15e-6 under the same reheating rule (T_R = 6.7e9 GeV * lambda'^(1/4), N* self-consistent), i.e. n_s_target = 0.97403 (D977 baseline row, recomputed in-run with the same code).
Method: solve for C (bracket [0.1, 3] x lambda' C0, brentq on n_s(C) - n_s_target, tolerance 1e-5 in n_s), spectra_fast (validated for n_s, r), start Ehat = 5000/lambda', assert Ntot >= N* + 8.
Report: fitted C, N*, n_s, r, and r/r_baseline - 1.
Outcome (fixed now): if |r/r_baseline - 1| < 3%: "Project H indistinguishable from SERAPIS-E by (n_s, r) at the 3% level"; if >= 3%: "Project H predicts r differing by X% at equal n_s: a test for LiteBIRD-class sigma(r)".
Script theory/flux/projH_nsmatch_d979.py; output field_tests/results/projH_nsmatch_d979.txt. Runs on Danny's PC queue (queue_pc.txt).
