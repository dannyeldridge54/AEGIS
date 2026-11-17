# PREREG D9 — galpy-backed orbit path for the Star Mapper (prepares the McMillan17 default) — locked 2026-11-17, before code or run
Motivation: C8/D1194 (MWPotential2014 FAILS Horta+2026; McMillan17 PASSES). galpy's C integrator does a 3-Gyr McMillan17 orbit in 0.02 s (timed this tick), so a galpy path is practical.
New function, added after this lock: mapper_feed.orbit_params_galpy(x, y, z, vx, vy, vz, pot='MWPotential2014'|'McMillan17', t_gyr=3).
- Galactocentric cartesian → (R, vR, vT, z, vz, φ) in physical units, galpy Orbit arrays, dop853_c, 3001 output points.
- Returns r_peri, r_apo (spherical), z_max, ecc.
- The existing functions are untouched.
Regression (scored):
- R1: for 5 fixed test stars, orbit_params_galpy(pot='MWPotential2014') agrees with orbit_params (our galaxy.py, DOP853) within 1% on r_peri, r_apo and z_max.
- Test stars, Galactocentric kpc and km/s, solar-like to halo-like:
  - (−8, 0, 0.02, 11, 232, 7);
  - (−8.5, 1, 0.3, 30, 200, 20);
  - (−6, −2, −0.5, −50, 180, 40);
  - (−10, 3, 1.5, 80, 120, −60);
  - (−7, 0.5, 2.0, 150, 60, 100).
Reported: the same stars with pot='McMillan17' (galpy), as the change in orbit parameters a default switch would bring.
NOT done this tick, and why:
- The default is not flipped. A real switch also changes the Sun's frame constants (v0 = 233.1 and R0 = 8.21 for McMillan17 vs 220/8.0 in mapper_feed V_SUN/R0_XY). That changes every Galactocentric velocity, so it is a separate locked step.
- The Star Mapper on Danny's PC uses its own copy, which is left untouched.
