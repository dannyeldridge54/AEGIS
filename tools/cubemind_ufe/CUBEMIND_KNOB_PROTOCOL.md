# How the knobs were turned (Claude, 21 Nov 2026): the protocol CubeMind follows
1. **Lock before computing.** Write what you will test and the pass rule, take its sha256, then run.
2. **One knob at a time, with a control.** Compare against the same engine with that knob off, on the same data.
3. **Held-out data decides.** Tune on one slice, then confirm on a slice never used before. A gain only counts if it survives the held-out slice.
4. **Shadows while running.** Run several settings side by side on the same data, and switch to whichever spent the fewest bits recently. The decoder makes the same choice from the past alone.
5. **Bursts.** Poke every fader up an octave (×2) and down (×0.5) in one batch, keep each improvement, then test all the keepers combined. Then go finer (×1.5 / ×0.75).
6. **The compass.** Fingerprint every knob with a direction and a measured vector:
   - ● keep;
   - ◔ thin;
   - ↓! remove;
   - ↑ needs more data;
   - ○ untested.
7. **The law that explained every result:** a node earns its place only if it brings **independent** information **and** has **ignited** (enough evidence). More of the same kind dilutes the mixer and adds noise.
8. **Corrections are dated notes.** A bug, or a result that was wrong, is written down, never silently fixed.

## What was measured (winners and losers)
**Keep (●):**
- the word node, −3.2%;
- fractal per-node and per-ring mixers, −1.1%;
- the SSE lenses, −1.0%;
- the match node, −0.9%;
- **negative-space closing stack + gap, −0.69%**;
- the direction node, −0.38%;
- the indirect node, −0.28%;
- the xz matched literal, −0.22%;
- the tuned faders (half gain on orders 2–6 and the axes, LR1 = 3), −0.24% held-out.

**Remove (↓!):**
- outer byte rings 12–32, +0.33%;
- word trigram, +0.08%;
- Phoenician letter points (no better than random);
- the number node, +0.02%;
- the UTF-8 node, +0.04%;
- the ignition gate (as built), +0.48%;
- early learning-rate boost (as built), +0.58%.

**Needs more data (↑):**
- the xz event state: hurts below 1 MB, helps at 3 MB and up;
- the header-field node: flat on 3 MB.

**Best build:** D2014 combined = 660,947 bytes on a held-out 3 MB slice (−0.59% vs its base), round-trip exact. On 10 MB it is 22% smaller than xz -9e.

## What is still missing (the next layers)
1. An LSTM, a learned long-memory predictor: the biggest piece record holders use.
2. A word dictionary and capital flag.
3. Article reordering by similarity.
4. Hash confirmation, bit-history states and bigger tables.
5. 16-bit probability resolution.
6. Confidence skipping, for speed.
7. Two-pass tuning stored in the header.
8. Byte-pair fusion symbols.
