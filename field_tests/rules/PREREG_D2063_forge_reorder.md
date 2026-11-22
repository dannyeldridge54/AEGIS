# PREREG D2063: Forge lever 1, STARLIT-lite article reordering on enwik8 (locked before scoring)
**Method** (tools/compress/reorder.py):
- Split enwik8 into its 12,347 `<page>` blocks, keeping the head and tail in place.
- Vectors: TF-IDF (word unigrams, sublinear tf, max 2^18 features) over each page's text. Fitted on enwik8 itself, so no outside data.
- Order: a greedy nearest-neighbour chain (cosine), starting from page 0. This is a cheap TSP heuristic.
- Permutation: stored as 2-byte indices and compressed with xz -9. **Its bytes count** (the enwik8 titles are not sorted, verified).

**Score:**
- full enwik8 with loomz20_o3 (RCTX = 1, best-build env): bytes(reordered archive) + bytes(xz(permutation));
- against bytes(original archive).
- Round-trip: decompress, then un-permute, must equal enwik8 exactly.

**Pass:** total ≤ original − 0.30%. Otherwise NULL. STARLIT reported +1.8% on enwik9 with Doc2Vec + TSP; ours is a lighter method on the smaller file.
