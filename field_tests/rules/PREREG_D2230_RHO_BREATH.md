# PREREG D2230 — breath 2 of the filtered scan: steer the lattice complex structure rho (Danny 17:53 steering knobs). Written before computing.
Same scan as D2229 + DEV-1 (wrappings |w| <= 6; F1 tree split; F2 massless hypercharge; all step-3a filters), with rho as the steered knob.
For each rho in {1/4, 1/3, 2/3, 1, 3/2, 2} (rho = 1/2 done in D2229): regenerate the SUSY bulk list with z6p_checks3's own condition
((P-Q)/(2 rho) = U+V, volume (P+Q) - (2/3) rho (V-U) > 0, tadpole bounds 0 <= P+Q <= 8, |U-V| <= 24, wrappings |w| <= 6), then run.
F1 uses the same rho in the volume. Report per rho: n bulk cycles, F1 bulk pairs, (a,b) pairs with 3 chiral doublets, F1 survivors,
F1+F2 survivors. Cap 15 min per rho (PARTIAL if hit). No filter changes after counts are seen.
Reading fixed now: a rho with F1+F2 survivors -> candidate lattice for the N=2 Delta b derivation (next lock); none at any rho -> the
tree-unified 3-generation brane route is closed on T6/Z6' ABa for these rho (and the forces ring needs another geometry or a non-brane
mechanism). Caveat stated now: a given rho must also be a stabilised value of the T3 complex structure; that is not checked here.
