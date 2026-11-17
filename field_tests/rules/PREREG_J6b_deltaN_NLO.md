# PREREG J6b — next-to-leading-order δN power spectrum and r (follows D999)

Locked 2026-11-17 before any J6b number is computed.

## Formulas (fetched; arithmetic rotation marked [derived])
- Byrnes & Wands astro-ph/0605679 (ar5iv): Eqs. 43–45, at Hubble exit, C = 2 − ln2 − γ_E ≈ 0.7296:
  P_σ = (H/2π)²(1 + (−2+6C)ε − 2Cη_σσ), C_σs = −2Cη_σs (H/2π)², P_s = (H/2π)²(1 + (−2+2C)ε − 2Cη_ss).
  Eq. 81: P_X ≃ P_X^(0)(1 + n_T − C n_X) for adiabatic, isocurvature and tensor spectra; with n_T = −2ε
  this gives P_T = P_T^(0)(1 + (−2+2C)ε).
- η_IJ = V_IJ/(3H²) (Avgoustidis et al. 1110.4081 Eq. 2.8 notation); ε = ε_H on the slice.
- [derived] field basis: M_IJ = δ_IJ(1 + (−2+2C)ε) + 4Cε σ̂_I σ̂_J − 2C η_IJ, σ̂ = unit field velocity.
- P_ζ = (H*/2π)² N_I M_IJ N_J;  r = 8(1 + (−2+2C)ε)/(N_I M_IJ N_J)  (P_T^(0) = 8(H*/2π)², VW Eq. 28 at lowest order).
- N_I as in J6 (theory/janus/j6_deltaN.py deltaN, h/2 values).

## Tests
T1b m²φ² single field at the J6 point (φ* = 15.3): |r_NLO − r_calc|/r_calc < 1e-3 (calculator second-order r = 16ε₁(1 + C_E ε₂)).
T2b equal masses, angles 0.1, 0.5, 0.9, 1.3: r_NLO spread < 1e-6 relative and equal to T1b's r_NLO to 1e-6.
T3b VW point (R = 1/9, (8.2, 12.9)): report r_NLO and the NLO/LO ratio (no pass criterion; record only).
Verdict VALIDATED iff T1b and T2b pass. Fixes only via PREREG_J6b_deltaN_NLO_DEVIATIONS.md before any rerun.
