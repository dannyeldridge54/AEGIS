# PREREG A8c3 (track X, Hyperion -> Star Mapper; manual Djl 17 Nov 06:31 CT): faster accurate orbits (written before running)
Follows A8c2 (D1074: accuracy met for disk stars, r_peri 1.3e-3 for extreme stars; 15–26 ms/star). Profiling (development, before this lock): the force call is ~47 µs per step for 200 stars, of which the bulge's incomplete-gamma call is ~22 µs; the per-step turning-point parabola work and array copies are most of the rest (~184 µs per step in total).
Code: mapper_feed.orbit_params_batch3 (committed with this lock, never run before it): bulge M(r) from a 20,000-point table in ln r (linear interpolation), parabolas only where a turn occurs, no list shuffling, two-tier step η = 0.006 inside r < 1 kpc else 0.01 (cap 0.02).
Script theory/janus_astro/a8c3_check.py = a8c2_check.py with batch3 (same populations, seeds, reference, limits).
Pass (both populations): r_peri, r_apo, e ≤ 1e-3 relative; z_max ≤ 1e-3 relative or 1e-3 kpc; cost ≤ 10 ms/star → A8c3 VALIDATED.
Output field_tests/results/janus_astro_a8c3.txt. No reruns to chase; DEVIATIONS first.
