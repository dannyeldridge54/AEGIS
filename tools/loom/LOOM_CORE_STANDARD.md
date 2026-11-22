# The Loom Core Standard (v1, 22 Nov 2026): knobs within knobs, an agent at every point, a centre that balances
Danny 00:33–00:34: "every knob … 9 other knobs at each point … the agent that's controlling them … make it the standard, the core."

This standard applies to **every** engine: the UFE/Weave, the compressor, the R(3,10) search, CubeMind and GIMPS.
Each rule cites the test that earned it.

## 1. Structure: a fractal of agents
- **Knob tree.** Every knob K has up to **9 sub-knobs**, each owned by a **local agent** with its own goalpost. Agents nest: an agent's output is one knob of the agent above.
  - **Never more than ~9 knobs on one controller.** Raw spins on one mixer cost +1.2%; given a local mixer per node they stopped hurting (D2006). The fractal mixers were worth −1.1% (v4).
- **The centre** balances the agents below it. It moves effort (compute, tuning steps) toward the agents that are currently improving: a bandit over their recent gains. That is the live balancer of D2011.
- **Three tandem axes** (the S/T/U of the UFE). Imbalances are traced to an interface between axes, not hidden inside one (UFE v4 §7).

## 2. What a node must bring: the admission rule
- A node or knob earns its place only if it brings **independent** information **and** it has **ignited** (enough evidence).
  - Proved by every keep and drop: word, match, directions, negative space and indirect were kept; outer rings, trigram, number and UTF were dropped (D2006–D2014).
  - More of the same kind dilutes the controller.
- **Look in the negative space.** Ask what is *owed* or *absent*, not only what was seen. The closing stack was worth −0.69%, the largest new node (D2012).
- **Coarse beats fine when evidence is thin.** Vowel/consonant and directions beat 20 fine letter classes (D2007/D2008).
- **Memory and hygiene matter.** Big tables plus hash confirmation gave −1.75% (D2016/D2017). An agent reading another agent's slot is silent poison.

## 3. How agents tune (the instrument)
- **Octave then fifth.** Poke ×2 / ×0.5, keep what helps, then refine at ×1.5 / ×0.75 (tune.py, burst.py).
- **Shadows.** Run several settings side by side on the same data and switch to the one with the lowest recent cost. The decision uses only the past, so it can be replayed (D2011).
- **Bursts.** Poke all knobs in one parallel batch, keep the winners, then test them combined, since winners can reinforce each other (D2012a: combined −0.69%).
- **Ladder to null.** Optimise in stages until one stage gains under ~5% or sits inside the noise, then stop (D2020: 20 s → 0.21 s).

## 4. Integrity (the referee in the centre)
- **Lock before computing:** PREREG + sha256, pushed first. Code is committed before scored runs. DEVIATIONS are written before any rerun. Never rerun to chase a result.
- **Held-out decides.** Every knob layer is confirmed on data it never tuned on. More knobs mean more ways to fool yourself (all of D2010–D2017 used fresh slices).
- **Positive and negative controls first.** Reproduce known answers before searching: Z35/Z40 (D2018/D2019), planted (3,4,8)/(3,5,12)/(3,7,22), and M = 9 U1 solutions verified (D2020).
- **Independent methods.** Two or three methods must agree before a claim (D2003: gluing + SAT + numba).
- **Triangulate.** Three sources or vectors; use the median; consensus within 1σ / 0.3 dex.
- **Labels and corrections.** PASS / FIT / NULL / NO-POWER. Bugs and voided numbers get dated notes, never silent edits (v7 comment bug; the bracket "bug" is kept as a feature, D2014).

## 5. Bookkeeping
- **Compass:** every knob has a direction, a vector and headroom (COMPRESSION_COMPASS.md, WEAVE_COMPASS.md).
- **Registry:** every tool is filed by problem and version; scored builds are never overwritten (TOOL_REGISTRY.md).
- **Live readout:** each scale's cost is printed while running (loomz7c COMPASS lines).
- **Stall rule:** 7 nulls without balance is a STALL, not success; switch to exploring.

## 6. Hardware
- Use every part of the machine: all cores minus one, RAM for tables, GPU only where its arithmetic fits.
- Detect at start-up and size to fit (cm_ramsey.py, cm_compress.py).
- Long jobs are chunked and resumable (run_u1.py).

## 7. Reference implementation
`tools/loom/loomcore.py`: `Agent` (≤ 9 knobs, octave/fifth tuning, held-out gate) and `Centre` (a bandit over agents, nesting, a ledger of every poke). Any engine plugs in by giving each agent an `evaluate(settings, split)` function.

## 8. v1.1 additions (22 Nov 2026, FILTRATION_REVIEW.md)
- **One target per agent.** A global log-likelihood over its datasets minus a fitted-knob penalty (BIC-style). A knob must buy more likelihood than it costs.
- **Referees at every gate:**
  - lock referee;
  - compute referee (C1–C7);
  - centre referee (balance + trials + tension);
  - an independent final referee.
- **Blinding.** Build with the data value hidden or offset; unblind once.
- **Automatic trials ledger.** Every scan logs its trials; significances are corrected.
- **Injection-recovery.** Plant a known signal; the whole chain must recover it.
- **Tension metrics** before combining datasets.
- **Scale ladder.** A result must hold on its last two scale rungs (size, loop order, n).

## 9. Stop rules
- **NAILED:** target met on held-out or post-lock data, all gates passed.
- **STALL:** 7 nulls; explore.
- **FIT:** met only by adding fitted knobs; recorded, never claimed.
