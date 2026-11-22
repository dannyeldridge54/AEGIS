# PREREG D2002: exhaustive gluing for the degree-4 case of a (3,10,40)-graph. Locked before code and runs.
**Claim to test.** Suppose a (3,10)-graph G on 40 vertices has a vertex v of degree 4. Then G − N[v] is a (3,9)-graph on 35 vertices. That graph is unique (Angeltveit, arXiv 2401.00392): H = circulant C₃₅(1,7,11,16), found and verified in D2000. H is 8-regular, so every vertex of G has degree ≤ 9 and each H-vertex gains at most one neighbour among N(v) = {w₁..w₄}. The attachment sets A_i = N(w_i) ∩ V(H) are therefore **disjoint independent sets of H** with 3 ≤ \|A_i\| ≤ 8 (since 4 ≤ deg w_i ≤ 9).

**G has α ≤ 9 exactly when** (with W independent and v adjacent to all of W):
| independent sets of H | must be hit by |
| --- | --- |
| every 8-set | at least 3 of the A_i |
| every 7-set | at least 2 |
| every 6-set | at least 1 |
(I_j counts H's independent j-sets: I₈ = 3360, I₇ = 13760, I₆ = 22995.) Triangle-freeness holds automatically: the A_i are independent and disjoint, and W is independent.

**Search.** Without loss of generality, by rotation 0 ∈ A₁. Then A₂ < A₃ < A₄ in candidate order. Pruning: every pair of A's jointly hits all 8-sets; every triple jointly hits all 7-sets; all four jointly hit all 6-sets. Exhaustive, split over 2 cores.

**Output.**
- Either every solution, each turned into a 40-vertex graph and checked by verify.py (K = 10). **A verified solution proves R(3,10) = 41.**
- Or none: then **no (3,10,40)-graph has a vertex of degree 4**. New in the case the literature leaves open (diameter 3; arXiv 2601.03572 excludes degree 4 only for diameter 2).

**Calibration of the code itself.** The same program, run on the analogous case for **R(3,9)**, must reproduce known facts. It is **K = 9, n = 35**, where a degree-4 vertex's dual neighbourhood would be a 30-vertex (3,8)-graph. That needs a list of (3,8,30) graphs, which we don't have, so instead a **unit test**: the constraint checker must accept a known valid 40-vertex construction if one is planted. So the planted-solution test is:
- take a random set of 4 disjoint A's;
- check that the checker's accept/reject decision matches verify.py on the glued 40-vertex graph, for 200 random instances, with **0 disagreements**.
