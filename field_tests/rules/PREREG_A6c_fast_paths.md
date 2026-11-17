# PREREG A6c (track X, Hyperion; Danny 17 Nov 06:34 CT "continue speeding all paths"): compiled fast paths, regression-tested (written before running)
Code: tools/janus_astro/fast.py as committed with this lock (numba 0.68.1; never run before it): orbits_fast (same algorithm as mapper_feed.orbit_params_batch3, compiled, parallel over stars), jfactor_fast (same geometry as jfactor.J_route_B; line of sight on fixed Gauss–Legendre panels, 64 nodes × 11 panels, vectorised).
Regression tests (fast path vs the validated Python routine, same inputs):
R1 orbits_fast vs orbit_params_batch3 on A8c3's two populations (seeds 2026 and 11, 200 stars each, 3 Gyr): r_peri, r_apo, z_max, e relative ≤ 1e-9 (identical algorithm; floating-point order only).
R2 jfactor_fast vs J_route_B for the five A7a profiles (r_⊙ 8.5 kpc, ρ_⊙ 0.39): relative ≤ 1e-6.
Pass R1–R2 → A6c VALIDATED. Speed (first call excluded = compile time, reported separately) reported, not scored: ms per star for orbits (single and 2 threads) and seconds per J.
Output field_tests/results/janus_astro_a6c.txt via theory/janus_astro/a6c_check.py. No reruns to chase; DEVIATIONS first.
