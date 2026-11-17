# PREREG D10 — Star Mapper orbit model switch: McMillan17 default with consistent solar frame — locked 2026-11-17, before code or run
Change (written after this lock):
- mapper_feed.galactocentric gets optional r0_xy and v_sun arguments. The defaults are unchanged (8.0 kpc; (11.1, 232.24, 7.25) km/s), so all existing callers and validations (A5a/A8*) are untouched.
- mapper_orbits.run/process_rows get model ∈ {'McMillan17' (new default), 'MWPotential2014' (legacy)}.
  - McMillan17 frame: R0 = 8.21 kpc and v0 = 233.1 km/s (McMillan 2017's own values, as in galpy's McMillan17, C7/C8), with the Schönrich+2010 solar motion (11.1, 12.24, 7.25). So v_sun = (11.1, 245.34, 7.25) and z_sun = 20.8 pc (unchanged).
  - Orbits through mapper_feed.orbit_params_galpy(pot='McMillan17') (D9-validated).
  - Output goes to cosmos_map/hyperion_mcm17/L5/, so legacy MWP2014 results in cosmos_map/hyperion/L5/ are never mixed (the run is resumable by tile).
  - Summary version 'hyperion-orbits-2' with an honest model string.
  - CLI flag --model.
- The legacy path (model='MWPotential2014') is byte-for-byte the old code path: same output dir, version and orbit engine.
Tests (scored):
- T1: legacy path. process_rows(rows, model='MWPotential2014') equals the pre-change process_rows output exactly on a synthetic 20-star tile (fixed seed).
- T2: frame consistency. The LSR point (x = −8.21, y = 0, z = 0.0208 kpc; v = (0, 233.1, 0)) has ecc < 0.01 in McMillan17, and its r_peri/r_apo lie within 2% of 8.21.
- T3: smoke test. process_rows(rows, model='McMillan17') on the same tile returns 20 finite rows with 0 ≤ ecc < 1.
The PC copy is untouched. The next PC run would need Danny's PC linked, and its output goes to the new directory.
