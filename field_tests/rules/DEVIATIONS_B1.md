# DEVIATIONS B1 (written before any change) — 2026-11-17, found by B5 (D1106)
D1: bbn.Yp wraps CAMB's BBN_table_interpolator.Y_p, which returns the BBN NUCLEON fraction Y_p^BBN = 4·n_He4/n_b. It does not return the helium MASS fraction (CAMB docstring: "helium nucleon fraction"). bbn.py's docstring wrongly called it the mass fraction (CMB convention).
B1/B2/B3 compared Y_p^BBN to Aver+2021's Y_p, which is a mass fraction. That is unlike with like: 0.24721 vs the true mass fraction 0.24588 (table 'Yp' column), an offset of 0.0013.
Change: correct the docstring, and add bbn.Yp_mass (the table's 'Yp' column). bbn.Yp is left unchanged (it is still the nucleon fraction) so stored results stay reproducible. No rerun of B1–B3; the corrected pulls are recomputed by arithmetic in D1106.
