# DEVIATIONS for PREREG_D779
D1 (run 1 failed K4: SVs (0, √2, √2) ≠ (c, c, √2), and crashed): the basis was built from n and Y* = (1, −i)/√2 = n, the same vector twice, so it was singular. Fix: use n and Y as the two doublet basis vectors (orthonormal: n†Y = 0). No other change. Run 1 is kept as INVALID.
D2 (run 2 crashed, NaN): applying D1 by sed commented out the trailing 'B[2,2]=1' on the same line. Restored; no other change. Run 2 produced no results (crash), so nothing is kept from it.
