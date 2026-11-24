# PREREG D2244 — Negative-triangularity (NT) mode: full reactor redo in one pass (locked 2026-11-23)

Why: D2243 closed every tokamak design on H-mode access (best f_LH 0.38). NT tokamaks run in L-mode with H-mode-level
confinement and need no L-H threshold (review arXiv:2606.26513: H98 >~ 1 on DIII-D/TCV; ELM-free up to 10x P_LH;
core radiated fraction raised to 0.45-0.55 by seeding without L-H limitation; detachment needs ~>0.9 n_G on DIII-D;
beta_N routinely >2.5, ideal ~3, somewhat below positive triangularity; confinement degrades more steeply with power;
mostly carbon-wall data).

Engine: D2243 engine with its deviations (Psep = P_alpha + P_aux - P_rad_core everywhere; Psep >= 1 MW; Psep/R <= 17;
seeding <= 5%; core argon = c/eta; 5 impurity iterations; Greenwald 0.94; wall 2 MW/m2; TBR margin; coil post hoc 12/20 T;
blanket 90% Li-6 10 cm). NT changes only:
- H-mode access (L-H) limit REMOVED.
- Confinement IPB98 x H98 with H98 = 1.0 (NT-1.0, literature) and H98 = 0.8 (NT-0.8, pessimistic for power degradation /
  metal wall). Two physics passes.
- Detachment density: density fixed at 0.9 n_G (DIII-D requirement).
- Pressure: beta_N <= 2.8 primary; beta_N <= 2.5 reported variant (NT slightly lower limits).
- Divertor model unchanged (Eich lambda_q, Lengyel); outboard-divertor area benefit NOT credited (conservative).
Not changed / flagged: pedestal profile shapes retained (NT is L-mode-like: profile effect unmodelled); synchrotron budget
unverified (R111 F5); E2 = Psep*B/(q95 A R) <= 9.2 reported as variant.
Search: 2500 points per pass, uniform without replacement (seed 2244) from R[6.2,7,8,9] B[5.3,6,7,8,9]
fAr[0.0014,0.003,0.005,0.008] leg[1..5] Paux[10,20,30,50] nu[0.4,0.5,0.6] eta[3,5,10] (14,400-point grid, 17%).
Control: D2243 engine (with L-H) at the D2241 point must fail with LH among violations.
Verdicts per pass x coil class (fixed now): OPEN (feasible at eta 3), CONDITIONAL (only eta >= 5), CLOSED.
Report best P_net design with full plant numbers, count feasible, and the most-ready (fewest violations) design if none.
Labels: ESTIMATE; self-check plus one referee micro-round; fixes only via _DEVIATIONS.md before one rerun.
