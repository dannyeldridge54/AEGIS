# DEVIATIONS for D2039 (written before any rerun; goalposts, cost and model unchanged)
**Run 1 result:** STALL at a local minimum. The first ×0.1 / ×10 octave drove m₃/₂ to its lower bound while the leak term dominated, and the greedy single-knob pokes never left that basin.

**This is an engine finding, not a physics result.** Single-start greedy tuning gets trapped when one goalpost dominates the cost.

**Run 2 (allowed changes only):**
- (a) **Multi-start:** the Centre is restarted from v4 and from 3 seeds that differ in their starting sq and boost (sq ∈ {1, 0.1, 0.01}, boost ∈ {1, 1e2, 1e4}), with m₃/₂ and Δ₃ started at their v4 values. The lowest-cost end wins.
- (b) **Hands-on pass:** Danny asked for hands on the knobs. I set sq and boost by hand to the edges of G2/G3, then bisect Δ₃ to |z| = 0. That pass is reported separately and labelled HAND.
