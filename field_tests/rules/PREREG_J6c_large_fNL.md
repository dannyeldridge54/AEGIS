# PREREG J6c — Janus two-field δN in a LARGE f_NL case (T5 of the J6 plan)

Locked 2026-11-17 before any J6c number is computed.

## Reference (fetched, Byrnes, Choi & Hall 0807.1101, ar5iv)
Sec. V.1 Example A: W = ½ e^{−λφ²} m² χ² (M_P = 1), χ* = 16, full equations solved to ε = 1; Fig. 4: λ = 0.05, φ* = 1e-3.
Analytic product-potential result, WMAP sign: Eq. 21
 f_NL^(4) = (5/6)·2/(u²/ε_φ* + v²/ε_χ*)² · [u³/ε_φ*(1 − η_φφ*/(2ε_φ*)) + v³/ε_χ*(1 − η_χχ*/(2ε_χ*)) − (u/ε_φ* − v/ε_χ*)² A_P],
 Eq. 18 u = ε_φ^e/ε^e, v = ε_χ^e/ε^e; Eq. 22 η̂ = (ε_χη_φφ + ε_φη_χχ)/ε; Eq. 23 A_P = −(ε_φ^e ε_χ^e/(ε^e)²)[η̂^e − 4ε_φ^eε_χ^e/ε^e];
 Eq. 24 ε_φ = ½(U_φ/U)², ε_χ = ½(V_χ/V)²; Eq. 25 η_φφ = U_φφ/U, η_χχ = V_χχ/V. End quantities ^e at the numeric ε_H = 1 point.

## Numeric
Janus δN (as D999/D1000): N to ε_H = 1, slow-roll start velocity; f_NL = (5/6) N_aN_bN_ab/(N_cN_c)²;
anisotropic central differences h_φ = φ*/10, h_χ = 1e-3, and the halved pair for convergence.

## Cases
A1: λ = 0.05, φ* = 1e-3, χ* = 16.   A2: λ = 0.04, φ* = 1e-3, χ* = 16.   A3: λ = 0.05, φ* = 1e-4, χ* = 16.

## Tests
T5: for every case |f_NL,num − f_NL,Eq21| < 0.10·|f_NL,Eq21| (slow-roll analytic vs exact numerics; 10 % allowed for
    the ε → 1 end region where Eq. 21's slow-roll ends are approximate).
T5L: at least one case has |f_NL| ≥ 1 (else the test is INCONCLUSIVE for "large f_NL", recorded as such).
T6: convergence, h vs h/2: f_NL relative change < 2e-2 in every case.
Verdict VALIDATED iff T5, T5L, T6 pass; NOT VALIDATED if T5 or T6 fails; INCONCLUSIVE if only T5L fails.
Fixes only via PREREG_J6c_large_fNL_DEVIATIONS.md before any rerun.
