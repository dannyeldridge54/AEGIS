# PREREG D2271 — Modulus masses in the Zhinu potential at rho and i (locked 27 Nov 2026)
**Potential.** V0 = V_inf |grad ln Lambda|^2 / lambda^2 with Lambda = E(tau,3/2)^(-a), hyperbolic gradient |grad f|^2 = y^2 (f_x^2 + f_y^2).
**Analytic claim (before computing).** The Zhinu identity V0/V_inf = 1/3 + (4/3) Lap ln Lambda follows from Lap ln E = s(s-1) - |grad ln E|^2
only if a = 1/3 and lambda^2 = 1/4 (constants a^2 s(s-1)/lambda^2 = 1/3, a/lambda^2 = 4/3 at s = 3/2). Then V0 = (4/9) V_inf |grad ln E|^2,
the 4/9 = (2/3)^2 of D2259 is this prefactor, and with K = -n log y the canonical masses are m^2 = (16/9) e_k^2 V_inf / n, e_k the eigenvalues of
y^2 Hess E / E: at rho e = 3/8 (double) -> m^2 = V_inf/(4n) (= D2259's v3/YFORK2 "V_inf/4" at n = 1); dropping the 4/9 gives 9/16 (literal v4).
At i: e = -0.21961, +0.96961 -> m^2 = 0.0857 and 1.671 V_inf/n.
**Numeric check.** Finite-difference Hessian of V0 (mpmath E, dps 30) at rho and i, canonical with n = 1; also check the identity holds at 5 random
points to 1e-8. PASS if all agree to 1e-6 relative. Run once. Output field_tests/results/d2271_zhinu_masses.json.
