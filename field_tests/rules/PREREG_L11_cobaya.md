# PREREG L11 — independent posterior check of L7 (Janus-LT w0waCDM, BAO + CMB compressed + Pantheon+) with Cobaya's MCMC
Locked 2026-11-17 before any L11 number. Likelihood: exactly L7's χ² (theory/janus_lt/l7_joint.py, D1042), log p = −χ²/2, passed to Cobaya 3.6.2
(arXiv 2005.05290) as an external likelihood. Sampler: Cobaya mcmc (adaptive Metropolis, its default), stop at Gelman–Rubin R−1 < 0.02 (Cobaya's
convergence test on chain splits), burn-in 30%. Priors uniform: w0 [−2.0, 0.0], wa [−3.0, 2.0], h [0.55, 0.80], ω_b and ω_bc ± 10σ around L7's CMB
prior means; L7's own bounds (w0 + wa < 0) applied as in L7.
Claims (L7: w0 −0.853 ± 0.053, wa −0.518 ± 0.200 from the Hessian at the MAP):
 C1 |posterior mean − L7 MAP| ≤ 0.5 σ_L7 for both w0 and wa; C2 posterior s.d. within ±30% of L7's σ for both; C3 R−1 < 0.02 reached.
All → L7 ERRORS CONFIRMED BY MCMC; else report which differs (non-Gaussian posterior or prior volume effects are possible and would be the finding).
Runs on the cloud box (background). Results: field_tests/results/janus_lt_l11_cobaya.txt (+ chain summary, + stamp).
