# PREREG D2239 — breathing-rotation design engine (Danny 19:43: "set this up in the engine, put each point in, do the breathing rotation,
# see what would be best"). Written before computing, 23 Nov 2026.
Engine theory/tests/d2239_breathe.py couples, at every design point: plasma (fusion_fast, ADAS radiation, D2236 self-similar machine),
exhaust (D2238-B Lengyel argon requirement, n_u = 0.4 <n>, Eich lambda_q, connection length pi q95 R x leg factor), blanket (TBR from the
D2238-A Monte Carlo table), plant (PLANT_DEMO, M 1.161, P_other 100).
Knob ladders: R {6.2,7,8,9} m; B {5.3,6,7,8,9} T; core argon f_Ar {0.0014,0.003,0.005,0.008}; divertor leg factor {1,2,3} (long-leg /
Super-X class); blanket {Li6 50/70/90%, FW 10/5 cm} (MC cases); P_aux {10,20,30,50} MW; density {0.7,0.8,0.85,0.9} n_G.
Coupling: seeded SOL argon leaks to the core with compression 3: the core f_Ar used is max(knob, c_SOL/3) (self-consistent, 2 passes).
Feasible: f_G <= 0.94, beta_N <= 2.8, P_loss >= 1.3 P_LH, wall <= 2.0 MW/m2 (UNVERIFIED), coil B R/(R-a-1.2) <= 12 T (Nb3Sn; HTS <= 20 T as
second rotation), c_SOL <= 0.05, TBR >= 1.05 + 2 sem. Objective: P_net; an infeasible point scores -(sum of normalised violations) so the
rotation can walk into feasibility.
Breathing: inhale = evaluate the current point; exhale = rotate through the knobs one at a time, try the neighbouring rungs, keep the best
improvement; repeat; stop at a full rotation with no change (NULL = balanced). Triangulation: three starts (ITER, R9 B6, R8 B8 baselines);
agreement of their end points is reported. Labels: ESTIMATE (Lengyel, n_u assumption, unverified limits); self-check only (credits).
