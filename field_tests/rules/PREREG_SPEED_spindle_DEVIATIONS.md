# SPEED-Spindle DEVIATIONS (written before any rerun), 2026-11-23 ~09:12 CT
First run: S1 PASS (5.6e-16; 2.6x), S2 PASS (3.9e-10; 35x), S3 2 of 3 cases agree to 2e-8 / 1.8e-7 (case 2, rho0 = 0.3, phi = 0,
q = 1.5, does not oscillate: reference and analytic both return NaN) -> S3 FAILS as locked (the rule demanded all three), recorded;
the analytic period is offered as an option, not a replacement. S4 FAILED (0.14): eigsh with a random start vector can miss one
of a degenerate pair (the (5,5) spectrum has a doubly degenerate first excited level); a direct check gives identical values.
DEV-1: S4 fast path uses a fixed start vector, ncv = max(4k+1, 20), computes k+2 levels and keeps the lowest k. S4 rerun once.
No other test is rerun.

## Result after DEV-1 (no further reruns)
S4 still FAILS: worst 1.0 at (L,N,J,U) = (5,5,0,1), the J = 0 limit with a massively degenerate spectrum; a Lanczos start vector
cannot reveal degenerate multiplicities. Verdict: the sparse path is NOT accepted as a replacement. It is kept as an opt-in for
larger lattices (7x7: dim 1716 in 0.24 s; 8x8: dim 6435 in 4.4 s), labelled "levels may be missing when degenerate".
Accepted fast paths: S1 (vectorised SMA, 2.6x, 5.6e-16) and S2 (DOP853 mean field, 35x, 3.9e-10).
S3 analytic period: offered as an option (agrees to 2e-8 where an oscillation exists).
