# PREREG D595: replace D591's estimated "~180×" stiff-phase growth with a computed number (locked before computing)
Using the D592 background code (no Y field):
- integrate the SERAPIS two-term φ background from 3 e-folds before the end to N_end + 3;
- measure ln ρ_φ against N; take the effective w over [N_end + 0.5, N_end + 1.5] and [N_end + 1.5, N_end + 3] from the slope, d ln ρ/dN = −3(1 + w).
Then the growth factor of f_Y (free Y, matter-like) from N_end + 1.5 to the octic→quadratic crossover is G = (a_x/a_1.5)^{3w}, with a_x set by ρ_x/ρ_end = 2.4e-6 (D578, C1) and the measured w for the later window.
Updated requirement: f_Y(N_end + 1.5) ≤ 4e-11/G. Report the R that meets it, interpolated from the D592/D594 points.
Fixes go in PREREG_D595_DEVIATIONS.md, written first.
