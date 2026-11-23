# PC revert incident (23 Nov 2026, found 18:41 UTC)
The PC restarted ~18:39 UTC (watchdog relaunched ollama, grading loop, learn loop, weave pool at 12:39-12:40 CT). Afterwards 10 files in
CubeMind_janus were OLDER than their own newest backups (learn_loop.py and registry.py = 21 Nov versions; weave_tools.py, weave_sweep.py,
store.py, WEAVE_FACTS.txt older still; aegis_bundle/tools/fusion/fusion_cm.py missing) and cubemind_memory.jsonl had no records between
22 Nov ~06:00 UTC and 23 Nov ~18:00 UTC. New files survived. Cause unknown (not a restore by Danny; CubeMind_backups holds only a 31 Oct zip).
Restored 18:55 UTC (Danny's choice "re-apply"), reverted copies kept as *.reverted_23nov:
- registry.py <- .bak_cards_23nov (+ CM-CARDS tools); learn_loop.py <- .bak_cards_23nov (+ CM-CARDS prompt + DEV-4/5); fusion_cm.py <- stage;
- weave_tools.py <- .bak_v5b_22nov + v5b block; weave_sweep.py <- cloud tools/weave_cm (= bak_pool_20nov + pool sharding/merge);
- store.py <- store.py.FIXED_0215 (QA1 adopted weights); WEAVE_FACTS.txt <- v5 facts (.bak_v5c_22nov).
Memory: playbook + 119 element cards re-added. NOT recoverable: CubeMind's own records 22 Nov 06:00 -> 23 Nov 18:00 UTC (no copy found).
Check: registry 78 tools; nuclide_binding, fusion_sigmav, weave_verdict return correct values.
