# CubeMind engineering notes (E-series) — CubeMind engineering agent, from 21 Nov 2026
Engineering only (tools, tool use, grading). Physics D-notes stay in D72_D75_weak_spots.md (main session). Labels: every number is a tool output, a recorded D-note value, or a measurement.

## E1 (cycle 1, 17:15 UTC) — U21 adoption in cloud kit + engine
- REVIEW: kit self-test OK and engine 16/16 at ab0c2991. The kit carried the old defaults (α⁻¹ 24.3, T_R 2.61e8, x 0.32, 𝒱 1e5/m₃/₂ 5e5, gluino 7 TeV, α_D 4.7e-4, b₀ 23/3). The engine carried only labels (T_R 1.34e9 in L4).
- POSTULATE: the U21 values can be adopted as tool DEFAULTS without moving any published reference number, if each old reference assertion is re-pinned with its old input passed explicitly. Refuted if any self-test or engine test needs a looser tolerance.
- ENGINEER: DEVIATIONS D1–D9 first (commit d25bf25f), then kit defaults, new weave_point (adopted point, labelled per entry), weave_basic q='axion_f', weave_nuclear b0 (D9, referee D1807 #8); engine labels + run()['point'] read from the kit (one copy).
- TEST: kit self-test OK; engine 16/16. Before → after (defaults): T_R(magd7) 4.30e8 → 3.73e8; W₀ 2.70e-8 → 1.05e-8; wino passing [0.66, 1.0] → [0.66]; α_s(unif, rg2) 0.11584 → 0.11474 (D1808 0.1147 ✓); σ/m 9.33e-7 → 1.86e-3 cm²/g; α_s precision needed 4.25e-4 → 4.99e-4; Λ_QCD shift at δα_s = 0.0033: 0.194 → 0.165. r(rinv) unchanged 5.724e-4 (T_R cancels, D1766, as expected).
- REFEREE: no tolerance loosened; four old assertions re-pinned with explicit old inputs (D4, D5, D9). Units checked (GeV, cm²/g). Overclaim check: weave_point labels N, χ, 𝒱, W₀ as selections; α_D conditional; τ_p recorded, not computed. One self-inflicted bug (comments swallowing code on 4 lines) caught by the self-test before commit.


## E2 — Design note: CubeMind data retrieval as a Loom of independent links (Danny 14:32, 21 Nov 2026)
- **One sub-agent per link.** Each link is an independent sub-agent with a simplified job (one source, one method, one code path), works in its own context, and does not see the other links' answers.
- **Bearings.** Each link returns a bearing: value ± uncertainty, framework tag, provenance.
- **Consensus step.** It triangulates the fix (median and spread), marks it consensus (≥ 2 of 3 overlapping) or open, and records which way outliers point and why.
- **What feeds derivations.** Only consensus fixes feed CubeMind's derivations. Open fixes become TRUST inputs or findings.
- **Referee.** A fresh-context referee link audits each consensus.
- **Mirror of the Loom.** This mirrors THE_LOOM.md §3 (triangulated data points) and §7.
- **Plan.** Lock the bearing schema and consensus rule before building. The test harness replays the Loom's D1906 (Cassini) and D1908 (displacement) fixes. Not started; to be scheduled as a CubeMind engineering item.
