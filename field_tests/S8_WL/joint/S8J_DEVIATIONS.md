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
