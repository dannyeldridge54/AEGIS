# PREREG D2012: Negative-space (inward) nodes. Locked before scoring.
- **N1, closing stack:** the stack of unclosed openers (`[[` → `]]`, `{{` → `}}`, `(` → `)`, `<` → `>`). Context = hash(top expected closer, depth ≤ 7, last byte).
- **N2, gap:** the distance since the top opener, bucketed (log2), plus the top closer and the last byte.

**Engine.** loomz10 (v9 balancer, gains = 1, EV on, DIR_ONE class map) plus N1 and N2 as two new table nodes in ring 1.

**Slice.** F (enwik8 [80, 83) MB). It was used once (D2010), never for tuning.

**Runs:**
- base;
- +N1;
- +N2;
- +N1+N2.

**Pass.** +N1+N2 is ≥ 0.05% smaller than base, and round-trips. Each node's share is reported.
