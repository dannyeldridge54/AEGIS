# FUSION-1 deviations (written before any fix or rerun). Hints read online first (Danny 10:57: "look online first, hints, fix").
Runs as locked: G1 PASS; G2 FAIL (share); G3 PASS; G4 PASS; G5 PASS (by cancellation, R82); G6 FAIL; G7-G9 PASS; G10 FAIL (0.51%);
G11 reported; G12 partial; G13 FAIL. These stay recorded as failed-as-locked.

From R81 (S1, S7):
- DEV-1 G2 goalpost was a mass-number shortcut (14.07 = 0.8 x 17.59) with an arithmetic slip (0.7999, not 0.7997). Corrected benchmark:
  reactants at rest, relativistic two-body E_n = 14.028 MeV, share 0.7976 +- 0.001 (NeSST arXiv:2605.20432; Ballabio et al. 1998).
- DEV-2 G13 goalpost paired 5.9 keV (15 MK) with 15.7 MK. Rerun checks both: 5.9 keV at 15 MK +- 3%, and the textbook formula
  1.22 (Z1^2 Z2^2 A T6^2)^(1/3) keV at 15.7 MK (6.07 keV) +- 3%.
- DEV-3 net.settle() returns a converged flag (not just max_sweeps); postulates are collected and judged by the parent.
- D-He3 coefficients confirmed against METIS, ASCOT5, PROCESS, PlasmaPy: "as recalled" flag removed.
From R82 (S2, S3) and the ITER FDR Physics Table 4.3.1-1 (500 MW column) read online:
- DEV-4 add synchrotron radiation (Albajar et al. 2001 fit with the Fidone reflection term, as given by UKAEA PROCESS docs:
  wall reflectivity 0.6, beta_T = 2 for (1 - rho^2)^alpha_T profiles) and line radiation. Line radiation needs impurity cooling
  rates not yet wired: it is taken as an INPUT = 27 MW (the ITER column) and labelled so.
- DEV-5 plasma composition from the ITER column instead of one Z=4 impurity: f_He 3.2% (avg), f_Be 2.0%, f_Ar 0.14% (axis values used
  as averages, labelled), fully stripped; n_DT/n_e and Z_eff computed from it (expect Z_eff ~1.73 vs table 1.72); T_i/T_e = 8.1/8.9.
- DEV-6 scalings use the line-averaged density (Greenwald, IPB98, Martin); ITER V = 831 m^3 and S = 683 m^2 from the table.
- DEV-7 G5/G6 re-locked to ONE column (500 MW): at <n_e> = 1.13e20 and P_aux = 50 MW the model should give P_fus 500 +- 20%,
  tau_E 3.4 s +- 15%, W_th 353 MJ +- 15%, beta_N 2.0 +- 15%, P_rad 61 MW +- 25%, P_loss 104 MW +- 20%. These are new goalposts, set
  after seeing run 1; they are labelled post-hoc.
- DEV-8 dials: Greenwald fraction capped at 0.94 (the ITER design value); the report names the binding constraint.
- DEV-9 G3's flag stored as a real boolean.
R83 (S4-S6) findings will be appended here before their fixes. One rerun of all tests after all fixes.
