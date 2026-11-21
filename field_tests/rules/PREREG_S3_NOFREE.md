# PREREG S3 — how many quark numbers are really free? Up on class 8, down on class ½ (τ_d = computed m = ½ minimum, D1778). Locked BEFORE computing.
Model w864, targets/tolerances/score as Q12/B6. Three levels:
(a) ZERO free couplings: all moduli = 1, all phases = 0 ⇒ report score and the 8 ratios.
(b) PHASES ONLY: moduli fixed at 1, the 4 phases (g_arg, f_arg per sector) free in [−π, π]; 400 starts (seed 18), best 5 Nelder–Mead (maxiter 4000) ⇒ report best score, fails.
(c) MODULI ONLY: phases 0, the 8 moduli free in [1/2, 2], same search (seed 28).
Readings (decided now): the quark sector needs "k free numbers" where k is the smallest level (0, 4 or 8) that reaches 0 fails. Report k. One run. Code theory/quarks/s3_nofree.py (runs in the cloud; 3 small searches).
