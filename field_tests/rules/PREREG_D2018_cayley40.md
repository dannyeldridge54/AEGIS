# PREREG D2018: Exhaustive Cayley-graph search for a (3,10,40)-graph over all groups of order 40. Locked before code and runs.
**Groups.** Every group of order 40 is Z5 ⋊_φ P with |P| = 8, because the Sylow-5 subgroup is normal (n₅ | 8 and n₅ ≡ 1 mod 5, so n₅ = 1).
- P ∈ {Z8, Z4×Z2, Z2³, D4, Q8}.
- φ ranges over all homomorphisms P → Aut(Z5) ≅ Z4.
- Isomorphic copies are allowed: they cost time, not correctness.

**Search.** Connection sets S ⊆ G∖{e} with the following properties:
- inverse-closed;
- triangle-free: no a, b ∈ S with ab ∈ S;
- 5 ≤ |S| ≤ 9 (δ ≥ 5 from D2003; triangle-free gives Δ ≤ α ≤ 9);
- **maximal** among triangle-free inverse-closed sets. This loses nothing: adding an element only lowers α. The size cap means maximal is taken among sets of size ≤ 9; a set at size 9 is kept even if it could be extended.

For each S, compute α(Cay(G, S)) by an exact branch-and-bound.

**Calibration (must pass first).**
- The same code on Z35 must find the unique (3,9,35)-graph: α = 8 at K = 9, i.e. a circulant witness, as in D2000.
- On Z40 it must reproduce D2000 (no witness).

**Output.** Either a witness, which must then be verified by verify.py **and** an independent α check (that would prove R(3,10) = 41), or the statement "no Cayley graph on any group of order 40 is a (3,10)-graph". Novelty is not claimed until it is checked against the literature.
