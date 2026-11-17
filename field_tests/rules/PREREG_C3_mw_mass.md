# PREREG C3 — Milky Way enclosed mass: MWPotential2014 vs Gaia-era Jeans masses (Djl C) — locked 2026-11-17
Data (quoted, Bird et al. 2022, arXiv:2207.08839, Table 1; LAMOST/SEGUE/Gaia K giants and BHB stars; 3D spherical Jeans):
- M(<73 kpc) = 4.3 ± 0.95 e11 M_⊙ (KG)
- M(<52 kpc) = 4.1 ± 1.2 e11 M_⊙ (BHB)
Model: M(<r) ≈ r v_c(r)²/G, with v_c from galpy MWPotential2014 in the plane (ro = 8, vo = 220). Spherical approximation; G = 4.30091e-6 kpc (km/s)² M_⊙⁻¹ (IAU-based value as used by galpy/astropy; computed in code from astropy constants).
Cases: halo amplitude s = 0.8, 1.0, 1.2, 1.5 (W2/D1089 handles).
Scored per case: CONSISTENT if both points are within 2σ, TENSION if worse than 2σ but within 3σ, EXCLUDED beyond 3σ.
Reported: the pulls, and which s range the two points allow.
Script theory/wiring/c3_mw_mass.py (written after this lock).
