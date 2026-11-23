# PREREG SPEED-fusion (locked before build), 2026-11-23 12:30 CT
The goal-dial scan took 511 s (PROM-3): plasma() integrates 400 profile points in pure Python inside a 150-point root scan inside a
He-ash iteration. Build tools/fusion/fusion_fast.py: numpy-vectorised sigmav, profiles and plasma() (same formulas, same grid), a
coarse-to-fine root bracket (scan the power-balance residual on the same 150 T points, vectorised over T), and warm-started He iteration.
Tests: V1 plasma() fast vs reference: every output rel <= 1e-10 on 50 random (n, T, f_He) points; V2 operating_point: same roots and
outputs rel <= 1e-8 on ITER, ITER_400 and 10 dial points; V3 goal_dials: identical best point (same n, P_aux) and P_net rel <= 1e-8;
V4 speed: goal_dials >= 10x faster. Pass = all four; else failed-as-locked, DEVIATIONS first, one rerun. The fast path becomes the
default only after V1-V4 pass and after R86's fixes are applied.
