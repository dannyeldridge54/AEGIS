# PREREG A8c (track X, Hyperion -> Star Mapper; manual Djl 17 Nov 06:25 CT): fast batch orbits (written before running)
Code (committed with this lock, never run before it): galaxy.force_array (vectorised MWPotential2014 forces, same formulas as MW.force); mapper_feed.orbit_params_batch (kick–drift–kick leapfrog for N stars at once, dt = 0.01 natural units ≈ 0.36 Myr, default window 3 Gyr).
Reference: mapper_feed.orbit_params (A8a: DOP853 rtol 1e-12, validated vs galpy to 5e-10) on the SAME 3-Gyr window with 20001 samples.
Stars: 200 synthetic (A8a/A8b generator, seed 2026).
Tests:
C1 force_array vs MW.force at 1000 random (R, z) in [0.05, 4] × [−1, 1] natural units: relative ≤ 1e-12.
C2 batch vs exact per-star: r_peri, r_apo, e — relative ≤ 1e-3; z_max — relative ≤ 1e-3 OR absolute ≤ 1e-3 kpc (near-planar orbits), for all 200 stars.
C3 cost: report ms per star for the batch (target ≤ 10 ms, reported; scored only as "faster than A8a's 517 ms").
Pass C1–C3 → A8c VALIDATED.
Output field_tests/results/janus_astro_a8c.txt via theory/janus_astro/a8c_check.py. No reruns to chase; DEVIATIONS first.
