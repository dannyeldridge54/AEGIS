# PREREG D2266 — Can one distance |u| from tau = i do the lepton jobs at once? (locked 27 Nov 2026)

**Coordinate.** u = (tau - i)/(tau + i), x = |u| (the same coordinate in Feruglio 2302.11580 and in 2609.09262).
**Inputs (fixed now).**
- Neutrino scaling near i, Feruglio's only data-compatible class (k_S odd, m_nu(0,0) singular): r = dm2_sol/dm2_atm = c_r x^3, sin^2 theta13 = c_13 x^2.
- Data (NuFIT 6.0, normal ordering): dm2_21 = 7.49e-5 eV^2, dm2_31 = 2.513e-3 eV^2 (r = 0.02980), sin^2 theta13 = 0.02195.
- Charged-lepton "octave" point (2609.09262): tau = 1.0685 i, so x_oct = 0.0685/2.0685 = 0.03312.
**O(1) window.** A coefficient is natural if 1/3 <= c <= 3.
**Test.** X_nu = the set of x in [0.005, 0.6] where both c_r and c_13 are in the window. PASS (one |u| works) if x_oct lies in X_nu.
FAIL if X_nu is empty or excludes x_oct. Report X_nu and the coefficients at x_oct.
**Out of scope (no near-i power law in hand):** the mu term (2412.07642) and the quark ladder. Reported OPEN, not tested.
**Run once.** Output field_tests/results/d2266_one_u.json.
