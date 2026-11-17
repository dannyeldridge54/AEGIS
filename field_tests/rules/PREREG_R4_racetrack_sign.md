# PREREG R4 — sign and size of the Green–Schwarz tilt with a racetrack dilaton sector (follows D1016)
Locked 2026-11-17 before any R4 number.
Setup (D1011 structure, real S = s): Y = 2s − δL, Ω = A₁e^{−a₁s} − A₂e^{−a₂s}, a_i = 8π²/N_i. Dilaton held at its
supersymmetric racetrack minimum F_S = Ω_s − Ω/Y = 0 (Ã = 0 there, and Ã is quadratic in F_S, so dÃ/dL = 0 at the
minimum); s therefore follows L: s*(L). Remaining L-dependence of the inflaton potential's prefactor: G(L) = Ω(s*)²/Y(s*, L)
(e^K ∝ 1/Y, |Ω|²). Ratio R = (d ln G/dL)/(δ/Y) (R = +1: the D1010 e^K-only case; R = −1: D1016 single condensate).
Grid: (N₁, N₂) ∈ {(5,6), (6,7), (8,9), (10,11)}, A₁ = 1, A₂ ∈ {1, 2}, δ = 1e-3 (small; R is δ-independent at O(δ));
derivative by central differences in L (h = 1e-3) after solving F_S = 0 by root finding.
Report R, s*, Y for each. Claim to test: "R > 0 for the racetrack (tilt sign as observed for δ_GS > 0)" — TRUE if R > 0 on all
grid points, FALSE if R < 0 on all, MIXED otherwise.
