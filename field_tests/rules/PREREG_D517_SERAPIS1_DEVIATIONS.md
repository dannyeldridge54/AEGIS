# D517 DEVIATIONS (written before rerunning)
D1. In the first run (kept as results/serapis1_d517_run1.txt) V(i)/V_pl came out 1.3e-51 against the 2.1e-110 target. That is the 50-digit floor: j(i) − 1728 ~ 1e-48 numerically, so the √ main term
leaves ~1e-24 and V ~ 1e-51. Fix: recompute V(i) and the Hessian at 200 digits (mp.dps = 200, more q-terms). Inflation numbers and criteria unchanged (they were computed and are kept).
