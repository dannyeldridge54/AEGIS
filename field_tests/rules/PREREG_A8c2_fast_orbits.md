# PREREG A8c2 (track X, Hyperion -> Star Mapper; manual Djl 17 Nov 06:27 CT): accurate fast orbits (written before running)
Follows A8c (D1073: 2.9 ms/star but r_peri off 2.5%). Code: mapper_feed.orbit_params_batch2 (committed with this lock, never run before it): per-star adaptive kick–drift–kick, dt_i = η r_i/|v_i| (η = 0.01, cap 0.02 natural units), stars independent so each takes its own step; r and |z| turning points refined by a parabola through the last three samples.
Reference: mapper_feed.orbit_params (A8a exact DOP853, 20001 samples) on the same 3-Gyr window.
Populations: (P1) the extreme synthetic set (A8a generator, seed 2026, 200 stars); (P2) a realistic disk set (seed 11, 200 stars): Galactocentric positions within 3 kpc of the Sun in the plane, |z| ≤ 0.5 kpc, velocities = Sun-like rotation (v_φ ≈ 220–232 km/s) plus Gaussian (σ_R, σ_φ, σ_z) = (35, 25, 20) km/s.
Pass (each population): r_peri, r_apo, e relative ≤ 1e-3 for every star; z_max relative ≤ 1e-3 or absolute ≤ 1e-3 kpc; cost ≤ 10 ms/star → A8c2 VALIDATED (both populations required).
Output field_tests/results/janus_astro_a8c2.txt via theory/janus_astro/a8c2_check.py. No reruns to chase; DEVIATIONS first.
