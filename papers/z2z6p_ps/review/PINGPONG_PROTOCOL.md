# Ping-pong derivation protocol: two poles meeting at the null (as run on 22 Nov 2026, D2110–D2121)

## Roles
- **Positive pole (builder, the main session).** Starts from **what we have**: the current formula, code and results. Adds, computes and fixes.
- **Negative pole (referee, a background agent).** Starts from **the opposite end: what is missing or wrong**. It never edits the repo. It runs only short checks in /tmp/claude-0/referee/. It is spawned with the Agent tool (general-purpose, run_in_background) and continued with SendMessage, so it keeps its context between rounds.
- **The centre is the null.** The loop for an item closes only when a referee round returns **"NULL — BALANCED"**: nothing at blocker or major level, and nothing new to add.

## Per item (each "equation" or test)
1. **Builder opens from its end.** State exactly what we have: formula, source (paper and line), code path, current verdict.
2. **Referee opens from the other end.** Report what is missing, wrong or overstated, ranked by severity.
   - Each finding has: ID | severity (blocker / major / minor) | CONFIRMED or SUSPECTED | file:line | problem | evidence (a calculation, or a quote with its line) | fix.
   - The referee also proposes at least one **online-sourced fold-in** (with URL), and names what to add.
3. **Builder answers.**
   - Write the lock first: PREREG_D###.md + .sha256, committed and pushed **before** computing.
   - Code fixes after a lock go in *_DEVIATIONS.md, written **before** any rerun.
   - Pass criteria are fixed before any output is read (addenda allowed only before reading).
   - Compute once. Record a D-note with numbers and verdict. Corrections get their own dated note (e.g. D2120a); nothing is edited silently.
   - Report back to the referee what was added, with file paths, plus the builder's own search finding.
4. **Ping-pong** micro-rounds: about one search plus one check per round, returning fast (search time + 5–10 s of thinking). The builder works outward (adds) while the referee works inward (removes errors). Triangulation is when both land on the same thing independently; record it.
5. When the referee says the item is **ready to test**, run the locked test. Then derive and record the verdict: PASS / FAIL / OBSTRUCTED / CONDITIONAL / FLAG / ESTIMATE / OPEN.
6. **The final sweep for the item** returns "NULL — BALANCED". Update the paper and ledger, commit and push, then **move straight on to the next item** in the checklist.

## Integrity rules (never relaxed)
- Never loosen tolerances. No reruns to chase a result. A FAIL stays a FAIL.
- Literature formulas are quoted with their line numbers. Interpretive readings, such as typo corrections, are disclosed in the PREREG.
- When the referee is right, say so, fix it, and log a correction note.
- No publishing (arXiv/Zenodo) without Danny's explicit "Publish".
- Keep cost low: micro-rounds, short scripts, one referee agent at a time.

## Lessons from the first run
- **Grid searches miss minima.** Use constrained optimisation over solution curves (R1-1).
- **Check normalisation conventions against the source line** (the 4π/g² = 2π Re f issue, R1-2).
- **Caps and truncations must be removed or reported** (the 5,000 cap, R1-4).
- **Necessary is not sufficient.** Test discrete symmetries on the exact integral lattice (unimodularity, det = 1) and calibrate on a published model (R2-3, R2-6, R2-7).
- **Bibliography and caveats are part of BALANCED** (R2-12, R2-13).
