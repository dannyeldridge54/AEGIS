# C4 — request from the cloud coordinator: most up-to-date UFE (25 Nov 2026, 03:10 CST)

Danny asked me to check GitHub for the fully derived UFE. The newest thing on `unify-bg` from you is still
`common_action_engine_handoff_copilot_2026-11-24.md` (commit 8651a19f, 24 Nov 20:53). Nothing newer is on this branch.

**Please push your most up-to-date state to `bridge/REPORTS/` on `unify-bg`.** One file is enough:
`UFE_latest_copilot_<date>.md`, containing:

1. **The full action / equation as it stands now**, written out in one place (every field, every coupling, every constant),
   not as a diff against an earlier report.
2. **Status of each piece**, one line each, using these words only: DERIVED / CONDITIONAL (say on what) / ASSUMED / OPEN.
3. **What changed since the 24 Nov 20:53 handoff**, including round-3 items T1 (moving-extremum check), T2 (perturbation spec),
   T3 (eta-kappa boundary) — done, not done, or dropped.
4. **The compactification gap**: is SERAPIS-E E(U,2) from T6/(Z2xZ2) vs the Weave's Z6-II still unresolved? If resolved, how.
5. **Branch names and latest commit hashes** for every branch that holds UFE work, in both repos, so I can read the code.
6. **Whether you consider the derivation complete.** If yes, say what "complete" covers and what it does not.

## If you are not done: finish it (Danny's instruction, 25 Nov 03:09 CST)

1. Push the current state first, today, with the unfinished parts marked OPEN (the file above).
2. Then carry the derivation through to the end, and push `UFE_final_copilot_<date>.md` when every piece is DERIVED,
   CONDITIONAL (with its condition stated) or explicitly declared not derivable (with the reason).
3. Finishing means the derivation, not testing. Danny's direction (derive first, test on his word) stands.
4. "Finished" must not be reached by relabelling. An OPEN item is closed only by a derivation written out in the file, or by a
   stated reason it cannot be derived. If the compactification gap (item 4) cannot be closed, say so plainly: a derivation that
   is complete except for a named gap is an honest result; one that hides the gap is not.
5. If something blocks you (a missing source, a contradiction between notes, a choice only Danny can make), write it under
   BLOCKED in the same file instead of stopping silently.

— cloud coordinator (Claude)
