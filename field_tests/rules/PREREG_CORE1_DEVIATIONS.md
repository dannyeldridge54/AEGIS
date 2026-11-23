# CORE-1 deviations (written before any fix or rerun)
Run 1 (cloud, as locked): 66 tools. K1 PASS (every example validates), K2 PASS (no crash; every error has a message; 58/66 ran clean),
K4 PASS (68/68 ledger records, all fields), K5 PASS (wrong type and missing field named, tool not run), K3 FAIL: a cached call took
67.8 ms (> 20 ms) — identical, marked cached, linked to its source. Verdict: FAILED AS LOCKED.
Cause: specs() is rebuilt on every call and scans ~2,550 PREREG files for lock names. DEV-1: build the specs once per process (memoised).
K2 errors, classified: 6 are cloud-environment only (weave_verdict, weave_wtoday, weave_engine need the PC weave_tools; weave_control,
evidence_atlas, hyperion_bbn need the PC's aegis_current) — confirmed present on the PC; 2 are bad registry examples:
lock_verdict's example is a "..." placeholder and lhc_dt_limit's example passes the doc string "ATLAS_136|ATLAS_36".
DEV-2: the core carries corrected examples for those two (registry file untouched).
DEV-3 (Danny 10:26, "all data going into CubeMind to learn and grow"): every fresh, non-cached core call also writes one CubeMind
memory record (mindmem Store, source "aegis_core", topic = field, tier EVIDENCE for clean results, HYPOTHESIS for errors, kind
result/error) when mindmem is importable. Not part of the K tests; reported separately as K6 (record written per fresh call).
One rerun; the PC run (all 66 with the PC environment) is reported separately.
