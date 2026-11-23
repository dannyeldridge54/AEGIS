# PREREG PROM-4 — cycle 4: inertial fusion ignition model (locked before computing), 2026-11-23 13:10 CT
Hints: tools/fusion/hints/cycle4.json (12; act on 1-6, 9). S4 gains an ignition engine:
  hot-spot radius from volume (sphere); G_LC = (p/420 Gbar)(R/50 um); f_alpha = E_alpha/(2 E_hs) with E_alpha = Y/5; the pressure
  DERIVED from yield, temperature, burn width and volume: p = 4 kT sqrt(Y_n / (<sv>(T) V tau)) (equal D-T, n_e = n_i, Bosch-Hale <sv>);
  chi_noalpha and the required-yield law as functions (no data to test them against here, reported only).
Goalposts (HELD OUT: N210808 published values are never used to tune; no knobs exist):
  I1 derived pressure from (Y 1.37 MJ, T 10.9 keV, tau 89 ps, V 6.4e5 um^3) within the published 569 +- 61 Gbar (1 sigma).
  I2 G_LC from the published p and V: > 1 (the paper: ignited by Eq. 2); also computed with the derived p.
  I3 E_alpha/(2 E_hs) from published Y and E_hs: > 1.4 (paper: satisfied).
  I4 target gain 1.37/1.917 = 0.715 (paper 0.72).
  I5 SENSITIVITY (F2 rule): the derived pressure moves by the expected sqrt law when tau or V change by 10% (the test can fail).
Referee after; DEVIATIONS first; one rerun.
