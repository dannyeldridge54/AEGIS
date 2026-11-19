# PREREG KEFF2 — three-number reduction: (k_eff, τ*) with τ* = C·e(y*), the tilt fraction at horizon exit

Locked 2026-11-19 (08:55 CT) before computing. Follows D1517 (two-number (k, C) reduction failed on DILMIX: prefactor of e acts as tilt).
Chart: recompute the UCHART pure-power grid with engine F, recording y* and τ* = C·e(y*) per point; add k = 3.5 at C ∈ {0, 5e-7}
(B0 has k_eff 3.38). Same validity filter as PREREG_UCHART_DEVIATIONS D1.
Read-off for a model with (k_eff, τ*): on each chart row k, interpolate (n_s, r) linearly in τ* (τ* is monotone in C along a row);
then interpolate linearly in k between the two bracketing rows. Models: the five from PREREG_KEFF (S, A1, B0, M25, M50) using their
KEFF values of k_eff, y*, and τ* = C·e(y*) recomputed from their own e(y) (same script path), plus control U2.
Rule (unchanged from KEFF): "works" for a model if |Δn_s| ≤ 0.003 and |Δr|/r ≤ 20 % against its engine-F values and the in-band/out
status is right; "works" overall if all five pass. Expectation stated now: S, A1, M25, M50 pass; B0 passes if k = 3.5 row is valid.
If it works, the screen for any new route is (k_eff, τ*) → chart. No reruns to chase results; fixes only via PREREG_KEFF2_DEVIATIONS.md.
