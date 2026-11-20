# PREREG_M4_CMBSPLIT — which part of the CMB prior drives the thread and the sign-switch gains? (locked D1706, 2026-11-20 01:40 UTC)
Same likelihood as PREREG_REALDATA_CMB, but the 3D CMB prior is replaced by its marginal pieces:
(A) θ* only (1D Gaussian, σ² = 0.006621e-9);
(B) (ω_b, ω_bc) only (2D block of the covariance).
For each: ΛCDM, the Weave thread (leading order) and ΛsCDM (z† ≤ 10). Report Δχ² versus ΛCDM within the same prior.
Reading: a model's gain is "θ*-driven" if its Δχ² under (A) is more negative than under (B) by more than 1, and "density-driven" if the reverse. The mirror question: do the thread and ΛsCDM tie for the SAME reason or for different reasons?
Script: field_tests/scripts/realdata/m4.py (background)
