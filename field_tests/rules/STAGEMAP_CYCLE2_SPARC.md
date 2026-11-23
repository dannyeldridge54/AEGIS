# STAGE MAP cycle 2 — SPARC (written before computing)
Code-to-code with cfspopcon itself is BLOCKED here: its pipeline needs radas atomic data (OpenADAS download not reachable), even for Z_eff/dilution.
One change from cfspopcon's own SPARC_PRD input.yaml (github.com/cfs-energy/cfspopcon, example_cases/SPARC_PRD): geometry and impurities as THEY use them:
areal elongation 1.75, inverse aspect ratio 0.3081 -> V = 2 pi R^3 eps^2 kappa_A (pi - (pi - 8/3) eps) = 19.80 m^3 (we used Creely's 20.9);
O 3.1e-3 (we used the quasi-neutrality value 3.61e-3); He 0.06, W 1.5e-5, 50/50 D-T as before; T peaking 2.5; Ti/Te 1. Same L4 goalpost (140 MW +-25%,
7.3 keV +-20%), popcon convention. One run; the referee batch reviews it.
