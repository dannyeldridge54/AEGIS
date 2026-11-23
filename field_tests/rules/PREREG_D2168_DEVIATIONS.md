# D2168 DEVIATIONS
## DEV-1 (written before the rerun): crash fix
The first run crashed inside SLSQP: a trial step took a log dial to exp(-huge) = 0 (ZeroDivisionError in L2 M_N_top). Fix: bounds |z_j| <= 3 on every dial (a factor e^3 = 20 in the log dials; +-3 on split/dNeff), and a failing evaluation returns -1e6 for every node (infeasible). No equation, scale or readout changed. No result existed from the first run.
