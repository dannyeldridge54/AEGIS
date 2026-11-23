# PREREG HARDEN-1 (23 Nov 2026 15:05 CT) — tighten the ladder's weak tests (audits R98/R99): exact neutron balance + error bars
mc.run gains bookkeeping counters (no physics change): births (source + secondaries), leaks, absorptions (no neutron out), cutoffs (E < 1e-5 eV)
and multiplication (sum over collisions of n_out - 1 when n_out >= 1).
Goalposts (locked):
B1 exact balance on the workshop sphere, 2000 histories: source + sum(n_out - 1 over scattering/multiplying collisions) = leaks + absorptions + cutoffs,
   to 0 (integer identity) - catches any lost or double-counted particle.
B2 the same identity holds with the (Pb, MT16) yield-1 override (can-fail path exercised).
B3 TBR from the collision estimator agrees with an analog count of tritium-producing reactions (Li-6 MT105 + Li-7 tritium channels sampled) within
   3 combined standard errors (estimator cross-check; two independent tallies).
Referee after; DEVIATIONS before any fix; one rerun.
