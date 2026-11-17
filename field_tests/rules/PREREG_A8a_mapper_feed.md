# PREREG A8a (track X, Hyperion -> Star Mapper; Danny 17 Nov 06:19 CT "continue developing it cause it can feed mapper"): Gaia astrometry to Galactic orbits (written before running)
Code: tools/janus_astro/mapper_feed.py as committed with this lock (never run before it). Inputs are exactly the Star Mapper's Gaia DR3 columns (ra, dec, parallax / r_med_geo, pmra, pmdec, radial_velocity, phot_g_mean_mag). No Gaia data is in this workspace (the sweep lives on Danny's PC), so the test uses 200 synthetic stars (seed 2026: ra U[0,360), dec asin U[-1,1], d U[0.05, 5] kpc, pm N(0, 20) mas/yr, rv N(0, 50) km/s); 30 of them for orbits.
Tests:
F1 ICRS -> Galactic (l, b) vs astropy (ICRS -> Galactic) for the 200 stars: max angular difference ≤ 1e-6 deg (the NGP constants are rounded to 1e-5 deg in the docstring; stated).
F2 Galactocentric position and velocity vs astropy Galactocentric(galcen_distance = sqrt(8.0² + 0.0208²) kpc, z_sun = 20.8 pc, galcen_v_sun = (11.1, 232.24, 7.25) km/s, roll = 0): max |Δx| ≤ 1e-6 kpc and |Δv| ≤ 1e-4 km/s.
F3 orbit parameters (r_peri, r_apo, z_max, e) for 30 stars, 5 Gyr: Hyperion vs galpy Orbit built from the same Galactocentric cylindrical coordinates (natural units ro = 8, vo = 220), integrated in MWPotential2014 on the same time grid (dop853_c), r_peri/r_apo/z_max as min/max over the grid: relative ≤ 1e-4 each (spherical r; galpy's r = sqrt(R² + z²)).
Pass F1–F3 → A8a VALIDATED.
Reported: the Sun's own orbit parameters, the per-star time cost, and a sample feed record (JSON) for the mapper.
Output field_tests/results/janus_astro_a8a.txt via theory/janus_astro/a8a_check.py. No reruns to chase; DEVIATIONS first.
