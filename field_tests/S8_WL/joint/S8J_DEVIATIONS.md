# S8-J deviations (rule PREREG_S8_JOINT.md, unchanged)

## S8J-D1 (8 Nov 2026, ~11:25 UTC): gate G-J failed on the PC; code fixed to match the rule; no fit had run
- G-J at the Pantheon+ Spiral best fit gave chi2 2403.024 against the expected 2399.144 (difference 3.88).
- Cause: the S8 likelihood asked the theory for "omega_cdm". On the coupled build CLASS returns its present-day CDM
  density (which includes the coupling factor), not the sampled input. The rule fixes S8 with the input omega_cdm
  (as s8wl_score.py and S8-WL Part 1), so the code was wrong, not the rule.
- Fix: the likelihood reads omega_b and omega_cdm as aliases of the sampled inputs; sigma8 and H0 still come from
  CLASS. Cloud check at the same point: chi2_S8 = 6.109 (expected 6.11).
- The failed gate output is kept as results/s8j_gate_pc_D1fail.json and the log as s8j_pc_log_D1fail.txt. The gate is
  then rerun unchanged; fits start only if it passes.

## S8J-D2 (8 Nov 2026, ~11:30 UTC): gate run one process per run; JSON write fixed; no fit had run
- The first G-J run evaluated all six runs in one process. The Spiral runs load the coupled CLASS build first, so the
  three ΛCDM evaluations then ran on that build instead of their own (their chi2 came out 15–18 above expectation, a
  state carry-over, not a model result). The script also crashed writing numpy booleans to JSON.
- Fix: one process per run (`gate_pc <run>`), per-likelihood chi2 written for each, `gate_sum` combines them; booleans
  cast. The gate threshold and the rule are unchanged. Old outputs kept with suffix _D1fail.

## S8J-D3 (8 Nov 2026, 13:10 UTC): two extra restarts for each ΛCDM reference; rule unchanged
- The SF engine fits ΛCDM with best of 2 (as the stored SF ΛCDM references were), and the three ΛCDM+S8 fits ran that
  way (all converged, finished 06:10–06:47 CST). The rule says "best of 4" for the Spiral and "same treatment" for
  ΛCDM, which can be read as 4 for both.
- To remove the doubt in the conservative direction (extra effort can only help ΛCDM, i.e. work against the Spiral),
  each ΛCDM reference gets 2 more restarts (`s8_joint_fit.py more <run>` → cmp_<run>_more.json); the scorer uses the
  lower chi2. Started while the Spiral fits run. Nothing else changes.
