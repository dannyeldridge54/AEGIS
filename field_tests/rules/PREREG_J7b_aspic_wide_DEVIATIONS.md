# DEVIATIONS — PREREG_J7b_aspic_wide

D1 (17 Nov ~04:45Z, after the first `summary`, no numbers recomputed): the verdict line printed "NOT SHOWN" while
printing C1 True, C2 True, C3 True. Cause: C3 is a numpy bool and the code tested `C3 is True` (identity), which is
False for numpy.bool_. Fix: cast C1–C3 with bool() before the identity test. The scored data
(field_tests/results/janus_j7b.part.jsonl) are not rerun; only the summary is regenerated. Lock logic unchanged.
