# PREREG D2251 — Long reactor redesign: the exhaust / core-radiation squeeze (locked 2026-11-23)

Pre-run audit (before this lock): (1) synchrotron uses the Albajar fit with the Fidone reflection term exactly as in the UKAEA
PROCESS documentation (coefficients and exponents checked); (2) bremsstrahlung C_B = 5.35e-37 W m^3 keV^-1/2 (NRL); (3) argon
from OPEN-ADAS. Budget at the D2244 near-design (R7 B9, Ar 0.8%): bremsstrahlung 265, synchrotron 114, argon line 261 MW
(core 99% of heating). Same machine at Ar 0.14%: 4.5 GW fusion, core 48%, but ~500 MW crosses the edge (P_sep/R ~ 71).

Question: is there any negative-triangularity (NT) design with net electricity > 0 that meets every locked limit, including a
core radiated fraction within what experiments have shown?

Engine: D2244 engine unchanged (D2243 deviations; NT: no L-H limit; IPB98 x H98 = 1.0; density 0.9 n_G for detachment;
5 impurity iterations; Lengyel divertor; ADAS argon; Albajar synchrotron). Wider ladders:
R [5, 6, 7, 8, 9] m; B [4, 4.5, 5, 6, 7, 8, 9] T; core Ar floor [0.0005, 0.001, 0.0014, 0.002, 0.003, 0.005];
leg [1..5]; P_aux [10, 20, 30, 50] MW; n_u/<n> [0.4, 0.5, 0.6]; enrichment eta [3, 5, 10]; blanket 90% Li-6 / 10 cm.
Physics variant: wall reflectivity f_reflect 0.6 (primary, PROCESS/ITER-class) and 0.8 (metal-wall variant), two passes.
Sampling: 6000 grid points per pass, uniform without replacement, seed 2251 (grid 113,400 points). Then polish: coordinate
descent (one ladder step at a time) from the 15 least-violating burning samples per pass, score = P_net if feasible else
-(sum of normalised violations); stop when a full sweep changes nothing.

Limits (all locked): f_G 0.94 (density fixed 0.9), beta_N <= 2.8, wall <= 2 MW/m2, coil <= 20 T (HTS; Nb3Sn 12 T reported),
SOL argon <= 5%, core argon consistent (c/eta), TBR margin, P_sep >= 1 MW, P_sep/R <= 17 MW/m, P_net > 0, and
core radiated fraction f_rad = P_rad,core/(P_alpha + P_aux) <= 0.60 (primary; NT DIII-D 0.45-0.55) with <= 0.67 reported
(EU-DEMO reference: P_sep 150 of ~450 MW heating).
Verdicts (fixed now): OPEN (feasible at eta 3, f_rad <= 0.60, f_reflect 0.6); CONDITIONAL (feasible only with eta >= 5,
f_rad <= 0.67 or f_reflect 0.8 - each condition named); CLOSED. Always report the most-ready design (fewest / smallest
violations) with its full plant numbers and the size of each remaining gap.
Control: D2244 near-design (R7 B9 Ar 0.8% P_aux 50) must reproduce P_net ~559 MW and f_rad ~0.99.
Labels: ESTIMATE; NT confinement assumed (H98 1.0, extrapolated); pedestal profiles retained (known optimism, R112 N3).
Referee: independent review; fixes only via _DEVIATIONS.md before one rerun.
