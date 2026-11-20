# PREREG_A3_D6_ANISO — does the D = 6 result survive unequal radii? (locked D1682, 2026-11-20 00:48 UTC)
Same validated code (D1680), Γ_{4,4} = Π_i Γ_{1,1}(R_i), with B = 0. Radii sets: (1,1,1,2), (1,1,2,2), (1,2,2,2), (1,1,1,3), (1,1,3,3), (1.5,1.5,1.5,1.5), (1,1,1,1.3).
Question: is I < 0 only when SEVERAL radii sit near the self-dual value, i.e. is the positivity condition "volume beyond ~1.3⁴ ℓ_s⁴", or "every radius beyond 1.3"?
Reading: report I for each set, and whether sign(I) tracks the total volume V = Π R_i (I > 0 for all sets with V ≥ 4 counts as "volume-controlled").
Script: field_tests/scripts/a3d6/aniso.py
