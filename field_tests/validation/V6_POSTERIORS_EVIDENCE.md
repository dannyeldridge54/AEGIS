# V6 — Full posteriors and Bayesian evidence (referee priority #1)

**Problem.** All headline numbers are maximum-likelihood/MAP estimates from Cobaya's minimiser (best of 2–4 restarts).
Referees expect marginalised posteriors (MCMC, Gelman–Rubin R−1 < 0.01–0.02) and a model comparison that penalises
prior volume: Bayesian evidence ratios ln B = ln Z_Twist − ln Z_ΛCDM, read on the Jeffreys/Trotta scale, beside Δχ²_min,
ΔAIC and ΔBIC.

**Scope (first pass).** Spiral (SF) and ΛCDM-halofit on Planck low-ℓ + ACT DR6 + Planck-cut + ACT lensing + SPT-3G +
DESI DR2 + {Pantheon+, DES-Dovekie, Union3}: 6 chains; then w0–wa on the same data (3 chains) for the like-for-like
extended-model comparison; Locked Twist (CAMB) later.

**Method.**
- Cobaya `mcmc` with the SF priors unchanged (locked in PREREGISTRATION_SPIRAL_FIT.md), oversampling fast nuisance
  parameters, covariance seeded from the minimiser Hessian; convergence R−1 < 0.02 and ≥ 30 effective samples per
  parameter.
- Evidence: (a) MCEvidence (Heavens et al. 2017, k-NN estimator on MCMC chains, no extra sampling); (b) PolyChord on one
  case as a cross-check, if installed on the PC; (c) Laplace approximation from the Hessian as a sanity bound.
- Report also: 1D/2D posteriors for κ, β_eff, f, H0, S8; prior-dominated directions flagged.

**Pre-registration.** Needs a locked rule before chains are read: thresholds (e.g. |ln B| < 1 inconclusive, 1–2.5 weak,
2.5–5 moderate, > 5 strong), the prior ranges (= SF's), convergence criteria, and what is reported if ln B and Δχ²
disagree.

**Cost.** AxiCLASS SPA evaluations are slow; expect ~2–4 days wall time for 6 chains on the PC (2 threads each).
Only after the current S8 fits and the bracket finish.

**Prep done (8 Nov).** This plan. **Next:** check PC for `polychord`/`mcevidence` (pip), estimate per-evaluation time
from the SF logs, draft the rule.
