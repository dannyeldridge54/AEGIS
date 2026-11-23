# PREREG D2175 — "each node a prime, string the fractal parts": recursive prime-node wheel walked in ascending k (TOOL benchmark)
Locked 2026-11-23 ~01:12 CT before running. Danny 01:10. Follows D2174 diagnosis (early exit lost).
Build: each node is a prime r (8, 3, 5, 7, 11, then 13, 17, 19, 23 as a second ring); a node keeps the residues of k for which q = 2kp+1 is allowed mod r. Nesting the nodes (CRT) gives a self-similar tree; its leaves, read in order, are one period of a GAP STRING (the "string of fractal parts"). Walking k upward by that repeating gap string touches only surviving k, in ascending order, so the first factor found is the smallest (early exit kept).
Rings tested: R1 = {8,3,5,7,11} (period 4620·?, per p), R2 = R1 + {13,17,19,23}.
Same benchmark as D2174 (200 prime p in [1e6, 1e6+2e4), TF to 2^40).
 C1 correctness: identical smallest factor (or none) to the naive loop on all 200; any mismatch = FAIL.
 C2 speed: R1 faster than naive by ≥ 2.5× (fraction of k kept 0.208, so the ceiling is ~4.8×); report R2 too.
 C3 report the fraction of k touched and the gap-string length per ring.
