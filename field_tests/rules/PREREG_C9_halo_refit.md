# PREREG C9 — refit the McMillan17 dark halo (NFW) to the Eilers+2019 rotation curve, with McMillan17 baryons fixed — locked 2026-11-17, before code or run
Data: Eilers et al. 2019 (arXiv:1810.09466v2) Table 1, transcribed via WebFetch to field_tests/data/eilers2019_table1.csv (38 rows).
- Used: R = 5.27–20.78 kpc (32 points). The 6 outer points with σ > 5 km/s are dropped (stated).
- σ = mean of σ⁻ and σ⁺, statistical only. A 2% systematic floor (Eilers' quoted 2–5%) is added in quadrature as a reported variant.
- Eilers' R0 = 8.122 kpc (GRAVITY 2018, as used by Eilers; labelled recalled). Their R values are used as given.
Model (galpy McMillan17 components): baryons = DiskSCF [0] + SCF bulge [2], fixed. Halo = NFW(amp, a) refit, starting from the McMillan17 NFW.
- v_c² = v_c,bar² + v_c,NFW². Least squares on (amp, a) with scipy least_squares.
Scored:
- Q1: fit quality, χ²/dof < 2 with the statistical errors.
- Q2: the fitted local slope dv_c/dR at R = 8.178 is negative. That is the D1203 defect test (McMillan17 had +1.3).
Reported:
- fitted (ρ_s, r_s); v_c(8.178); κ, Ω and dv/dR at 8.178;
- Horta+2026 pulls on v_c, Ω and κ;
- ρ_DM☉, M200;
- the 2%-floor variant.
- The original McMillan17 χ² on the same data, for comparison.
