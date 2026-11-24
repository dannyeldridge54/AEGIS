# PREREG D2243 — Steady helm pass: global search + literature H-mode rule (locked 2026-11-23)

Why: D2241 left two open items: (1) the coordinate-descent optimiser cannot leave no-burn regions, so the "closed"
verdict may be an optimiser artefact; (2) the best point (R 9, B 9, eta 10) fails only H-mode access (L-H).
Deep dive (Siccinio et al., EU-DEMO): reference operates at f_LH = P_sep/P_LH = 1.2 (Martin 2008 scaling); EU-DEMO
divertor limit P_sep*B/(q95*A*R) <= ~9 MW T/m. Our engine judges L-H on P_loss = P_alpha + P_aux - P_rad
(= power crossing the separatrix in this 0-D model) with margin 1.3.

Engine: d2241_enrichment.py physics unchanged. Blanket fixed at 90% Li-6 / 10 cm (TBR 1.095, not SUSPECT).
Coil limit applied post hoc (12 T Nb3Sn, 20 T HTS) from the returned coil field.
Search: 5000 points drawn uniformly (seed 2243) from the ladders R[6.2,7,8,9] B[5.3,6,7,8,9]
fAr[0.0014,0.003,0.005,0.008] leg[1..5] Paux[10,20,30,50] dens[0.7,0.8,0.85,0.9] nu[0.4,0.5,0.6] eta[3,5,10].
Each point returns all limit ratios; feasibility is judged post hoc under four rule sets:
  R13: locked D2241 limits (L-H margin 1.3, P_sep/R <= 17)       <- primary, continuity
  R12: same with L-H margin 1.2 (EU-DEMO literature)            <- literature variant
  R13E/R12E: each plus P_sep*B/(q95*A*R) <= 9.2 with q95 = 3.0 (as D2237)
Control: the D2241 eta10 R8B8 endpoint re-evaluated must give P_net 1004.5 MW and violations [LH] (HTS).
Verdicts per rule set and coil class (fixed now): OPEN (feasible at eta 3), CONDITIONAL (feasible only at eta >= 5),
CLOSED (no feasible sample). Report best P_net, its point, and the count of feasible samples.
Labels: ESTIMATE; eta 5/10 UNVERIFIED; a random sample can miss narrow windows (5000 of 115,200 grid points).
Referee: one independent review after the run; fixes only via _DEVIATIONS.md before one rerun.
