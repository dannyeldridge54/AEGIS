# PREREG PROM-3 — cycle 3: fix R85, then the big loom up to the GOAL node (net electricity). Locked before computing, 2026-11-23 12:10 CT
Danny 11:15: "every time you come to a stop, implement fixes and do the big loom ... do all the ping pongs."
Hints: tools/fusion/hints/cycle3.json (14 usable; misses logged). Act on 1-5, 7-11.
FIXES (R85): F1 report P_LH from BOTH laws: Martin 2008 x 2/A_eff (Righi 1999) and the ITER Physics Basis 1999 law; compare the 1999 law
  with the FDR table (51 MW at 500 MW). F2 every future held-out test must be shown to move when the change is switched off
  (a sensitivity check is part of the test, or it does not count).
GOAL NODE (S0 plant), on the fractal net above S1-S7:
  P_th = M P_n + P_alpha + P_aux;  P_gross = eta_th P_th;  P_recirc = P_aux / eta_wp + f_pump P_th + P_other;  P_net = P_gross - P_recirc;
  Q_e = P_gross / P_recirc.  Inputs are labelled with their sources (no tuning).
GOALPOSTS:
  E1 ARC consistency (data): with P_fus 525, P_aux 38.6, eta_th 0.40: the M that reproduces P_tot 708 MW is reported; then P_gross =
     283 MW +- 1 and, with P_net 190, P_recirc = 93 MW and Q_e = 3.0 +- 0.05. (Bookkeeping check of the node, not a prediction.)
  E2 DEMO-A multiplication: M = 1 + 321 / (P_n of 1686 MW) reported and inside DEMO's 1.2-1.3 (Federici).
  E3 PREDICTION (labelled): the model's own ITER 500 MW plasma (S3) with a DEMO-style plant (M from E2, eta_th 0.368, eta_wp 0.4,
     f_pump 0.085 helium, P_other 0 as a best case) -> P_net, Q_e. Sensitivity: P_net with eta_wp 0.25 (achieved) also reported.
  E4 GOAL DIALS: on the ITER machine, choose <n> (scan) and P_aux in {30, 40, 50, 60, 73} MW to maximise P_net subject to f_G <= 0.94,
     beta_N <= 2.8, P_loss >= 1.3 P_LH (Martin x 2/A_eff); report the best point and the binding limit; and show it moves if the plant
     inputs change (F2).
  E5 S1, S2, S4-S7 unchanged.
Referee after the build; DEVIATIONS first; one rerun. A stop (NULL) triggers fixes + the next big loom, not an end (Danny 11:15).
