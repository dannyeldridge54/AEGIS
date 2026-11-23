# SPEED-hyperion deviations (referee R80, written before fixes)
R80 MAJOR: the 4e-11 agreement holds only for smooth profiles; a cored profile whose core edge lies inside [b_mask, psi_max] misses the
1e-6 gate (1.75e-6 NFW rc 0.1 kpc HESS; 1.1e-5 Einasto rc 1 kpc psi 10 deg). The locked cored test never reached that regime.
MINOR: b_mask_deg = 0 crashes (log 0). Speedup is case-dependent (26-65x under load vs 102x locked).
Fixes (DEV-1): J_route_A_fast falls back to J_route_A when b_mask_deg <= 0 or when called with smooth=False; settings.jfactor keeps
fast=True (it only reaches HESS_IGS with uncored Einasto/NFW/Burkert, which R80 confirmed at <= 1e-12); docstrings state the scope:
"smooth (uncored) profiles only; cored profiles use the reference route". H1 verdict unchanged for the locked cases; scope narrowed.
