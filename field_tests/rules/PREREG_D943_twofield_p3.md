# PREREG D943: does the heavy-field form of P3 (D941) reproduce SERAPIS-E? (two-field background check)
Model: path Re tau = 1/2 (SERAPIS-E), y = Im tau, phi = ln(y)/sqrt2 (K = -log y, n = 1). Ehat(y) = E(tau,2) - E(rho,2), E from its Fourier expansion (Bessel terms n <= 12).
Single-field (P3): V1 = Ehat/(Ehat+1) * (1 + C Ehat).
Two-field (D941): V2 = [Ehat chi^2 + (1-chi)^2] (1 + C Ehat), chi = sigma/M with sigma canonical; field space flat.
C = 1.15e-6 (middle of the paper's 1.0-1.3e-6). M = 0.1, 0.2, 0.5 (Planck units).
Method: e-fold-time background ODEs for canonical fields, start deep on the plateau on the chi* = 1/(Ehat+1) valley with slow-roll velocity, end at eps_H = 1; N* = 55 before the end. Observables at N*: n_s = 1 - 2 eps_H - dln eps_H/dN, r = 16 eps_H (first-order Hubble-flow; same formula for both models, so the DIFFERENCE is what is tested). Turn rate Omega/H along the two-field path and the heavy-mass estimate 1 - c_s^2 = 4 Omega^2/(m_eff^2/H^2) (no exact MS spectra in this check).
PASS (fixed now): for M = 0.1 and 0.2, |n_s(2f) - n_s(1f)| <= 5e-4, |r(2f)/r(1f) - 1| <= 2%, and 1 - c_s^2 <= 1e-2. M = 0.5 reported only.
FAIL otherwise. Either way frozen predictions are unchanged; this tests only whether D941 can stand in for P3.
Script theory/flux/twofield_p3_d943.py; output field_tests/results/twofield_p3_d943.txt.
