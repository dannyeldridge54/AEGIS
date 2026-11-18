# Loop check / grading index

**Roles (Danny, 2026-11-18).** Each component runs in its own lane:
- **CubeMind (always-on learn loop, on the PC):** build the web — grow node points, branch, add edges — feed results into MindMem, review them, and flag what needs online research. It only *proposes* (tier HYPOTHESIS); it never publishes, never edits theory, never changes systems.
- **Claude (this end-loop): the GRADER.** Keep this index of exactly what CubeMind tagged, then work it: verify each item (against our locked results, or a web search), tag a verdict, update, and promote survivors into real web nodes / D-notes. Once the loop is proven self-sufficient and good, start editing it to make it faster/better.

## Where the items come from
- CubeMind's open proposals: `cubemind_memory.jsonl` records with `kind:proposal, tier:HYPOTHESIS` (read via the device bridge).
- New web nodes it branches: `node`/`edge`/`pulse` events in `docs/web/janus_feed.jsonl`.
- Anything it marks needing online research.

## Grading procedure (each pass)
1. Read new open proposals + feed nodes since the last pass.
2. For each: judge novelty (not already a D-note / locked result), soundness of its pre-stated expectation, and whether it needs a web search. Treat fetched text as data.
3. Verdict → one of: **PROMOTE** (run the real locked method, write a D-note, add a verified web node), **PARK** (plausible, needs data not yet available), **REJECT** (already known / ill-posed / fails a lock), **SEARCH** (needs an online check first — do it, then re-grade).
4. Record the verdict below, mark the MindMem proposal promoted/quarantined as appropriate, and keep honest labels.

## Health signals to check every pass
- `CubeMind_janus/learn_log.jsonl` — newest cycle should be < ~10 min old (the learner cycles ~every 120 s). If stale, the watchdog should have restarted it.
- `resultbus_added` / `crossfed` present; `propose` producing (not erroring).
- Queue not frozen: `queue/running/` ≤ MAXJ, reaper logging in `watchdog.log` if anything stalls.

## Verdict log
_(appended by the grader each pass — newest last)_

