# D1984 DEVIATIONS
- **O7 (01:16Z, before the one B4 rerun).** Cause of D1982's VOID: in a temp copy, planner.py found the repo root from its own file location (tmp/..). That failed test_planner's toolkit-existence case on every copy, mutated or not.
  - **Fix:** planner.py honours the env AEGIS_ROOT, and the runner sets it. The tests and the 18 mutants are unchanged.
- **O1–O4** were carried out under PREREG_D1986 and PREREG_D1987 (the woven field and two detectors) instead of a separate D1984 run. D1986's O2 FAILed and D1987 superseded its detector.
