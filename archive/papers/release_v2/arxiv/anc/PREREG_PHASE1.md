# Pre-registration: Phase 1 of the master plan (making the result referee-proof)

Written 29 October 2026, about 23:00 CT, by Danny Lee Eldridge, **before any of the runs below has started.** Nothing
in this file may change after it is locked; the guardrail check fails if it does. Any deviation is added only in a
separate dated file, `PREREG_PHASE1_DEVIATIONS.md`, and reported beside the result.

Common to every step:
- **Data:** P-ACT (Planck 2018 cut + ACT DR6 + ACT DR6 × Planck PR4 lensing) + DESI DR2 BAO + Pantheon+, no SH0ES,
  exactly as in the blind test, unless a step says otherwise.
- **Models:** ΛCDM; Locked Twist (2 extra settings: f_EDE, θ_i; onset at equality); Twist-1H (1 extra setting: θ_i;
  onset at equality and F = √(3/2) M_Pl / 9).
- **Priors:** f_EDE uniform on [0, 0.30]; θ_i uniform on [0.1, 3.1] rad; all ΛCDM parameters as in the blind test.
- **No retuning:** no data, prior, setting or rule is changed after the first result of a step is seen.

## 1.1 MCMC posteriors
- Cobaya MCMC, 4 chains per model; stop when Gelman–Rubin R − 1 < 0.02 on every parameter.
- Report: the mean and 68% / 95% intervals of f_EDE, θ_i and H₀, plus triangle plots, for every model.
- **Rule:** *posterior supports early dark energy* if the 95% lower limit of f_EDE in the Locked Twist is above 0.01;
  otherwise *posterior consistent with no early dark energy*. Both outcomes are published. Prior-volume effects are
  named as a possible cause in the second case, never used to override it.

## 1.2 Profile likelihood in the divisor N
- F = √(3/2) M_Pl / N for N = 6, 7, 8, 9, 10, 11, 12 (onset locked; f_EDE and θ_i free), minimised 3 times per N.
- Report Δχ²(N) relative to the minimum, on P-ACT and on Planck 2018 + DESI DR2 + Pantheon+.
- **Rule:** *9 is consistent* if Δχ²(9) − min Δχ² < 1 on P-ACT; *9 is disfavoured* if it is between 1 and 4;
  *9 is excluded* if it is 4 or more.

## 1.3 Exact field solution
- Re-run the Locked Twist and Twist-1H best fits with a code that solves the scalar field exactly (AxiCLASS or CLASS
  with a scalar field) instead of the fluid approximation, re-minimising all parameters.
- **Rule:** *the fluid approximation holds* if Δχ² vs ΛCDM agrees with the CAMB fluid result to within 0.5. If not,
  the exact result replaces the fluid one everywhere, and the difference is reported.

## 1.4 Full weak-lensing likelihood
- Add the DES Y3 cosmic-shear likelihood (and, separately, KiDS-Legacy if a public Cobaya likelihood is available)
  in place of the S8 penalty, and re-minimise ΛCDM and the Locked Twist on P-ACT + DESI DR2 + Pantheon+ + lensing.
- **Rule (replaces item 4 of PREREGISTRATION_VERDICT.md for this data):** *preferred* if Δχ² < −4 with each lensing
  set; *tie* if −4 ≤ Δχ² < −2 with either; *noise* if Δχ² ≥ −2 with either.

## Decision point A
- If 1.1 gives *consistent with no early dark energy* **and** 1.4 gives *noise*, the front page of the repository says,
  in the first paragraph: "The evidence for the Twist fell below 1.5σ with full posteriors and weak lensing. The model
  is paused." No further runs are made until a new theory step (Phase 2) changes the model, with a new pre-registration.
- Otherwise, Phase 2 begins, and every result here is reported, including any that weaken the case.
