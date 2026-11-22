# PREREG D1988: close the test gaps found by D1982 B4. Locked at this commit, before the new tests are run.
B4 (after the O7 fix, with the controls PASSing) scored a kill rate of **13/18 = 0.72 < 0.8: FAIL. That stands.**

New tests, added to tools/loom/test_loom_battery.py as B8. Each targets a survivor:
| test | targets | what it does |
|---|---|---|
| B8a | planner, "and not alarms" | every endpoint condition is met (all layers LOCKED, no fits, 7 nulls, killable 4, referee signed, E3 True), but a G-T3 alarm fires. The endpoint must be **not reached** |
| B8b | planner, holds ignored | N0 holds L2 and orders derive for L4. A spent fit whose layer is L2 must **not** appear among the actions |
| B8c | lens_core, 15° threshold | two rank-1 lenses at 10° must classify PASS |
| B8d | lens_core, 75° threshold | lenses at 80° must classify BLOCKED |

**Declared equivalent (not counted):** the mutant forcing rank ≥ 1. It changes behaviour only for a nonzero matrix with numerical rank 0, which cannot occur because s > 1e-3·s.max holds for at least s.max itself. It is equivalent by construction (Jia & Harman 2011, on equivalent mutants).

Then B4 runs once with the same 18 mutants. Score = killed / 17 non-equivalent. Bar ≥ 0.8.

B8a needs the planner's E3 to be evaluable (D1980a). This lock therefore also fixes the planner:
- E3 is read from field_tests/loom/four_corners.json;
- E5 is read from field_tests/loom/referee_signoff.json;
- a missing file means False;
- the endpoint requires E1–E5 all True and no alarms.
