# AEGIS BRIDGE — cloud coordinator <-> local agents (set up 24 Nov 2026 at Danny's request)

Purpose: one place where the cloud Claude session (coordinator: holds the full D-note record, locks, referee ledger) and the local
agents on Danny's PC (GitHub Copilot worktrees) exchange tasks and results.

Where it lives: on the PC at `C:\Users\Danny\Desktop\AEGIS_BRIDGE\` and mirrored in the AEGIS repo, branch `unify-bg`, folder `bridge/`.

How it works
- `TASKS_FROM_CLOUD.md`  — the coordinator writes tasks here. Local agents READ it at the start of every task.
- `SOURCES.md`           — where the real source files are, so nothing has to be treated as "unavailable".
- `STATE_OF_THE_WEAVE.md`— what is already derived, tested and decided (so work is not repeated).
- `REPORTS/`             — local agents WRITE one file per finished task: `REPORTS/<task-id>_<agent-name>.md`
                           (what was done, numbers, files, what is still open). The coordinator reads these and replies in TASKS.
Rules (same for both sides)
1. Lock before computing (PREREG + sha256). Run once. Fixes only via a DEVIATIONS file written first.
2. Honest labels: derived / literature / assumed / ESTIMATE / OPEN. A FAIL stays a FAIL.
3. Never publish, never push to master, never touch another agent's worktree or git. Reports are plain files here.
4. If a source is missing, say which file and stop that step; do not transcribe formulas from memory.
