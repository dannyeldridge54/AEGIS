# PREREG PROM-9 TREE (23 Nov 2026 13:20 CT) — Prometheus cycle 7: the whole fusion tree in ONE layered run
Danny 13:06: "do layered testing in one run, research entire tree, set goal, get". Hints: tools/fusion/hints/cycle7.json.
## Change (one, mechanical, source-derived)
S3 gains convention='popcon' (cfspopcon 9.0.1, H1-H5): tau_E scaling evaluated at P_heat = P_alpha + P_aux (+ ohmic, here inside P_aux),
power balance W/tau = P_heat; W = 3/2 (<n_e><T_e> + (<n_i> + sum n_imp)<T_i>) V from volume averages. Used ONLY for the SPARC node (its source
convention). ITER keeps its FDR-calibrated convention; all other nodes unchanged.
## Layers and goalposts (all locked; earlier nodes keep their original locked tolerances)
L1 S1: sigma v DT 10/20 keV within 0.5% of Bosch-Hale (G1); Q(DT) 17.589 +- 0.002 MeV, n share 0.7997 +- 0.001 (G2).
L2 S2: n T tau_min 2.6-3.4e21 keV s m^-3 at 11-16 keV (G3); ideal ignition 4.0-4.8 keV (G4).
L3 S3-ITER: 500 MW column P_fus 350-650 MW, Q 6-15, tau_E 3.0-4.4 s (G5/G6); 400 MW held-out within 10% of 400 MW (PROM-1).
L4 S3-SPARC (NEW, the goal): popcon convention, Creely composition/profiles/heating, H98 1.0: P_fus within +-25% of 140 MW AND <T> within +-20% of 7.3 keV.
   can-fail: the same node in our ITER convention must differ by > 15% (it gave 120 MW / Lux and 80 MW / all-radiation before).
L5 S3-ARC: prescribed-profile P_fus within +-20% of 525 MW; implied H98 within +-15% of 1.8.
L6 S4: specific yield 3.37e11 J/g +- 0.5% and Phi(3) = 1/3 (G7); NIF 2021-08-08 pressure within 1 sigma of 569 +- 61 Gbar.
L7 S5: tritium burn within 1% of 56.08 kg/GW-fpy (derived; literature 55.8-56.1); TBR doubling (1 GW, 10 kg, 5 y) 1.04-1.06.
L8 S7: solar pp Gamow peak within 3% of 5.9 keV at 15.7 MK (G13).
L9 data: Fe-56 B/A 8.790 +- 0.01 MeV, He-4 7.074 +- 0.01; H-3 half-life 12.32 y +- 0.2%.
Tree verdict = all layers pass. Referee after; DEVIATIONS before any fix; one rerun.
