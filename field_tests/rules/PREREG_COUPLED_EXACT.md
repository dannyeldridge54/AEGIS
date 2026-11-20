# PREREG_COUPLED_EXACT — the coupled thread with the EXACT perturbative curve and amp free to 5 (locked D1710, 2026-11-20 02:00 UTC)
Resolves D1708's flag (amp at its 0.9 bound). Shape: g(y) from PREREG_REALDATA_EXACT (never negative; floor at y² = c/3). Coupling as in PREREG_COUPLED_THREAD. amp ∈ [0.005, 5] (amp > 2.4 starts below the floor y² = c/3 = 0.912 ⇔ amp ≈ 8.0 at leading-order equivalence; capped at 5). Starts: D1708's best point and amp ∈ {0.5, 1.5, 3}.
Data: BAO + SN + CMB. Reading: the fix STANDS if Δχ²(exact, coupled) ≤ −9 with amp off its bound and |b_c| ≤ 0.1. Report w_eff at z = 0, 0.5, 1, 2.
Script: field_tests/scripts/realdata/coupled_exact.py (background)
