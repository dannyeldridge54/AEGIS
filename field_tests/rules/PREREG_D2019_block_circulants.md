# PREREG D2019: Exhaustive block-circulant search for a (3,10,40)-graph. Continuous run until every case is done. Locked before code and runs.
**Graphs.** Z_m acts with B orbits (B·m = 40), for (B, m) = (2, 20), (4, 10), (5, 8) and (8, 5). This covers every graph with a fixed-point-free automorphism of order m whose orbits are the blocks.

**Edge orbits:**
- within block b: a distance d ∈ 1..⌊m/2⌋;
- between blocks b < b′: an offset t ∈ Z_m.

**Search.**
- Choose a set of orbits that is triangle-free, with every vertex degree ≤ 9 and ≥ 5 (D2003), and maximal under those caps.
- Then compute α by exact branch-and-bound.
- Symmetry: translating block b by s shifts every offset touching b. The run uses one such normalisation (block 1's first cross offset to block 0 is 0), which is sound.

**Calibration.**
- (B, m) = (1, 35) must find the (3,9,35)-graph at K = 9.
- (1, 40) must find none, reproducing D2000.

**Output.** Any witness is verified by verify.py plus an independent α. That would prove R(3,10) = 41. Otherwise: "no block-circulant (3,10,40)-graph for (B, m) = …". Novelty is not claimed.

**Run mode (Danny 23:53).** One continuous run; no timer ticks. It moves stage to stage and stops only when every stage is complete, or at a witness.
