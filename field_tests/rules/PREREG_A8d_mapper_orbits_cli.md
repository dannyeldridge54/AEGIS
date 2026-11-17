# PREREG A8d (track X, Hyperion -> Star Mapper PC version; Danny 17 Nov 06:43 CT "Start pc version publish and push"): the Mapper orbit CLI (written before running)
Code: tools/janus_astro/mapper_orbits.py and ufe-v2/START_HYPERION_ORBITS.bat as committed with this lock (never run before it). Read-only on the sweep.
Test data: two synthetic tiles (seed 5) in the Star Mapper's tile format (gzip CSV, the star_scanner COLUMNS + ASTROMETRY_FIELDS headers), 60 rows each, including rows with no radial velocity, rows with parallax_over_error ≤ 5, and rows with empty r_med_geo, written to a scratch cosmos_map/tiles/L5/.
Tests:
M1 selection: exactly the rows with a finite radial_velocity and parallax/parallax_error > 5 are processed; rows with empty r_med_geo carry the 'dist_parallax' flag; every row carries 'MG_noext'.
M2 values: every output number equals a direct call (icrs_to_galactic, galactocentric, abs_mag_G, fast.orbits_fast on the same inputs) to ≤ 1e-12 relative (absolute 1e-12 where the value is 0) after the CSV round trip (written with repr precision).
M3 resumability: a second run processes 0 tiles and skips 2; outputs unchanged (byte-identical).
M4 summary: hyperion_orbits.json has version, model, n_stars (= processed rows), tiles with n/med_ecc/med_zmax/med_rperi/med_rapo, most_eccentric sorted descending (≤ 50 entries).
Pass M1–M4 → A8d VALIDATED (the PC version is ready to run on real tiles). Real-data run happens on Danny's PC (no Gaia tiles here).
Output field_tests/results/janus_astro_a8d.txt via theory/janus_astro/a8d_check.py. No reruns to chase; DEVIATIONS first.
