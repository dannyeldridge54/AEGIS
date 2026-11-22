# The Loom against 24 systems that improve themselves (Danny 18:57, 22 Nov 2026)
For each source: what it is, how it optimises itself, what the Loom took from it, and the result of the locked test. The D-notes are D1984–D1988.

## A. Research agents and AI scientists
| # | system | how it optimises itself | taken into the Loom | result |
|---|---|---|---|---|
| 1 | [AI Scientist-v2](https://arxiv.org/abs/2504.08066) (Sakana) | agentic tree search over experiments, with a manager that expands the best nodes | planner: innermost-first ordering, plus exploration as a tree branch | in the planner (D1980) |
| 2 | [AI co-scientist](https://arxiv.org/abs/2502.18864) (Google) | generate, debate, then an Elo tournament between hypotheses; evolve the winners | competing derivations are ranked, not picked by hand (rotation, D1982) | rotation locked; tournament queued for L4's candidate axes |
| 3 | [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) | self-modifies, keeps an **archive** of every variant, validates on benchmarks | method_archive.jsonl keeps every engine version, with a held-out score | O5 done |
| 4 | [AlphaEvolve](https://arxiv.org/abs/2506.13131) (DeepMind) | evolutionary code search driven by an automatic **evaluator** | the battery and the bars as the evaluator; held-out seed | O4: blind run on seed 2026 |
| 5 | [ADAS](https://arxiv.org/abs/2408.08435) (Automated Design of Agentic Systems) | a meta-agent designs agents, judged on held-out tasks | engine v1 → v2 → v3 judged by the same locked bars | v3 PASSes A1–A4 |
| 6 | [FunSearch](https://www.nature.com/articles/s41586-023-06924-6) (DeepMind) | LLM program search with a scorer and an islands population | populations of detector configs | O3 (shadows) |
| 7 | [Agent Laboratory](https://arxiv.org/abs/2501.04227) | staged pipeline, with human checkpoints | guards: Danny's OK for publishing and downloads | already in force |
| 8 | [Robin](https://arxiv.org/abs/2505.13400) (FutureHouse) | multi-agent loop: literature, hypothesis, experiment, analysis | node agents, the N0 lead, referees | in the charter |
| 9 | [Coscientist](https://pmc.ncbi.nlm.nih.gov/articles/PMC10733136) (CMU) | an LLM plans, then runs tools and instruments | toolkit registry, so actions call validated tools | toolkits.json (40 entries, all resolve) |
| 10 | [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | an orchestrator with parallel subagents; effort scaled to the task | effort tags, at most one high-effort action per pulse | O9 PASS |
| 11 | [Multiagent debate](https://arxiv.org/abs/2305.14325) (Du et al.) | several models debate to improve factuality | referees run on a different model from the main loop | O9 PASS; referee D1985 found 4 MAJORs |
| 12 | [Reflexion](https://arxiv.org/abs/2303.11366) | verbal memory of past failures, reused next time | mistakes.jsonl (12 dated mistakes) attached to each action | O8 PASS |
| 13 | [Voyager](https://arxiv.org/abs/2305.16291) | a growing skill library of verified code | the toolkit map, with an existence check | in place |

## B. Self-tuning optimisers
| # | system | how it optimises itself | taken | result |
|---|---|---|---|---|
| 14 | [Population Based Training](https://arxiv.org/abs/1711.09846) | exploit/explore on a population **during** training | live detector tuned during the run on self-injected probes, never on scored events | O3: 11 updates |
| 15 | [Hyperband](https://arxiv.org/abs/1603.06560) | bandit early-stopping of bad configs | worst shadow replaced each 5 s | O3 |
| 16 | [Self-driving labs / Bayesian optimisation](https://arxiv.org/pdf/2508.06642) | choose the next experiment by information gain | rotation T, S, T, U from Fisher weights (T is loosest) | locked, D1982 |

## C. Real-time detection and statistical control
| # | method | what it does | taken | result |
|---|---|---|---|---|
| 17 | [CUSUM](https://en.wikipedia.org/wiki/CUSUM) (Page 1954) | optimal sequential detector of a mean shift | detector B on whitened, self-normalised data margins | precision 1.0, latency ≤ 2.6 ms (D1987) |
| 18 | [Bayesian online changepoint detection](https://arxiv.org/abs/0710.3742) | run-length posterior | the alternative, kept in reserve | not needed |
| 19 | [Online FDR, LORD](https://arxiv.org/abs/1502.06197) | α-wealth for streams of tests | online_fdr.py over the Loom's claims across rounds | O6 PASS: FWER 0.0265 ≤ 0.05 |
| 20 | [Safe anytime-valid inference](https://arxiv.org/abs/2210.01948) (e-values) | tests valid at any stopping time | the basis for always-on referees; next, e-process detectors | queued |
| 21 | [Simulation-based calibration](https://arxiv.org/abs/1804.06788) | check an inference tool on data with a known truth | null-stream calibration before any scored run | D1986 FAIL (caught the flaw), D1987 PASS |

## D. Testing the tester
| # | method | what it does | taken | result |
|---|---|---|---|---|
| 22 | [Mutation analysis](https://mutationtesting.uni.lu/survey.pdf) (Jia & Harman) | break the code on purpose; good tests catch it; declare equivalent mutants | 18 mutants with an unmutated control | VOID → 0.72 FAIL → gaps closed → **0.88 PASS** |
| 23 | [Metamorphic testing](https://i.cs.hku.hk/~tse/Papers/2010s/hlmtCSUR.html) | relations that must hold under a transformation | rotating the knob axes leaves the lensing unchanged | B2 PASS |
| 24 | [Blind analysis](https://arxiv.org/abs/physics/0312102) (Klein & Roodman) | freeze the procedure before looking | locks, code committed before scored runs, held-out seed | in force |

## What the Loom now does that most of these do not
- **Locks before computing.** The tests are hashed and pushed first.
- **Labels honestly.** PRED, FIT, NULL, TRUST, BOUND and OPEN are kept apart, so fits cannot pose as predictions.
- **Has guards against gaming its own endpoint** (G-T1 to G-T6).

## What it still lacks
- Real data streaming in. The streams are synthetic Gaussians around the published numbers.
- A tournament between competing derivations.
- e-process detectors.
