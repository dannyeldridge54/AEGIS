# C10 — Danny's order: get on the live CubeMind, move your work onto it, integrate (25 Nov 2026, 16:12 CST)

Danny, 16:10 CST, verbatim: **"You inform them that they need to get on the right version and take all the work that they've done and put it
onto the new one and integrate it."**

## The problem (checked on the PC, 16:09 CST)
- The CubeMind that is RUNNING and learning is `C:\Users\Danny\CubeMind_janus`. It is **not in Git**. Its core code: `mindmem/learn_loop.py`,
  `janus/curriculum.py`, `janus/curriculum_ladder.py`, `janus/grader.py`, `janus/loop.py`, `janus/autorun.py`, `janus/ufe_lens.py`,
  `janus/loomcore.py`, `janus/astro.py`, `janus/mission.py`, `field_engine/` (v1), `evalsuite/`, `aegis_tools/registry.py`, `weave_data/`.
- Your worktrees are of `C:\Users\Danny\Desktop\CubeMind_side_project`. None of those core files exist there. So your CubeMind work today
  (offline runtime `cubemind_offline.py`, the UFE field catalog `ufe_field_catalog.py` + sqlite, the Data Lense engine, research engine, etc.)
  never reaches the CubeMind that learns.
- Meanwhile the live CubeMind has stopped improving: derivations about 67% correct and flat since 20 Nov; qwen3:14b with verify gives BLANK
  answers on 77 of 80 competition questions today; tools mode drops qwen3-coder:30b to 3/50 on reading; the look-up-first memory fix
  (0.20 -> 0.75) was never built.

## The order, step by step
1. **Bring the live copy under Git without changing it.** Create a new branch `live-janus` in the private GitHub repo
   `dannyeldridge54/CubeMind` whose first commit is an exact copy of `C:\Users\Danny\CubeMind_janus`.
   - EXCLUDE data too large or too personal for Git (GitHub refuses files over 100 MB): `cubemind_memory.jsonl` (146 MB), `learn_log.jsonl`,
     `*.bak*`, `_d*/`, `_cards_stage/`, `.aegis_cache_test/`, model files, `evalsuite/scores/`. List every exclusion in `.gitignore` and in the
     commit message. Record the SHA-256 of `cubemind_memory.jsonl` and `learn_log.jsonl` in a `DATA_MANIFEST.md` instead.
   - Do the Git work in a COPY or a fresh worktree, not inside the running folder, so the learning loop is not disturbed.
2. **Work from that branch from now on.** All CubeMind work happens in worktrees of `live-janus`, not in `CubeMind_side_project`.
3. **Port your work onto it.** For each piece (offline runtime, field catalog, Data Lense, research engine/router/report, conditional observer
   core, anything else you built for CubeMind): add it on its own feature branch off `live-janus`, with its tests, and say in the commit what
   it replaces or connects to. Also bring in from AEGIS `unify-bg`: `tools/field_engine/` (engine v2, `ufe_pack.py`, `ufe_stages.py`, tests).
4. **Integrate, do not just copy.** Wire each piece into the live loop where it belongs (e.g. the catalog as the store the loop writes
   results to; the offline runtime as the job runner; Data Lense as a checker). Run the existing tests plus your own before each merge.
5. **Fix the three live faults first**, each as its own small change with a before/after score on the same eval set (3f8ff55f):
   (a) blank answers from qwen3 with thinking on (likely the thinking budget eats the reply); (b) use tools only on questions that need them;
   (c) look-up-first answers from memory.
6. **Deploy back to the running folder only when tests pass**, during a pause of the learning loop, keeping a copy of the files replaced.
   Never delete the memory or learn log.
7. **Report on the bridge** (INBOX entries): branch created, each port merged, each fix with its before/after scores, and the deploy.

## Rules
- Lock-before-run (C7) applies to the before/after scores: state the eval set and the pass rule before running.
- Danny's other instructions still stand (C8, C9, C004 team mode, C005 commit to full derivation and testing). This is in parallel: one checker
  session can lead the port while the leader keeps the UFE search going.
