# PREREG D2000: extend the R(3,10) generator into two new dimensions (Danny 20:40). Locked before code and runs.
**Calibration result (D1998):** solved every known rung up to N = 27 within seconds, with 0 false finds on the 3 impossible rungs. It stalled at N = 35 (K = 9, known to exist; best score 82) and at N = 40 (best score 78). **The limit is the search space, not K.**

## Dimension 1: symmetry (tools/ramsey/circ.c)
- Exhaustive search over **circulant** graphs C_n(S), with S a symmetric set of distances.
- Only **maximal** triangle-free S are tested. The independence number only falls as S grows, so a non-maximal solution implies a maximal one.
- α < K is tested on independent sets through vertex 0, which suffices by vertex-transitivity.
- **This is complete:** it either finds every circulant (3,K)-graph on n vertices or proves none exists.
- **Calibration:** n = R(3,K) − 1 for K = 4..8 (report whether circulant witnesses exist; the literature has many). The negative rungs n = R(3,K) must give none.
- **Targets:** n = 35 (K = 9), 39 (K = 10) and **40 (K = 10)**.

## Dimension 2: centre-outward growth (r310 in grow mode)
- Start from a verified (3,K)-graph at a smaller N, lock it, and add one vertex. Its neighbourhood is chosen as an independent set of size ≤ K − 1 that minimises the number of new independent K-sets. Then repair by annealing at the new size (pulses).
- Lock the size when the score reaches 0, then grow outward again: layer by layer, like the Loom.
- **Calibration:** grow K = 9 from N = 27 up to 35. Success = a verified (3,9)-graph at 35.
- **Target:** grow K = 10 from the best available graph up to 40.

## Rules
- Every claim passes tools/ramsey/verify.py, with 2 methods, before it is called a find.
- Everything is logged in the target table.
- A circulant non-existence result at n = 40 is reported as "no circulant witness". **It does not settle R(3,10).**
