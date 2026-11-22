# PREREG D2006: Loom compressor, two-way nodes (pulse out = prediction, wave back = update). Locked before code and runs.
**Danny's idea (21 Nov 2026).** Every pulse that goes out has a wave coming back. Each node is a flip switch that records both ways.

**Mapping to compression (stated now).**
- A bit-level predictor sends out a prediction (the pulse). The real bit comes back (the wave). Every node updates on both outcomes.
- Each node stores two counts, n0 and n1. On bit y it increments n_y; if n_{1−y} > 2 it halves n_{1−y} (+1). That is the "flip": the switch leans toward the recent side but keeps both records.
- Nodes are the contexts of the last 0, 1, 2, 3, 4 and 6 bytes, plus a word context (hashed).
- A logistic mixer combines all nodes, and its weights also learn from the returning wave.
- A binary arithmetic coder turns the predictions into bits.

The decoder runs exactly the same pulse/wave sequence, so the result must round-trip losslessly. There is no look-ahead: the decoder only has the past.

**Test corpus (fixed now).** enwik8/enwik9 are unreachable from the cloud and the PC sandbox (mattmahoney.net and huggingface are blocked). So:
- **C1:** the concatenation of theory/pending_docs/*.md in sorted order, at HEAD of this commit. About 3.0 MB of English markdown.
- **C2:** enwik8, once Danny supplies it (the same test, rerun with no changes).

**Baselines on the same file:** gzip -9, bzip2 -9, xz -9e.

**Pass/fail:**
- (1) Exact round-trip (sha256 equal). Otherwise the engine is FAIL.
- (2) Reported, not pass/fail: bits per byte and size vs each baseline; compress and decompress seconds on 1 core; peak RAM.

**Hutter projection (honest scaling, reported).** The Hutter record is S = 100,424,672 bytes on enwik9 (fx2-cmix-T, 24 Jul 2026). A 1% claim needs ≤ 99,420,425 bytes within ~50 h, 1 core, < 10 GB RAM, no GPU.
- Time to enwik9 = measured seconds/MB × 1000.
- Size is projected only from C2 (enwik8); C1 is not Wikipedia and is not used for size projection.
- The known ratio enwik9/enwik8 for strong CM compressors is roughly 8.3–8.6×. This is literature, used only as a label.
