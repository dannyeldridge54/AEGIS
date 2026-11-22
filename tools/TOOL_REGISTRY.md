# Tool registry: every UFE/Loom-derived tool, named and filed by the problem it solves (22 Nov 2026)
**Rule (Danny 23:46):** keep a clean build.
- Whenever a tool is changed for a purpose, it gets a **new name or version**.
- It is filed under the **problem** it serves, with a row here recording what changed and the D-note.
- A scored build is never overwritten. Dev versions are labelled dev; void versions are labelled void.

**Naming:** `tools/<problem>/<tool><version>.<ext>`.
- Knob settings that define a "build" are written in the row (an env line), so any result can be reproduced.

## Names (Danny 00:55, 22 Nov)
- **The Unified Field Bloom (UFB):** the UFE derivation toolkit. It lives in tools/bloom (bloom.py, bloom_data.json, BLOOM.md) and tools/loom (core standard, loomcore, derivation_agents).
- **The Forge:** the compressor, tools/compress (loomz v1–v19). It is **paused**.

## 0. Core field engines (the Loom: the UFE as a self-balancing field)
| tool | what it is | status | notes |
|---|---|---|---|
| tools/loom/loom_rt2, rt4.py | earlier field engines | superseded | kept for replay |
| **tools/loom/loom_rt5.py** | exact fast engine (bitwise = v4); virtual clock; detector C; persistence confirmation | **current** | D1995–D1997 |
| tools/loom/parallel.py | 2-seed triangulation runner | current | D1995 |
| tools/loom/loomd.py | self-driving auto mode (STALL detection) | current | D1989 |
| tools/loom/calib10x.py | calibration with 10× pulses | PASS | D1997 |
| tools/targets/track.py | target-acquisition table (OpenML-style tasks, flows, runs) | current | — |
| tools/weave_cm/weave_tools.py | UFE chain calculators (wino, T_R, …) | current | D1801 etc. |

## 1. Problem: R(3,10) (Ramsey)
| tool | purpose | status | D-note |
|---|---|---|---|
| tools/ramsey/r310.c | annealing pulse search | stalls at hard rungs | D1998 |
| tools/ramsey/r310g.c | grow outward from a seed graph | untested | — |
| tools/ramsey/circ.c | exhaustive circulant search | PASS (Z35 found; none at 39/40) | D2000 |
| tools/ramsey/hcount.c | count H's independent sets | current | D2002 |
| tools/ramsey/glue4.c | exhaustive degree-4 gluing | PASS (0 solutions) | D2002/D2003 |
| tools/ramsey/sat_deg4.py | independent SAT check of degree 4 | PASS (UNSAT at K = 10) | D2003 |
| tools/ramsey/verify.py | 2-method witness verifier | current | — |
| tools/ramsey/cm/cm_ramsey.py | hardware-adaptive gluing (numba/GPU), the third method | PASS | D2003 |
| **tools/ramsey/cayley/groups40.py + cay.c** | Cayley search over all 28 Z5⋊P instances of order 40 | running | D2018 |
| tools/ramsey/R310_LOOM_PATH.md | 20 references, triangulation, two-front path | current | — |

## 2. Problem: the Hutter Prize (compression)
Base env for builds from D2008 onward: `CLASSMAP=DIR_ONE.map LR2=1`. EV = event state.

