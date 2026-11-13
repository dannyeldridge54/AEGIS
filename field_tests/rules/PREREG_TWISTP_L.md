LOCKED 2026-11-13 (time = lock commit) by the development driver on Danny's word ("work on both", 12:24 CT) under
STANDING_LOCK_AUTHORITY.md. Companion to PREREG_TWISTP.md (unchanged).

# PREREG_TWISTP_L — TWIST-P with a light angle

PREREG_TWISTP.md kept β ≤ 2.2×10⁻³ so the angle stays heavy, and left the light-angle range out until its isocurvature was
computed. D134 (results/isocurvature_check.txt) estimates the angle's isocurvature at S_B ≲ 2×10⁻¹⁰ (bound ~5×10⁻⁵), so the
range is allowed up to the S-stability limit. Same model, same Kähler potential, same exclusions: built after seeing the
current n_s data; everything public before this lock is excluded from scoring.

## Locked segment (kination +1.2, heat 0.8%; results/twistp_scan.txt)
| β | n_s | r |
|---|---|---|
| 4.6×10⁻³ | 0.9702 | 0.0064 |
| 1.0×10⁻² | 0.9709 | 0.0083 |
| 2.2×10⁻² | 0.9712 | 0.0112 |
β > 2.2×10⁻² excluded (S unstable by β ≈ 0.046). Loop shift +0.000…+0.003 on n_s. With PREREG_TWISTP the full TWIST-P family is
n_s 0.965–0.971 (+ loops ≤ 0.974), r 0.0036–0.011, r rising with n_s; its distinctive region (n_s ≥ 0.970) needs r ≥ 0.006.

## Readings (first eligible post-lock joint n_s–r result; as PREREG_TWISTP)
d = smallest Mahalanobis distance to the combined segment (both locks). CONSISTENT d ≤ 2; TENSION 2 < d ≤ 3; DISFAVOURED d > 3.
Additionally: if a post-lock result finds n_s ≥ 0.970 at > 2σ AND r < 0.005 at 95%, the whole TWIST-P family is DISFAVOURED.

## Failure handling
No changes after the lock; corrections only in PREREG_TWISTP_DEVIATIONS.md, written before any scoring.
