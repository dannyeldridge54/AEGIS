# D2224 DEVIATIONS (written after referee round 6, before the one rerun). Run 1: 8450 points, 222 prefiltered, 3 stable (0.035%), none natural.
Referee round 6 (13 scratch engine runs): no stable point was lost in its sample, but the prefilter is unsafe by construction; M12 clamp is silent.
- DEV-1 prefilter: replace the alpha_s-linear map with a 1/alpha_s-linear map (slopes in 1/alpha from the same 3 engine points) and keep
  |1/alpha_pred - 1/0.118| <= 0.30 (~4 sigma in 1/alpha); every survivor run exactly.
- DEV-2 clamp: engine bisection range widened to 1e10-1e20 GeV; any M12 within 1% of a bracket end is REJECTED (no alpha_s reported).
- DEV-3 validity: one-loop DKL thresholds require M12 <= M_s. The model has no single M_s -> two named variants reported side by side,
  neither chosen: M_s = 0.1 M_P = 2.4e17 GeV and M_s = M_P = 2.4e18 GeV. (Removes points only; cannot move any point toward the target.)
- DEV-4 named convention variants (all reported, none picked): DKL argument L x {0.9, 1.0, 1.1} (the 2-torus vs 4-cycle modulus question
  and the omitted additive constant, ~10%); U(1) flux weight {1, 3/5}. Primary = (L x 1.0, U(1) weight 1, M_s = 0.1 M_P).
- Unchanged: the 2 sigma, proton and Hoyle criteria; the strand ranges; the reading rules. Look-elsewhere noted by the referee: the Hoyle
  window is narrow, so a fine discrete grid can hit it by chance - the stable fraction is the reported statistic, per the lock.
