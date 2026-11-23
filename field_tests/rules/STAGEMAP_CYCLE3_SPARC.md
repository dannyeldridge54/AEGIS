# STAGE MAP cycle 3 — SPARC code-to-code (written before computing)
Build radas-format atomic data (one netCDF per element: coronal_Lz [W m^3] = PLT + PRB, coronal_mean_charge_state, equilibrium_* = coronal copies
over a ne_tau axis (stated approximation), dims dim_electron_temp [eV] x dim_electron_density [m^-3]) from our local OPEN-ADAS ADF11 mirror
(tools/fusion/adas/all; He, O, W, Xe, Ar). Then run cfspopcon 9.0.1's OWN SPARC_PRD pipeline (github cfs-energy/cfspopcon example_cases) unchanged
except radas_dir. Goalpost (marker B.L4): reproduce SPARC's PRD point with their code first (P_fus 140 MW cap, Q ~11, <T> ~7.3 keV), then compare OUR
engine at THEIR selected (n, T) point: P_fus within +-25% and required P_aux within +-25% of theirs. If their own code with our atomic data does not
reproduce 140 / Q ~11, the atomic data or pipeline is the issue and the marker stays OUT. Referee after; one rerun.
