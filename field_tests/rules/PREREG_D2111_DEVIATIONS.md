# D2111 DEVIATIONS (written before the rerun). The filters and verdict are unchanged.

**Why:** the first run had to be stopped after 2 of the 18 visible wrappings per shard. Each wrapping with finds produced 373,248 raw models (216 visible triples × 1,728 hidden completions). The process grew to about 0.5 GB per wrapping, which would run out of memory long before 18 wrappings. No results from that run are used. The only partial numbers seen were the progress lines quoted here.

**Fix (memory and counting only):**
1. Do not expand every raw model into a dict. Per visible triple, store the raw hidden-completion count, plus up to 20 sample completions.
2. Add a degeneracy-honest count. Labels (Z₂ eigenvalues, τ, σ) that give the **same cycle** (X, Y, exceptional vector) are the same brane. So report models that are distinct by cycle data: visible a, b, c cycles plus the multiset of hidden (N, cycle).
3. Compute vis_hidden_abs and the self-image χ for each distinct-by-cycle model, capped at the first 5,000 per shard.
4. The Table 27 control check is unchanged.
