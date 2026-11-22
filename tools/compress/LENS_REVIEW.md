# The compressor seen through every lens: what each idea predicted, what the data said, what survives (21 Nov 2026, 22:15 CT)
Rule, as with the UFE: every lens is a hypothesis. It is kept only if a measured test with a control supports it, and each answer opens the next question.

## The one law underneath everything
**Compressed size = the total surprise of the data under the model + the size of the model.** Every lens below is one way of lowering surprise without paying more in model. Once that is clear, every result in tonight's tests has the same shape:
- **New kinds of information lower surprise.** Words, matches, directions and the matched literal all add something the field did not already know.
- **More of the same kind adds noise.** Outer rings, finer letter splits and raw spins repeat what the field already knows. They dilute the mixer (it has to share weight among echoes) and cost time.

## Lens by lens
| Lens (whose idea) | What it predicted | Measured | Verdict | What survives |
|---|---|---|---|---|
| **Field / UFE**: nodes, rings, a centre (Danny) | layered predictors converging on one prediction | each scale beats the one before it (2.9 → 2.3 → 2.0 → 1.75 → 1.65 → 1.61 bpc) | ✅ | the architecture itself |
| **Two-way flip switch**: every pulse has a returning wave (Danny) | nodes that record both outcomes and lean toward the recent one | the core of the engine; the match and word nodes are built on it | ✅ | the nonstationary two-way counter (the same idea as PAQ's) |
| **Spins**, counter-rotating rings (Danny) | several adaptation speeds help | +1.2% raw (worse), ≈ 0 once each node mixes its own spins | ◔ | spins need a *local* mixer: the fractal structure, not the spin itself |
| **Fractal**: a mixer at every level (Danny) | per-node and per-ring mixers stop the dilution | −1.1% | ✅ | **the most important structural fix** |
| **Outward rings at multiples** (Danny) | longer contexts at 12, 16, 24, 32 | +0.17% / +0.33% (worse), +33% time | ❌ | long repeats are already the match node's job |
| **Lenses at each layer** (Danny) | refining stages sharpen the prediction | the SSE lenses give −1.0% | ✅ | two lenses; the balancer picks the blend |
| **Alphabet on its ancestral points** (Danny) | the Phoenician lineage carries structure | ties or loses to random partitions (locked NULL) | ❌ | — |
| **Symbols as directions** (Danny) | open, close, separate, end, toggle, reset | **−0.38%** (locked PASS) | ✅ | **the best new node of the night** |
| **Coarse vs fine classes** | — | vowel/consonant −0.21% beats 20 fine classes | ✅ | fewer, broader points beat many fine ones |
| **xz's circuit** (literature) | reps, matched literal, 12-state machine | −0.25%; the state machine needs data (hurts at 200 kB, −0.30% at 3 MB) | ✅ | matched literal and the event state |
| **Radio / soundboard / instrument tuning** (Danny) | turn each knob until the signal is clearest | the live balancer gives −0.06%; it switched once and then held | ◔ | the board was already near balance. The big gains are in **what** is fed in, not in the fader levels. Fader burst running. |
| **Max force at the start** (Danny) | high learning rate early, decaying | (test interrupted) | ○ | standard in Gated Linear Networks; owed a test |
| **Stellar ignition (Lawson n·T·τ)** (Danny) | a node only helps once count × sharpness × memory crosses a threshold | — | ○ | **explains the dilution results**: un-ignited nodes are noise. Test: an ignition gate |
| **Nucleosynthesis**: fuse symbols up to an "iron peak" (Danny) | merge frequent pairs while it saves bits, then stop | — | ○ | byte-pair fusion as a data-found alphabet. Test owed |
| **Three bodies compressing a centre** (Danny) | three rings alone balancing at the centre | — | ○ | the "three rings only" setting: test owed |
| **Encryption / target acquisition** (Danny) | surprise as a detector | — | ○ | compression distance can reorder the articles (the STARLIT and fx2-cmix trick), done with our own engine |
| **Rodin digit filters** (Danny, Mersenne) | the digital root picks out primes | NULL | ❌ | — |

## The postulate that ties them together
A node earns its place when it brings **independent** information **and** has **ignited** (enough evidence). The fractal mixers then decide, at every level, how much each ignited node is worth *in this context*.
- That one sentence explains every keep and every drop above.
- It also predicts where the next gains are:
  1. **New independent sources**: an LSTM (a learned, long-memory view of the text), and the article-level context: topic, section, which kind of page.
  2. **Better ignition**: hash confirmation (so a node is not reading someone else's slot) and bit-history states (a richer memory per slot).
  3. **Better symbols**: the fusion dictionary, the capital flag, and word codes sorted so neighbours share structure.
  4. **Better ordering**: articles grouped by similarity, so the field stays warm on a topic.

## Standing numbers
- **Best build (v9):** 2,128,359 on G (10 MB) vs xz 2,731,076 (−22%).
- **Full enwik8 (v1):** 20,923,436 (1.674 bpc), round-trip exact.
- **Record target:** ≈ 0.80 bpc on enwik9. The gap is ~2×. It closes through items 1–4, not through fader levels.
