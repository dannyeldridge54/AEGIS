# Course (set 16 Nov 2026, from tonight's data) — accelerate overall performance
Evidence → rule. Ticks follow these rules; revisit weekly with the numbers below.
1. Compute where it survives. Cloud: 6 heavy runs killed tonight (runner time limit ×2, container restart ×1, OOM ×1, stalls ×2); PC: 0 kills, 16 cores. RULE: anything > 10 min goes to queue_pc.txt (results → field_tests/results/pc/); cloud only for < 10 min jobs and locks.
2. Fast route first, exact route as referee. Janus: 1 ms vs 40–70 s (n_s, r validated 24/24, D989). RULE: scans, sweeps and new-model exploration run on Janus; the exact solver runs only on the few points a lock names as checks (≥ 3 per scan, spread across the range).
3. Two routes always (it caught 5 own bugs in Level S, a 10× slip in D991, an answer-key leak in the CubeMind pair, a stale-file copy twice). RULE unchanged; add: no number stated to Danny before code produced it.
4. One driver per repo. Two sessions ran the same lock tonight (D981 DEVIATIONS D3). RULE: this session drives AEGIS; before every push fetch+rebase; a second session must claim a track in CURRENT_STATE before touching it.
5. Ticks on events, not on the clock. Many empty Jl ticks tonight. RULE: schedule the next check at the expected finish time of the slowest pending job (not every few minutes); an empty tick advances one standing track instead of only reporting.
6. Lock once, reuse. The release path (lock → PC → results/pc → note → package) worked; reuse it as a template for every track.
## CubeMind (data: qwen3-coder 0.760, qwen2.5-coder 0.613; code/reading ≈ perfect; math 4–31/50 and competition 16–29/50 weak; qwen2.5 confidently wrong, math Brier 0.92; pair LOSS but 97.7% correct when two models agree)
7. Base model = qwen3-coder:30b (best plain score). gpt-oss:20b (61/61 so far) is the challenger once its run completes.
8. Biggest lever = the calculator tool (Phase 4) on math/competition/errorspot (the weak 40% of the suite); verdict from the locked A/B.
9. Next method to lock: agreement gate (both agree → answer; disagree → stronger model's answer or "not sure"), using the 97.7%-when-agree signal; scored on Brier + accuracy.
10. Calibration matters as much as accuracy: report Brier next to accuracy everywhere; a confidently-wrong model is worse than a hesitant one.
## Research priority order (expected value per credit)
R ρ-tilt origin (could explain the last fitted main-branch number; cheap with Level S) → Z swampland scorecard + E eternal inflation (minutes with Janus) → J3 third order + J7 ASPIC benchmark (the release that turns heads) → S4 backreaction (long, highest ceiling) → W data watch (weekly).
