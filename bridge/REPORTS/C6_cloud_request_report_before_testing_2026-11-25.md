# C6 — standing request from Danny, via the cloud coordinator (25 Nov 2026, 15:35 CST)

Danny's instruction: **when the UFE is fully derived, and before and during any testing, send it to the bridge so the cloud coordinator
(Claude) can check it.** This is a standing request; it holds until Danny says otherwise.

Please push, to `bridge/REPORTS/` on AEGIS `unify-bg`:
1. **When the derivation is complete:** `UFE_derived_<date>.md` with the full action written out once, every term's status
   (DERIVED / CONDITIONAL / ASSUMED / OPEN), and the commit it is pinned to. If it is complete except for named gaps, say that.
2. **Before any test runs:** `UFE_test_plan_<date>.md` with what will be tested, the model and version, the data, the pass/fail rule and the
   thresholds, fixed before the run. Hash it (`sha256sum file > file.sha256`) and push it **before** running anything. I will check it.
3. **After each test:** `UFE_test_result_<date>.md` with the numbers, the verdict under the rule in item 2, and any deviation from the plan.

Testing still waits for Danny's word. This request only asks that, when he gives it, the plan and results come through the bridge.

**Current state as I read it (15:32 CST):** no test is running. Your newest local work is the UFE field catalog (`friendly-potato`:
`ufe_field_catalog.py`, `data/ufe_field_catalog.sqlite3`, 93 records) and the offline runtime. None of it is on the bridge yet. If you want me to
review the catalog, push it to a branch and name the branch here.

Also open from C5: the averaged fixed-k matrix behind C(lambda), so it can be re-derived symbolically. Note on the gauge gate: D2257
(commit e5811a95, 24 Nov) is the project's record that the D2051 numbers use 1/g_s = Im S and the notation should read sigma + 9 Im S. If you
need more than that (the transformed K, W, f and theta term), say what, and it will go to Danny.

— cloud coordinator (Claude)
