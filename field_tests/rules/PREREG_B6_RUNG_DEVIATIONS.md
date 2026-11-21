# PREREG B6 — DEVIATIONS (written before the rerun)
## D1 (21 Nov 2026, 08:33 CT)
The first execution ran in the cloud container (2 CPU cores) and produced NO results in 8 CPU-minutes (the first (u, box) pair alone exceeded the estimate); at that rate the 18 pairs would exceed the 40-minute run limit. It was stopped with zero output (nothing seen, nothing chased).
Change: the identical script (same seeds 100·u + box index, same 400 starts, best 5, Nelder–Mead maxiter 4000, same boxes, targets, tolerances and readings) runs on Danny's PC with the (u, box) pairs spread over 4 parallel processes. Results are written to weave_data/b6_rung.jsonl on the PC and copied to field_tests/results/b6_rung.jsonl. No other change.

## D2 (21 Nov 2026, 08:45 CT; referee loop-1 item 13)
D1 said "No other change", but the script's import path also changed from tools/weave_cm/ to the script's own folder. On the PC that folder holds weave_tools.py = repo commit dfc76535 (md5 83f42470…; identical to HEAD except the later weave_mbb tool and its self-test line, which B6 does not use) and weave_sweep.py md5 c881df1a… (= repo HEAD). Recorded; no effect on the B6 procedure.
