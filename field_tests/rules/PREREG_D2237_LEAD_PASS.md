# PREREG D2237 — one-pass project-lead triangulation (Danny 19:38: lock all steps, one smooth pass, triangulate, then the paper). Before computing.
Machines (fixed now): ITER control (old-rule optimum), Nb3Sn R9 B6 and R8 B8 (D2236 reportable points, ADAS radiation, P_other 100).
For each, recompute the operating point at its stored density/P_aux and report, with three independent exhaust metrics (triangulation):
 E1 P_sep/R <= 17 MW/m; E2 P_sep*B/(q95*A*R) <= 9.2 MW T/m (EU-DEMO class, memory, UNVERIFIED); E3 Eich lambda_q = 0.63 B_pol^-1.19 mm,
 q_peak = (2/3) P_sep / (2 pi R lambda_q f_x), f_x = 5 -> seeded radiation fraction needed for q_peak <= 10 MW/m2 (order of magnitude).
 Wall: average load P_n/S; first-wall life = 20 dpa / (7.11 dpa/fpy per MW/m2 x load) (20 dpa EUROFER starter class, memory).
 Fuel: burn kg/y; TBR 1.021 (1-D computed) vs design margin 1.05 -> margin flag. Plant: P_net, Q_e.
Reading: a machine is "lead-ready at 0-D" only if E1-E3 agree (all pass or seeding <= 0.9) AND life >= 2 fpy AND TBR margin met. Self-check only
(credits); results labelled ESTIMATE where a formula is from memory. One run.
