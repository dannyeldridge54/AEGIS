# PREREG D2014: The fold-in battery (loomz13). Locked before scoring.
**New nodes (16–19), each switchable by MASK:**
- **HDR:** the XML field axis. Which header field we are in, plus the same field's byte on the previous page, at the same position.
- **IND:** indirect. What followed these 2 or 3 bytes last time.
- **NUM:** numbers. Digit-run length and the previous number's length.
- **UTF:** the UTF-8 continuation state.

**New knobs:**
- **FIXPREV:** bracket pairs use the true previous byte. v11–v12 compared the current byte with itself, so any single `[` counted as `[[`. That is recorded here as a correction.
- **GAINS / LR1 = 3:** the D2012a fader settings.
- **IGN = 4:** the ignition gate, which scales a node's inputs by (seen + 1)/5 until it has seen 4 events.
- **BOOST = 2:** max force early, a ×3 learning rate decaying with an 8 Mbit half-life.

**Slice.** J = enwik8 [90, 93) MB, never used before.

**Runs:**
1. base (new nodes off);
2. +HDR;
3. +IND;
4. +NUM;
5. +UTF;
6. +all 4;
7. all 4 + FIXPREV;
8. all 4 + faders;
9. all 4 + IGN;
10. all 4 + BOOST.

Then one combined run of every element that helped individually.

**Rules.**
- An element is kept if it is ≥ 0.03% smaller than its comparison run (2–5 vs 1; 7–10 vs 6).
- The combined run must round-trip.
