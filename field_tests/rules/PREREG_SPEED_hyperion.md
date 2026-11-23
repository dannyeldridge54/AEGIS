# PREREG SPEED-Hyperion (rotation rung 4), locked 2026-11-23 ~09:45 CT before code
Profile (pytest --durations): slowest are jfactor for all profiles (9.5 s; route A, one adaptive quad per (l, b) node, 14,400
quads), and galpy-backed tests (import/MWPotential2014 setup ~1 s, McMillan17 orbit 6.5 s; external code, not ours).
H1 fast route A: the line-of-sight integral los(psi) is sampled once on 96 Chebyshev nodes in log(psi) over [b_mask, psi_max]
   (psi never goes below b_mask in the masked region) and evaluated by barycentric interpolation at all grid nodes.
   Must match the reference J_route_A to 1e-6 relative for NFW, Einasto, Burkert and a cored Einasto (rc = 1 kpc), HESS_IGS
   region, and be at least 10x faster (median of 3).
The reference J_route_A stays; settings.jfactor gains fast=True only if H1 passes.
Field map: Galactic dynamics, dark-matter indirect detection, stars/BBN/neutron stars -> releases/field_maps/astrophysics.md.
