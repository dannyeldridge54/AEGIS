# D2239 DEVIATIONS (after run 1, before the one rerun). Run 1: all six starts stopped after one rotation, every point "no_solution".
Cause (diagnosed, not a code crash): the locked coupling leaks the required SOL argon (c_SOL ~1-2 >> 0.05, D2238-B) into the core as
f_Ar = c_SOL/3, which kills the burning plasma, so every point and every neighbour scored the same flat -99 and the rotation could not move.
- DEV-1 (scoring design error): a point whose seeded second pass has no solution is scored by its first-pass seeding violation,
  -(c_SOL/0.05) - 10, so the rotation can walk toward lower exhaust load (core radiator, longer leg, lower power). Feasibility rules,
  ladders, starts and objective unchanged.
