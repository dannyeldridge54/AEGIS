# PREREG N12 CLOSE THE LOOP (23 Nov 2026 14:35 CT) — neutron ladder: computed blanket numbers back into the plant and fuel cycle
Inputs (LIVE, from the ladder): blanket energy multiplication M = 1.161 (N9, D2207a; Pb-Li workshop sphere, local photon deposition);
TBR = 1.021 +- 0.004 (N8 rerun; idealised full-coverage 1-D sphere, 100 cm Pb-Li 50% Li-6). Replaces S0's M = 1.2387 (PROCESS DEMO A INPUT).
Method: goal_dials_fast on ITER with PLANT_DEMO except M (same P_aux set, Greenwald/beta/L-H limits); S5 tbr_required (1 GW, 10 kg) for hold
(t_d -> infinity proxy: 1.010 as D2196) and doubling in 5 y (1.051).
Goalposts (locked):
C1 consistency: at the reference operating point, P_net with M 1.161 is lower than with 1.2387 by 0.368 * (1.2387-1.161) * P_n * (1 + f_pump)
   within 1% (pure plant algebra; checks the plumbing).
C2 fuel: the computed TBR exceeds the hold requirement (1.010) by more than 2 sigma, and falls short of the 5-year doubling requirement (1.051)
   by more than 2 sigma (pre-registered prediction).
C3 report (no band): best net electric power of an ITER-sized machine with the computed M (pre-estimate from plant algebra: about +5 MW
   vs +19 MW with PROCESS M), and the blanket coverage below which the computed TBR no longer holds the inventory (TBR x coverage = 1.010).
Referee after; DEVIATIONS before any fix; one rerun.
