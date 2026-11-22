# PREREG D1986: the woven field. Goalposts at every node, scored live by each node's referee every pulse (Danny 19:01), with engine v2.
Locked 22 Nov 2026 (the lock time = this commit's time). The code is committed before the scored run (D1983h).

## Goalposts
tools/loom/goalposts.json: 61 goalposts on the 9 nodes. Its sha256 is in this lock's .sha256.
- 25 PRED, 14 NULL, 13 OPEN, 5 FIT, 2 BOUND, 2 TRUST.
- 16 big open problems with clear goalposts, among them baryogenesis, dark matter, Λ, H₀, S₈, Li-7, strong CP, hierarchy, unification, evolving dark energy and the neutron lifetime.
- 11 live: scored from the engine each pulse.

**Scoring per goalpost:**
| data type | rule |
|---|---|
| band | pull = (weave − value)/σ. PASS if \|pull\| ≤ 2, TENSION if 2 < \|pull\| ≤ 3, FAIL if > 3 |
| upper / lower limit | PASS or FAIL against the limit |
| window | PASS inside, FAIL outside |
| internal | the layer's own margin |
| no Weave value, or no data | OPEN, or UNSCORED |

**The label is kept alongside the score.** A FIT that passes is "PASS (FIT)", a NULL that passes is "PASS (null)", and a TRUST is "TRUST". **Only a PRED that PASSes counts as a prediction surviving a test that could have killed it.**

**A node is DONE when:**
- it is RESONANT for at least 3 s; and
- every scored goalpost of the node is PASS; and
- no OPEN goalpost remains; and
- no FIT is spent on its knobs.

## Engine v2 (tools/loom/loom_rt2.py), fixing referee D1985
- **Bounded knobs.** \|Δln\| ≤ ln 3 for u, M_N, m₃/₂ and T_R, with T_R < m_φ as well; split ∈ [−ln 3, ln 3].
- **Split is visible.** Its Jacobian column is a forward finite step of 0.05 (the a_s_eff switch at split ≠ 0 is a FIT, and it is counted).
- **O1: CUSUM detector** per margin on z = (m − baseline)/sd, with self-move compensation as in D1983.
- **LOST hysteresis:** a layer goes LOST only after 3 consecutive failing pulses. LOST can re-lock after 3 passing pulses, so it is not sticky.
- **O3: online population-based tuning.** 4 shadow configs (k, h) run on self-injected 2-sd probes. Every 5 s the live detector copies the best admissible shadow and the worst shadow is replaced by a perturbed copy. Fitness never sees the scored events.
- **O2: null calibration first.** 5 training seeds × 5 s with no events. The admissible starting (k, h) are those with a false-alarm rate ≤ 1e-5 per layer-pulse.
  - Grid: k ∈ {0.5, 1.0, 1.5} × h ∈ {8, 12, 16, 24}.
  - The start config is the admissible one with the lowest mean probe delay.
- **The controller** keeps D1983's rules, plus a new trigger: a layer that alarms during a non-predicted event window escalates (readings 3 → 5).

## The scored run (O4: blind, held out)
- 60 s, **seed 2026**, which is never used in calibration or development.
- The events are the same as in D1983. E2's predicted set comes from the lens at 24 s, now **with split visible**.
- **Quiet windows:** (2, 10), (20.5, 25), (35.5, 45), (55.5, 60) s. Each excludes 0.5 s after an edge. **Every alarm time is logged.**

**Bars:**
| bar | requirement |
|---|---|
| A1 | max \|Δ\| < 1e-9 (copy check) |
| A2 recall | 1 within 0.5 s |
| A2 precision | ≥ 0.9 both within 0.5 s **and** over the full window |
| A3 | ≤ 1e-3, reported against 1e-5 too |
| A4 | recovery, only for layers RESONANT just before the event; at least 1 such check |
| A5 | **no knob hits its bound for more than 10 % of the pulses**. A bound-hugging balancer is a runaway, and it is reported |

**PASS needs A1–A5.** The goalpost scoreboard is reported per node (PASS / TENSION / FAIL / OPEN / UNSCORED, by kind), along with the number of nodes DONE.

## Honest priors (written now)
- Most goalposts are static numbers from the D-notes. Only 11 move with the knobs. The scoreboard therefore mostly restates the battery, and the live part is what is new.
- The data are synthetic Gaussian streams around the quoted values. **Real-time detection is self-consistency on synthetic data, not real data arriving.**
- Expected: L1, L2 and L6 resonate; L4 stays OPAQUE; L5, L7 and L8 fight over m₃/₂ and T_R, now bounded; and **no node is DONE**. Every node has OPEN goalposts or a FIT, and L9 has only OPEN.
