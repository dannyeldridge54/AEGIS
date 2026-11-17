# PREREG A8c4 (track X, Hyperion -> Star Mapper; manual Djl 17 Nov 06:38 CT): exact turning-point reference (written before running)
Question (from D1075): is the extreme population's r_peri difference (1.3e-3) an error of the fast method or of the sampled reference (A8a orbit_params, 20,001 samples)?
Code: mapper_feed.orbit_params_exact_events (committed with this lock, never run before it): DOP853 rtol 1e-12 with events at every d(r²)/dt = 0 and v_z = 0, extremes from the event states (no sampling). Fast method: fast.orbits_fast (A6c, = batch3).
Tests (A8c3 populations, seeds 2026 and 11, 200 stars each, 3 Gyr):
E1 diagnosis (reported AND scored as the answer): for the extreme population, the fraction of stars whose orbits_fast r_peri is closer to the event reference than the sampled reference is; "reference sampling" is confirmed if this fraction ≥ 0.9 among stars where the two references differ by > 1e-4.
E2 accuracy: orbits_fast vs the event reference — r_peri, r_apo, e relative ≤ 1e-3; z_max relative ≤ 1e-3 or absolute ≤ 1e-3 kpc — for both populations.
Pass E2 → the fast Mapper orbits are VALIDATED against an exact reference (A8c4 VALIDATED); E1 settles the D1075 question either way.
Output field_tests/results/janus_astro_a8c4.txt via theory/janus_astro/a8c4_check.py. No reruns to chase; DEVIATIONS first.
