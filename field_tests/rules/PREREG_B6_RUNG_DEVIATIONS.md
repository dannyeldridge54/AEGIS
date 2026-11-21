# PREREG B6 — DEVIATIONS (written before the rerun)
## D1 (21 Nov 2026, 08:33 CT)
The first execution ran in the cloud container (2 CPU cores) and produced NO results in 8 CPU-minutes (the first (u, box) pair alone exceeded the estimate); at that rate the 18 pairs would exceed the 40-minute run limit. It was stopped with zero output (nothing seen, nothing chased).
Change: the identical script (same seeds 100·u + box index, same 400 starts, best 5, Nelder–Mead maxiter 4000, same boxes, targets, tolerances and readings) runs on Danny's PC with the (u, box) pairs spread over 4 parallel processes. Results are written to weave_data/b6_rung.jsonl on the PC and copied to field_tests/results/b6_rung.jsonl. No other change.
