# DEVIATIONS C6 (written before any rerun) — 2026-11-17
D1: Definition (ii) assumed Φ(∞) = 0. galpy's PowerSphericalPotentialwCutoff (the MWPotential2014 bulge) has a constant offset: Φ(r = 1e5 natural units) = +1.345 (checked; Miyamoto–Nagai and NFW → 0). So (ii) came out below (i), which is impossible.
Fix: (ii) := √(2[Φ(r = 1e5·ro) − Φ(r0)]). Definition (i) uses potential differences and is unaffected. Criteria unchanged.
