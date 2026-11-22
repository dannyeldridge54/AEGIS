# PREREG D1984: Loom optimisations from the literature (Danny 18:57), locked 22 Nov 2026 ~01:05Z, before building
Each item: the source idea, then what changes in the Loom, then its locked test.

**O1 CUSUM detector with hysteresis** (Page 1954; BOCPD, Adams & MacKay 2007, as the alternative).
- Per margin: z = (m − baseline)/sd, using D1983's self-move compensation. Two-sided CUSUM: S± = max(0, S± ± z − k), alarm when S > h, then S reset.
- **LOST hysteresis:** a RESONANT layer becomes LOST only after **3 consecutive** failing pulses, mirroring the 3-pulse lock rule (a Schmitt trigger).
- Test: on null streams, LOST flips **≤ 1 % of D1983's 9,857** for L7.

**O2 Calibration on null streams** (simulation-based calibration, Talts et al. 2018).
- Before the scored run: 5 training seeds × 5 s of pure noise (no events). Measure the false-alarm rate of every candidate (k, h).
- **A config is admissible only if its false-alarm rate is ≤ 1e-5 per layer-pulse** (100× under the A3 bar).

**O3 Online population-based tuning** (PBT, Jaderberg et al. 2017; early stopping as in Hyperband, Li et al. 2016).
- During the run, 4 shadow detector configs run on the same z streams, plus **self-injected probe shifts**: 2 sd for 200 pulses, every 2,000 pulses, on a seeded random layer.
- Fitness = mean probe detection delay (in pulses) + 1000 × the shadow's false alarms outside probes.
- Every 5 s, the live config takes the best admissible shadow (exploit), and the worst shadow becomes a perturbed copy of the best, with k × 0.8 or × 1.25 and h × 0.8 or × 1.25 (explore).
- **Fitness never sees the scored events.**
- The controller (D1983) keeps its rules and gains the owed trigger: a layer that fires on a non-predicted event window is escalated (readings 3 → 5).

**O4 Blind, held-out final run** (blind analysis, Klein & Roodman 2005; held-out evaluation as in the Darwin Gödel Machine / AlphaEvolve).
- The 60 s scored run uses **seed 2026**, never used in calibration or development. Its event schedule is identical to D1983. The scorer is fixed before the run.
- **Bars:**
  - A1 (max |Δ| < 1e-9);
  - A3 (≤ 1e-3; also reported against the stricter O2 bar of 1e-5);
  - A4;
  - recall = 1 within 0.5 s;
  - **precision ≥ 0.9 BOTH within 0.5 s of event start (new) AND over the full event window (D1983's definition, not loosened).**
- **PASS needs all of them.** D1983's FAIL stands regardless of this run.

**O5 Method archive** (Darwin Gödel Machine; ADAS, Hu et al. 2024).
- field_tests/loom/method_archive.jsonl records each method version: its config, its score on the training benchmark, its score on the held-out run, and its parent.
- The archive keeps **every** variant, not only the best.

**O6 Online FDR across rounds** (LORD++, Javanmard & Montanari 2015; Ramdas et al. 2017).
- tools/loom/online_fdr.py turns the sequence of the Loom's PASS-type claims into a test sequence with an α-wealth budget (α = 0.05).
- Test: in 2,000 simulated all-null sequences of length 100, the empirical FDR is ≤ 0.05 (that is, the FWER with all nulls).

**O7 Mutation runner fix** (Jia & Harman 2011 on mutation analysis; the control from D1982).
- The control copy must come out PASS. Then rerun B4 **once** with the same 18 mutants. Bar: kill rate ≥ 80 % and no VOID.

**O8 Mistake memory** (Reflexion, Shinn et al. 2023).
- field_tests/loom/mistakes.jsonl holds today's dated mistakes and how each was caught.
- planner.py puts the known failure modes relevant to each action into next_actions, so agents and referees see them.
- Test: the planner output for an L7 or L8 action lists the D1983a attribution mistake.

**O9 Heterogeneous referee and effort scaling** (multi-agent debate, Du et al. 2023; the Anthropic multi-agent research system).
- Referees run on a different model from the main loop (already so: sonnet).
- The planner tags each action's effort as low, med or high: derive = high, test = med, owed or check = low. At most 1 high per pulse.
- Test: a planner case.

Verdicts are reported per item. A failing item is FAIL, not retuned. One rerun per item only, with DEVIATIONS written first.
