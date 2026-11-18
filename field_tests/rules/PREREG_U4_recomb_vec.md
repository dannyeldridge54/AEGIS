# PREREG U4 — upgrade loop, counterpart: Hyperion / Janus-LT recombination (tools/janus_lt/recomb.py)
Locked before building. Profile (this tick): one Recomb + z_star + z_drag ≈ 7.0 s; one BAO+CMB χ² ≈ 8 ms ⇒ Recomb is the bottleneck (L4/L5/L7 grids: 25 × 7 s).
Cause: scalar Python loops — xe_of(z) / nH / Hs evaluated one node at a time on the same 20001-node trapezoid grids inside every brentq step, and sB.sol(z) per node.
Change (same mathematics, same nodes, same quadrature): evaluate those grids as arrays (interp1d and dense-output sol on arrays; Hs via a vectorised E(z) with the same f_nu spline). No physics or node change.
Tests on 5 (ω_b, ω_bc) points incl. the L5 grid corners: T1 |Δz*|, |Δz_d| ≤ 1e-6 vs the current code; T2 speed ≥ ×5 per Recomb+z*+z_d; T3 one L5-type χ² (BAO + compressed CMB) unchanged to 1e-8.
Adopt only on T1–T3 PASS (zgrid cache key changes automatically; old caches rebuild). Results: field_tests/results/u4_recomb_vec.txt.