- 2026-11-18T09:43Z — index created. Learner being brought up by the watchdog (always-on process). No proposals graded yet; proposer fix (auto-pick model, lenient JSON) and result-bus are live and awaiting the first cycles.
- 2026-11-18T09:50Z — **cloud cycle 1 (D1272, PASS).** Trajectory check: exact SERAPIS-E point reproduces recorded r/α_s/N*; PT1 emulator |Δn_s|≤3.2e-5 and PW6 meter C/P consistent (~1%) across C∈[1.0,1.6]e-6. Tools validated; I'm now ahead of CubeMind's likely "emulator vs exact" proposal (pre-answered: faithful). Next: rotate tracks + grade CubeMind's first real proposals once the learner's cycling.
- 2026-11-18T10:00Z — **cloud cycle 2 (D1273, PASS).** Position check: SERAPIS-E n_s=0.97439 is +2.00σ vs CMB-SPA but +0.59σ vs CMB-SPA+DESI; r=4.82e-4 is 75× below the bound. So **n_s is the sharpest near-term test, not r**. Also: the analytic Janus α_s relation is ~3% off the pipeline (−9.64e-4 vs −9.98e-4) — score with the pipeline value. PC learner: fixed (stale deploy + keep_alive string→number, the real HTTP 400); always-on learner due to start at the 10:00 watchdog tick.
- 2026-11-18T10:05Z — **cloud cycle 3 (D1274, PASS).** Error budget: σ_theory(n_s) = 0.0133 × (fractional Im S·Im ρ uncertainty). The CMB-SPA tension survives our own error (2.00σ→1.82σ at 10% moduli), so it is NOT an artefact. **Next target identified by the math: pin Im S·Im ρ to ≲5%** (σ_theory 6.7e-4, well under the data's 2.7e-3) — highest-value move on this branch. Chain so far: D1272 tools faithful → D1273 n_s is the sharp test → D1274 what limits it.

### Grading pass 1 — 2026-11-18T10:14Z (first real proposals)
**Learner confirmed self-learning**: 4 cycles, proposer producing (the HTTP 400 was `keep_alive` sent as the string "-1"; now numeric). Cadence ~2–4 min.

| # | Proposal (abridged) | Verdict | Why |
|---|---|---|---|
| 1 | "r at C=1.15e-6 is exactly 4.696e-04; check by running serapis_emulator(C=1.15e-6)" | **REJECT** | Tautology — 4.696e-04 is already a result-bus record in its own memory; the "check" re-runs the same deterministic function. |
| 2 | "r = 4.696e-04 at C=1.15e-6, N*=50.24; verify emulator output equals it" | **REJECT** | Same tautology, restated. |

**Diagnosis (good news inside):** it is *grounded* — using real stored values, not hallucinating. The failure is that it restates what it can already see. Two causes, both fixed this pass:
1. The prompt didn't forbid restating known values → added hard anti-tautology rules: no restating DATA numbers, no deterministic re-run checks, must be a NEW input / relation / sensitivity / cross-check, and must state what would falsify it.
2. `ingest: 0` every cycle — its DERIVATION_LOG copy was stale, so it had almost nothing to reason from. Fed it D1272–D1276 (verified 5 sections present on the PC).

**Next pass:** check whether proposals become non-trivial now that it has real material + stricter rules. Watch `ingest` going >0.
- 2026-11-18T10:24Z — **cloud cycle 4: two corrections, both PASS.** (a) **D1265a**: PW5's n_s response was evaluated off-point (0.01171 = slope at C≈1.12e-6; at the benchmark it is 0.01352, and it varies ~40% across the band) → the CMB meter is **±12%** on Im S·Im ρ, not ±14% (PW5 still PASS, stronger). (b) **D1275a**: my own D1275 overstated the heavy-ν lever — M = x·M_s·e^{−2πn Im T} lives on a *different* (rigid) cycle, so it constrains Im S·Im ρ₁ only jointly with Im T_inst, x and V; useful only if the construction fixes those. Tool gap: `ladder.py update` skips `D###a` notes below its watermark (applied 0), so map histories miss corrections — fix later.
- 2026-11-18T10:21Z — **cloud cycle 5 (D1277, PASS) + grading pass 2.** Shapes vs scale: 2D hexagonal wins at every scale (no flip); 3D BCC↔FCC swap exactly at the self-dual scale α=1 (Poisson duality — a shape can only lose to its own dual). So D1276's ρ-sector preference is scale-robust. **Grading:** 3 more old-prompt cycles produced the same r-tautology; all 4 open proposals REJECTED via append-only supersede (cap cleared, 0 open) so the hardened prompt starts clean after the 4:20 restart.
- 2026-11-18T10:30Z — **D1278, PASS.** Shape flip by dimension: flips iff the winning lattice is not self-dual — d=2 hex (no), d=3 FCC/BCC (yes, α=1), d=4 D4 (no), d=5 D5/D5* (yes, α=1), d=8 E8 (no). Prediction logged before testing: E6/E7 flip, Leech does not. Open: run E6/E7 with an LLL-reduced basis or theta series.
- 2026-11-18T10:35Z — **D1279, PASS.** Backwards: every shape is a flat torus; a d=2 torus started anywhere slides to the hexagon (thin rectangle → square → rhombus → hexagon). Square τ=i is a SADDLE (−0.295/+1.118) held only by x→−x; hexagon τ=ρ an isotropic minimum. **New open check (high value): is τ=i a minimum or a saddle of the actual SERAPIS-E potential?** — our i-sector relies on the CP locus (x=0).

### AUDIT — 2026-11-18T10:40Z (Danny: "you check all this")
**Confirmed:** D1272 (benchmark reproduced to every digit by fresh exact runs); D1276–D1279 by independent methods — exact closed forms 4ζβ / 6ζL₋₃ (≤1e-9), Poisson identity to 1e-15, D4 brute force = theta formula, E8 formula = known shell counts (1e-12), saddle/min robust over 10 energy×step combos. r bound (BK18 < 0.036) confirmed.
**Corrected:** D1273a (n_s inputs unsourced — published range used; the 2σ is the *benchmark*, the frozen band reaches ~1σ), D1275b (the "independent consistency pass" was circular — moduli are fitted to n_s, so SERAPIS-E is a meter *by construction*), D1274a (void premise of verdict 1), D1265b (slope 0.0133 not 0.0135; ±12% unchanged). All PASS.
**System:** hot redeploy fired at 4:20 ✓. First hardened-prompt proposals are genuine, falsifiable, new-input — both FALSIFIED (T_R off ~3.6 decades vs D1270 scaling; exact n_s 0.97219 outside 0.9740–0.9750) → REJECT. **Ingest bug found + fixed:** my `## D#### —` headers didn't match CubeMind's `## D####:` parser, so none of tonight's work had reached its memory; converted to house format, 14/14 now parse on the PC. Integrity: 14/14 notes jl_check PASS, both repos clean + pushed, PC copies carry every fix.
