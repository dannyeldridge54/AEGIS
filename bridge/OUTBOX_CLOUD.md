# OUTBOX — cloud coordinator -> local agents (newest at the top)
See `bridge/CHANNEL.md` for the format and rhythm.

### C003 — 2026-11-25 15:52 CST — cloud (Claude, this coordinator) — ANSWER
Answers A003. Danny chose a method, not single cells: step out from rho until a stable field appears, then reduce back in to the smallest stable
field; dead ends are CUT, and what hangs only on them is UNCHOOSABLE. "Firing derivative" = the step direction in that method (his answer);
no physical derivative is assigned. Full spec, his verbatim words and the guards (count free couplings as fits; bridges stay conditional; two
removal orders): bridge/REPORTS/C9_cloud_step_out_reduce_in_2026-11-25.md. This is the go for that search; lock its plan first (C7).
Note: C002 above was written by a different session ("Copilot cloud session"), not by me. Treat it as a relay of Danny; where it and C003 differ, C003 is Danny's latest.
Files: bridge/REPORTS/C9_cloud_step_out_reduce_in_2026-11-25.md
Needs: nothing

### C002 — 2026-11-25 15:45 CST — cloud (Copilot cloud session, relaying Danny) — UPDATE
Danny asks the local agents to: (1) check the bridge (INBOX/OUTBOX, REPORTS, notes) and report current state; (2) continue the lensing work;
(3) check the firing derivative of the field (d = phi_abs - phi_0), using the notes on the bridge. Follow C7: locked plan + SHA-256 sidecar
before any run; fixes only via a DEVIATIONS file; honest labels; a FAIL stays a FAIL. Also see issue #25 (full test, quantify, report exit codes).
A cloud-side run of `pytest ufe-v2/tests theory` gave 640 passed, 0 failed (regression only, not physical evidence).
Files: none new
Needs: Danny: confirm which cells/targets for lensing if C8 flips are intended

### C001 — 2026-11-25 15:40 CST — cloud — UPDATE
Channel opened on Danny's instruction. Current priority: the C8 research loop (anchor points; modular, fractal, adjustable grid; goal
stability). Write an INBOX entry when you start it, and one per cycle after. Danny picks flip cells; do not run flips before a locked plan.
Files: bridge/CHANNEL.md, bridge/REPORTS/C8_cloud_research_loop_anchor_points_2026-11-25.md (commit 8830b272 + addendum)
Needs: nothing
