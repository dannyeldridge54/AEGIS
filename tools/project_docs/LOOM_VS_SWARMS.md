# The Loom vs other agent swarms (21 Nov 2026, 18:25 CT; Danny 18:19)
**What was compared:**
- Anthropic's multi-agent research system (orchestrator plus parallel subagents; engineering write-up).
- Google's AI co-scientist (generate → debate → evolve, with tournament Elo ranking).
- The multi-agent-debate literature (heterogeneity matters, 2502.08788).
- Classical swarm data mining (particle swarms and ant colonies: exploration vs exploitation).

## The Loom as a toolkit
`python3 tools/loom/loomd.py pulse --rounds N [--method]` runs N consecutive pulses of the deterministic core:
1. the checks' self-test (VOID if it fails);
2. the still point;
3. the resonance map, centre outwards;
4. the method tests (optional);
5. the compass and review;
6. the centre brief;
7. the null-round test.

It then writes an **agent work order**: N0 always, the node agents only where the inputs changed, and the referee every second round. It stops after 7 null pulses in a row. `loomd.py status` shows the latest round. The rounds are stored in field_tests/loom/rounds/.

## What ours does well, and most swarms do not
1. **Pre-registration and hashed locks before any fetch or compute.** No swarm surveyed does this. It removes "results chosen after the fact".
2. **Independent heterogeneous referees on a schedule,** plus a **centre referee (N0) that leads**. Co-scientist has a reflection agent, but it critiques hypotheses, not the pipeline's own bookkeeping.
3. **Automatic checks with a self-test** (C1–C7: independence, power, validation, numerology, overclaim lint, four corners, formula benchmarks). These were validated on real mistakes.
4. **Method tests of the balancer itself** (injection–recovery, a null false-balance rate, dof and hold-outs). Most swarms evaluate output quality, not whether the method can tell signal from noise.
5. **Anti-gaming guards** (relabelling is not progress; fits cannot grow; killable predictions cannot shrink). This is a defence against goal hacking.
6. **Knock-on ledger and compass vectors:** every action records what it disturbed, and every datum carries a direction, not just a pass or fail.

## What others do really well, and we do less of
| practice | who | what they do | our gap |
|---|---|---|---|
| **Broad-then-narrow search** | Anthropic | Short broad queries first, then narrow; 3–5 subagents in parallel, each running 3+ tools in parallel | Our searches are narrow from the start, and one at a time |
| **Explicit effort scaling** | Anthropic | Simple fact: 1 agent, 3–10 calls. Comparison: 2–4 agents. Complex: 10+ | We have no rule; cost varies by hand |
| **Dedicated citation agent** | Anthropic | After research, a separate agent attaches every claim to its source | Our quote checks are manual. D1945 found an unverified paraphrase |
| **Source-quality filter** | Anthropic (a failure they fixed) | Prefer primary and authoritative sources over content farms | Implicit, not written down |
| **LLM-judge rubric plus a small eval set early** | Anthropic | About 20 representative queries; a 0–1 rubric (accuracy, citations, completeness, source quality, efficiency) | Our referees give prose verdicts, not a scored rubric, so there is no trend line |
| **External memory and fresh contexts** | Anthropic | The plan is saved outside the context; subagents write to files and pass references | Partly: D-notes and briefs. Node reports come back as large inline text |
| **Tournament ranking of candidates** | Co-scientist | Pairwise debates, Elo ratings, and evolution of the best hypotheses | We test one candidate at a time (split stacks, flavon, …). Competing explanations are not ranked against each other |
| **Generate → critique → evolve** | Co-scientist | Evolution agents recombine and improve top hypotheses | We have no evolution step; failed candidates are only withdrawn |
| **Real-world validation** | Co-scientist (wet lab) | Predictions checked by external experiments | Our equivalent is scoring locked predictions on new data (JUNO, LHC). Too few are scored yet |
| **Exploration vs exploitation** | particle and ant swarms | Part of the swarm keeps exploring far from the current best | Our still-point lens is pure exploitation, plus mining the loose directions |
| **Heterogeneity** | debate literature | Debate helps only when the agents differ (model, prompt, data) | Our referees run on one other model (Sonnet); the node agents are all the same model |

## Improvements, ranked (cost first, then value)
1. **A citation and quote-verify agent** at the end of each round. It checks every quoted sentence and number against the fetched source text, a string match. Cheap, and it would have caught D1945.
2. **A scored referee rubric** (0–1 on correctness, power, labels, guards, citations) plus pass/fail, stored per round. That gives a trend line for the method's own quality.
3. **Broad-then-narrow data mining with an effort rule.** Per data item: 1 broad search, then at most 2 narrow ones; 3 parallel fetchers for a contested number. Fewer calls for simple facts.
4. **A tournament for competing explanations.** For each open problem, make 3–5 candidates compete (for α_s: split stacks vs a non-universal threshold vs extra states vs single-stack-with-thresholds). Each is scored by the method tests (dof, hold-outs, false balance) and ranked; the best is evolved. This replaces one-at-a-time testing.
5. **An exploration share.** About 1 node agent in 5 explores away from the still point (for example the S at i branch, other folds, U₃ ≠ i), so the swarm does not over-commit to one basin.
6. **Heterogeneity.** Run the node agents on two different models or prompts and treat disagreement as a flag. Keep the referees on a different model from the author.
7. **External-memory handoff.** Node agents write their JSON to field_tests/loom/rounds/ and return only a path, which cuts tokens.
8. **A small eval set for the Loom itself.** About 20 past situations with known right answers (today's mistakes plus resolved cases). Re-run it whenever the method changes. This extends C7.

Sources:
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Google Research — Accelerating scientific breakthroughs with an AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- [AI co-scientist paper, arXiv:2502.18864](https://arxiv.org/pdf/2502.18864)
- [Multi-agent debate needs heterogeneity, arXiv:2502.08788](https://arxiv.org/abs/2502.08788)
