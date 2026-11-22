# PREREG D2025: The compressor as a circuit board. Bypass traces and a clocked bus. Locked before scoring.
**Idea (Danny 00:47).** "Compare it to like a circuit board … improve the wiring."

**The board as it stands (loomz17):**
- Each node is a component with its own local regulator: a LM mixer over its spins.
- The rings are buses. A bus is RM, a mixer keyed by the partial byte only.
- There are three parallel paths with different time constants: M1 (slow), M1b (fast) and M2 (context-keyed).
- A multiplexer (the MV shadow bank) picks the path with the lowest recent cost.
- Two APM trim stages act as feedback calibration.

**Circuit changes (loomz18; defaults = loomz17 exactly, 45,841 on d200k):**
- **SKIP = 2,8,20: bypass traces.** The strongest single components (the o2 node output, the word node, the match line) are wired straight to the final multiplexer bank, skipping the buses. New trace weights start at 0, an open switch the board learns to close. Comparable to paq8 / cmix final layers that see raw inputs.
- **RCTX = 1: a clocked bus.** Ring mixers choose their weight set by match state (none / short / long) × partial byte, instead of by partial byte alone. Comparable to paq8 mixer context sets.

**Test bed.** loomz18 at TB22, with the env of the best build (D2017 knobs). Note: the D2024 runs also use the TB22 build (loomz17 binary). Comparisons are within one binary.

**Slice.** enwik8 [31, 32) MB, never used. The d200k numbers above are a sanity check only; they are not scored.

**Arms:** BASE, SKIP, RCTX, SKIP+RCTX.

**Pass:**
- An arm must be smaller than BASE by at least 0.10% on the slice.
- Scale ladder: the best passing arm must also beat BASE by at least 0.05% on a 3 MB slice, [40, 43) MB, never used.
- Round-trip is required.
- Otherwise NULL.
