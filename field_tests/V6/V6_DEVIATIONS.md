# V6 deviations (written before the change is run)

## V6-D1 (9 Nov 2026, 12:50 UTC; Danny "Ok" at 06:41 CT to options a + c)
- **What:** the first V6 chains (started 11:24 UTC) had no starting proposal covariance; measured cost ~71 s per CLASS
  call on the loaded PC → 2.5–6 weeks for the Pantheon+ stage. They are stopped (about 1.5 h of burn-in discarded,
  nothing read from them) and restarted with a proposal covariance from a **Laplace step**: the numerical Hessian of
  −ln(L × prior) at each stored best fit (`v6_laplace.py`, central differences, step 0.25 × the fit's proposal width).
- **Unchanged:** likelihoods, priors, builds, R − 1 < 0.02 on 4 chains, MCEvidence as the evidence, readings.
- **Same step gives the rule's cross-check early:** the Laplace ln Z for all 9 runs is reported as soon as it exists,
  labelled "Laplace (cross-check), chains not converged", with no verdict word until MCEvidence on converged chains.
- **Gate:** the Hessian centre must reproduce the stored −ln posterior within 0.05; a non-positive-definite Hessian is
  reported and gives no Laplace number (the chain then starts from a diagonal proposal).
- **Clarification (V6-D0):** the 4 chains per model are independent processes (no MPI); the cross-chain Gelman–Rubin
  R − 1 is computed over the 4 chains before anything is read.
