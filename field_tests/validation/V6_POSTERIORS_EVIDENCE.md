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

## Status 9 Nov 07:41 UTC check-in
The step-6 schedule asked for a new draft rule. Not written: PREREG_V6_EVIDENCE.md was already locked (8 Nov, on
Danny's word) and its chains started on the PC 9 Nov 11:24 UTC (Pantheon+ first; Spiral, S8-L, ΛCDM × 4 chains;
see DATA_LOG). Differences between the schedule's request and the locked rule, reported, nothing changed:
- w0–wa is not in the locked V6 (the schedule asked for it). Adding it needs a new rule; cost about one more model's
  chains.
- Evidence tools: MCEvidence is not on PyPI; it installs from GitHub (yabebalFantaye/MCEvidence, HEAD ade1dcb) and is
  pure Python, so it is installed at scoring time. PolyChord is not on PyPI either (PolyChordLite needs a Fortran
  compiler); the locked rule does not use it.
- Per-evaluation time (Cobaya's own measurement, Spiral Pantheon+ chain 1, 11:30 UTC): CLASS 0.014 evaluations/s, i.e.
  **~71 s per theory call**, single-threaded on a loaded PC (3 flagship fits + 12 chains on 16 cores). Likelihoods are
  fast (ACT 155/s, Planck low-ℓ 500–1100/s), so CLASS is the whole cost.
- **Time estimate (rough):** R − 1 < 0.02 with 8 slow parameters usually takes ~2–5 × 10⁴ slow steps → **2.5–6 weeks**
  per chain at 71 s; ~1–2 weeks at ~20–30 s once the flagship fits finish and chains can use more threads. The
  Pantheon+ stage alone is weeks, not days; Dovekie and Union3 follow it. Options (not taken; Danny's call): give each
  chain the minimiser's covariance as its starting proposal (sampler tuning, priors untouched; would be a logged
  deviation), more threads per chain with fewer chains at once, or report the Laplace evidence (already in the rule as
  the cross-check) first.
