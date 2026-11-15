# PREREG D594: direct check of the D592 extrapolation (locked before computing)
Same toy and code as D592 (adiabatic_y_d592.py, unchanged physics), with the R loop changed to m/H_end ∈ {200, 320}. Report f_Y and f_track.
Verdict:
- If f_Y(320) ≤ 2e-13, the D592 requirement is CONFIRMED directly (no extrapolation).
- Otherwise, report the R at which 2e-13 is reached, by power-law interpolation between the computed points.
Also report the local power slopes for 100→200 and 200→320.
Numerical guard (fixed now): if f_Y falls below 1e-18, report it as "below numerical floor (rtol 1e-10)" rather than as a value.
Fixes go in PREREG_D594_DEVIATIONS.md, written first.
