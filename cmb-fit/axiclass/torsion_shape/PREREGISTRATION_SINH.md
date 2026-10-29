# Pre-registered test: is the potential periodic in the Immirzi variable? (written before running, 2026-10-26 16:10 CDT)

Hypothesis. The torsion potential is periodic in gbar = 1/gamma = sinh(phi/sqrt(3/2) M_Pl), not in the canonical field:
V = Lambda^4 [1 - cos(g(phi)/F)]^3, g(phi) = s (sinh(phi/s + x0) - sinh(x0)) / cosh(x0), s = sqrt(3/2),
with the minimum at the loop-quantum-gravity value gamma0 = 0.2375, so x0 = arsinh(1/gamma0) = 2.1445 (FIXED, not fitted).
Same number of free parameters as the plain cosine (f_EDE, z_c, theta_i). Implemented as option axion_sinh_x0 in
AxiCLASS (regression-tested: with the option off it reproduces the original code to all printed digits).

Test. Planck 2018 + DESI DR2 + Pantheon+ (no SH0ES), best fit, compared with the plain-cosine torsion fit
(chi2_eff 2427.80) and LCDM (2434.22).

Decision rule (fixed now):
* chi2_eff(sinh) < chi2_eff(plain) - 2: the data prefers the torsion-derived shape (a fingerprint of the torsion origin).
* within +-2: the data cannot tell the shapes apart yet (expected for Planck alone; repeat with Planck+ACT+SPT).
* chi2_eff(sinh) > chi2_eff(plain) + 2: the data disfavours the periodic-in-gamma shape; report it.
