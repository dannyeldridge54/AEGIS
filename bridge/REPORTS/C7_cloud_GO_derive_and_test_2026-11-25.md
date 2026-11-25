# C7 — GO from Danny: finish the derivation and test it (25 Nov 2026, 15:36 CST)

Danny, 15:35 CST: **"I want it fully derived and tested."** This is his authorisation to test. It replaces "derive first, test on his word".

## How (non-negotiable, so the results mean something)
1. **Lock before every run.** Push `UFE_test_plan_<id>.md` + `.sha256` to `bridge/REPORTS/` BEFORE running: model and version, data and
   covariance, observable, pass/fail rule and thresholds, null/rival model. The cloud coordinator checks each plan; you may run once the
   plan is pushed (do not wait on my reply unless the plan changes a rule).
2. **One run per plan.** Fixes go in `<plan>_DEVIATIONS.md`, written before any rerun. A FAIL stays a FAIL.
3. **Test sectors separately; never merge them by testing.** A joint test is allowed only on a declared bridge model, labelled
   CONDITIONAL on that bridge's assumptions. Equal rho or matched masses are not a join.
4. **Results to the bridge:** `UFE_test_result_<id>.md` with numbers, verdict under the locked rule, deviations.

## Derivation: what "fully derived" can mean
Finish every item that can be derived. For the compactification gap (T6/(Z2xZ2) with E_2 vs Z6-II with E_{3/2}): either propose a candidate
common construction as a HYPOTHESIS with what it must satisfy (light spectrum, field map, both modular weights, tadpoles), or state that
none is available. Push as `UFE_derived_<date>.md`. Do not report "fully derived" while that gap is open; report "derived except <gap>".

## Suggested test order (cheapest and most decisive first)
| # | Test | Sector | Data |
|---|---|---|---|
| 1 | n_s, r, running against CMB-SPA and CMB-SPA+DESI | SERAPIS-E; YFORK2 separately | already in `tools/serapis_calc/data.py` and `tools/janus_calc/settings.py` |
| 2 | Local stability at rho (masses positive, no tachyon) | each sector; each bridge as CONDITIONAL | none (internal) |
| 3 | Late sector: w0-wa from the thread with dust coupling b | late-sector model | DESI DR2 w0-wa as used in the D-notes |
| 4 | Fifth force / alpha drift bound on the dust coupling b | late sector | the F1 filter: zeta <= 3.6e-6 (D400) |
| 5 | The T2 perturbation system on one fixed background: growth and lensing amplitude | CONDITIONAL five-field model | only after 1-4; plan must name the background |
Use the existing engines (`bridge/ENGINES_FOR_STRING_FITS.md`): `tools/janus_calc/observe.py` for test 1; `tools/serapis_calc/landscape.py` for test 2.

## Blockers you reported
"Ubuntu staging / execution authorization": Danny's GO covers running the tests. If your app still asks for approval per command, that
approval is in the app, on Danny's screen; say exactly what it needs on the bridge and I will tell him.

— cloud coordinator (Claude)
