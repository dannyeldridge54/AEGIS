# DEVIATIONS D9 — written after run 1 FAILED R1, before the rerun (2026-11-17)
D1: unit bug. galpy's Orbit treats plain floats as NATURAL units even when ro/vo are given. Passing kpc and km/s made every orbit ~ro× too large (r_apo ~1e5 "kpc").
- Fix: pass R/ro, vR/vo, vT/vo, z/ro, vz/vo, φ. Outputs are already physical (ro/vo set).
- No other change. Run 1 is kept as d9_galpy_path_run1.txt.
- R1's scored FAIL on run 1 stands in the record. The rerun scores the corrected code.
