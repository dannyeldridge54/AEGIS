# PREREG D2236 — at the helm: raise the plant's net power output, steering design knobs with the referee (Danny 18:35). Before computing.
Baseline: the N12 plant = DEMO-style balance (PLANT_DEMO: eta_th 0.368, eta_wp 0.4, pumping 14/2058, 100 MW other) with the COMPUTED blanket
M = 1.161, on the ITER machine (R 6.2 m, a 2.0 m, B 5.3 T, Ip 15 MA), dials optimised by goal_dials_fast -> P_net +4.9 MW (D2207/N12).
Helm knobs (machine design, self-similar at fixed aspect ratio 3.1, kappa 1.85, q95 held = ITER's): major radius R in {6.2, 7, 8, 9} m;
on-axis field B in {5.3, 6, 7, 8, 9} T. Ip scales as B*R (fixed q95, fixed shape); V as R^3, S as R^2; pedestal and separatrix densities scale
with the Greenwald density; temperatures, impurities, H98 = 1 unchanged. Dials per machine (as goal_dials_fast): P_aux in {30, 40, 50, 60, 73, 100}
MW, density 0.6-1.0 n_G (21 steps).
Hard limits (all must hold; values fixed now, sources stated - referee to check): f_G <= 0.94 (ITER design), beta_N <= 2.8, P_loss >= 1.3 P_LH
(existing engine rules); average neutron wall load P_n/S <= 2.0 MW/m^2 (first-wall engineering ceiling class, EU DEMO studies; from the
record/memory, flagged); divertor P_sep/R <= 17 MW/m with P_sep = P_loss - P_rad_core (EU DEMO criterion, Wenninger et al. 2015; from memory,
flagged); magnet: peak field on coil ~ B R/(R - a - 1.2 m) <= 12 T (Nb3Sn class) reported, and <= 20 T (HTS class) as the second variant.
Report: P_net, P_fus, Q, Q_e, binding limit for every machine; the best machine per magnet class; the ITER-machine optimum unchanged (control =
+4.9 MW). No limit is relaxed after results. Blanket M and TBR stay the computed 1.161 / 1.021 (TBR hold condition re-checked at each P_fus).
Referee after; DEVIATIONS before any fix; one rerun.
