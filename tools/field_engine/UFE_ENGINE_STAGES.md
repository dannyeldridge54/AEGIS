# UFE Engine — staged plan (25 Nov 2026)

Built on the local agents' final derivation audit (`bridge/REPORTS/UFE_final_copilot_2026-11-25.md`). That audit's own
conclusion is the starting fact: **there is no single sourced UFE action.** There are three separate source sectors, four
proposed bridges, and eight open or blocked gates. So this engine does not "run the UFE". It runs the audit: it computes
what is derived, keeps the sectors apart, and works the open gates in order.

Staged like the Loom (centre outward, each stage has its own referee and a gate before the next), with five capabilities the
earlier staged setup did not have. Status words: DONE = built and tested; BUILT-UNTESTED; PLANNED.

## The stages
| # | Stage | What it does | Gate before the next stage | Status |
|---|---|---|---|---|
| 0 | Record | The audit as data: 3 sectors, 4 bridges with the assumptions each rests on, 8 gates | Every item carries a status and a source section | DONE (`ufe_pack.py`) |
| 1 | Relations | 7 derived or conditional relations as tools, each with an independent second method | Every tool passes its tester on all ranges; a wrong formula is caught | DONE (6 tests, mock models) |
| 2 | Exact numbers | Code-only fitters from `tools/serapis_calc`: E_2(rho), E_{3/2}(rho), the vacuum finder, the three local masses (2 V0 E_2(rho), V_inf/4, V_L/4). No model is asked | Fourier series and direct lattice sum agree; normalisation (coprime-pair vs full lattice) stated on every number | DONE (D2259): 18 of 18 checks pass; E_2(rho) = 5.78335929968, E_{3/2}(rho) = 8.89274510040 (full lattice) |
| 3 | Symbolic check | Each derivation step in the audit re-derived by computer algebra (the moving-extremum slope, the Kahler determinant, the Hessian blocks, the flux-bridge masses) | Every step either reproduces or is listed as a discrepancy for the agents | DONE (D2259): 18 of 18 reproduce |
| 4 | Contradiction finder | Every bridge's consequences computed side by side; any two that disagree are reported (the audit found one by hand: V_w = 32 vs 8 V0 E_2(rho)) | The known contradiction is found automatically; new ones go to the bridge | DONE (D2259): 4 disagreements listed; claims are declared by hand from the audit, so it groups what it is told and does not yet discover new ones |
| 5 | Layered pulse | Stages 1-4 run in order on every pulse, centre outward: mathematics, single sectors, bridges, late sector, perturbations. A layer is not pulsed until the one inside it is solid | The Loom's own checks pass (independence, false-alarm control) | PLANNED |
| 6 | Gate worker | Each open gate becomes a work order: what input would close it, who can supply it, what file would count as closing it | A gate closes only when a derivation file with a hash is attached; never by relabelling | PLANNED |
| 7 | Perturbation system | The audit's conditional five-field linear system (T2) as code, with its two constraint checks | Built and unit-tested on a known case only. **No scans or runs on the model until Danny says test** | PLANNED |
| 8 | Real models and speed | The engine on the PC's local models; three samples each, one model at a time | Ledger verifies; speed and accuracy recorded | BUILT-UNTESTED |
| 9 | Into the machine | The pack, its ledger and the gate list go into the knowledge pack with their labels | The machine answers a UFE question with the status and the model it belongs to | PLANNED |

## What makes it more capable than the earlier staged setup
1. **Status travels with every number.** Each lock in the ledger records DERIVED or CONDITIONAL, the model the relation
   belongs to, and what it must not be read as. The earlier engines recorded PASS or FAIL only.
2. **Sectors cannot be merged by accident.** `combine(a, b)` returns False unless a declared bridge joins them, and then
   returns the assumptions that bridge rests on. The Weave and SERAPIS-E have no bridge: the answer is OPEN.
3. **Open gates cannot be learned.** OPEN and BLOCKED items are refused as tools and printed at the start of every run.
4. **Models are asked last.** Stages 2-4 are code and computer algebra only; models are used at stage 1 and 8 for derivation
   practice, never to decide a result.
5. **It looks for its own contradictions** (stage 4) instead of waiting for a referee to notice them.

## What it cannot do
It cannot close the compactification gap. That needs a physical construction (a common light spectrum and field map between
T6/(Z2xZ2) and Z6-II) that is not in any source. The engine can show exactly where the gap is and check any proposed join;
it cannot supply one.

## Run
    python engine.py --pack ufe --models qwen3:14b qwen3-coder:30b --cycles 28
    python3 tools/field_engine/ufe_stages.py           (stages 2-4, from the repo root, about 3 s)
    python -m unittest test_engine test_ufe_pack test_ufe_stages       (20 tests, no models needed)
