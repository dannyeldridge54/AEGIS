# PREREG SPEED-Aion (rotation rung 2, one wave), locked 2026-11-23 ~09:20 CT before code
Reference: tools/gifts/aion/aion.py (unchanged). Fast path: aion_fast.py.
A1 scan3s vectorised with numpy broadcasting over (s12, s23, s13, delta): every reported range endpoint equals the reference
   to 1e-12 (relative) on the same 9x9x9x73 grid, both orderings.
A2 the MC 1-sigma sampler vectorised: identical numbers for the same seed (1e-12).
Timing: median of 3. Field map: neutrino mass and mixing -> releases/field_maps/neutrino_mass.md.