| build | what changed | result | status |
|---|---|---|---|
| loomz.c (v1) | two-way nodes, gated mixers, 2 SSE lenses | enwik8 **20,923,436** (1.674 bpc) | scored, D2006 |
| loomz2.c | spins + axes | −0.36% (dev) | dev |
| loomz3.c | masked rings really skip work | ablation tool | dev |
| loomz4.c | **fractal mixers** (per-node, per-ring) | −1.1% (dev) | dev |
| loomz5.c | early-boost learning rate | (interrupted) | dev |
| loomz6.c | class node (alphabet maps) | D2007 NULL (ancestry); D2008 directions PASS | scored |
| loomz7.c | xz circuit: reps, matched literal, event state | −0.25% dev; −0.86% with directions on H | scored, D2008a/b. *First v7 numbers void (comment bug)* |
| loomz7c.c | live compass readout | instrument | — |
| loomz8.c | outer rings 12/16/24/32 + trigram | **hurts** (+0.17/+0.33%) | rejected, D2010 |
| loomz9.c | live balancer (8 shadow mixers, 4 lens blends) | −0.06% | D2011 |
| loomz10.c | per-node gain knobs | tuning tool | D2012a |
| loomz11.c | **negative-space** nodes (closing stack, gap) | **−0.69%** | PASS, D2012 |
| loomz12.c | record/2D ring | images −7%, text +0.14% | universal build only, D2013 |
| loomz13.c | header, indirect, number and UTF nodes; knobs | combined (indirect + faders) **−0.59%** | PASS, D2014. Env: `MASK=1245183 LR1=3 GAINS=1,1,0.5×6,1,0.5,1,0.5,0.5,0.5 EV=1` |
| loomz14.c | 16-bit coder; TB 22/23/24 | −0.035%; TB24 **−1.14%** total | PASS, D2016 |
| **loomz15.c** | hash confirmation + backup slot (CONFIRM = 2 default) | **−0.62% → best: −1.75% vs v13** | **current best**, D2017. Env as v13 plus TB24 |
| loomz16.c | dictionary codes counted as word parts | untested | dev |
| prep.py / prep2.py | entity transform / capital flag + dictionary | capflag −0.12%; dictionary +1.9% on v15 | dev |
| classmaps.py, tune.py, burst.py | maps, the fader poke loop, the 2-minute burst battery | tools | — |
| COMPRESSION_COMPASS.md, LENS_REVIEW.md | knob fingerprints, lens review | current | — |

## 3. Problem: GIMPS / Mersenne primes
| tool | purpose | status |
|---|---|---|
| tools/mersenne/mloom.py | layered sieve (N1 to N4) + LL referee | locked D2005; calibration stopped, DEVIATIONS written |
| tools/mersenne/GIMPS_STRUCTURE.md | PRPLL/mfaktc structure; RTX 4070 hardware map | current |
| theory/tests/d1999_mersenne.py, d2004_rodin.py | pattern tests | NULL (both) |

## 4. Problem: the UFE derivation (Weave physics)
| tool | purpose | status |
|---|---|---|
| theory/tests/u20_chain.py | the derived chain (x, T_R, W₀ …) | D1801 |
| theory/tests/d2009_tr_channels.py | extra inflaton decay channels | D2009: not derived |
| tools/project_docs/WEAVE_UNIFIED_EQUATION.md, WEAVE_COMPASS.md | UFE v4 + compass | current |

## 5. CubeMind (the PC learner)
| tool | purpose | status |
|---|---|---|
| tools/cubemind_ufe/astro.py, ufe_lens.py | UFE-lens tracks (astro, compress, ufe, place) | installed, selftest 0 failures (D2015) |
| tools/cubemind_ufe/autorun.py, mission.py | LEARN → MISSION (M1 Hutter knobs, M2 R(3,10), M3 postulates) | installed; awaits Danny's model names |
| tools/cubemind_ufe/cm_compress.py | verified archiver (picks the build by free RAM; archives tagged by build) | installed (D2017 builds) |
| tools/ramsey/u1/check38.c | verifies the r38_27 list | PASS (477,142) | D2020 |
| tools/ramsey/u1/u1glue.c → u1fast.c → u1clq.c → **u1final.c (v4b)** | U1: (3,9,34)-graphs with a degree-6 vertex (ladder v1 to v5) | v4b current; PC launcher run_u1.py | D2020 |
| tools/ramsey/blockcirc/bc.c | D2019 block circulants (B, m) | 2×20 none; 5×8 running | D2019 |
| tools/ramsey/evolve/{initial_program.py, evaluator.py, config.yaml} | OpenEvolve swarm for front L (local Ollama, 5 islands, exact α evaluator) | smoke-tested | D2021 |

## Core (applies to every problem)
| tool | purpose | status |
|---|---|---|
| **tools/loom/LOOM_CORE_STANDARD.md** | THE standard: knob tree with ≤ 9 knobs per agent, a balancing centre, admission rule, instrument tuning, integrity, bookkeeping, hardware | v1, 22 Nov 2026 |
| **tools/loom/loomcore.py** | reference implementation: Agent (≤ 9 knobs, octave → fifth, held-out gate, nesting) + Centre (bandit; stops at BALANCED) | selftest PASS (balanced in 8 rounds, error 0.00) |
