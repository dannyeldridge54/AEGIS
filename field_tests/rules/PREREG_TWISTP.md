LOCKED 2026-11-13 (time = lock commit) by the development driver on Danny's word ("make another model if it's new and not
tested", 12:21 CT) under STANDING_LOCK_AUTHORITY.md

# PREREG_TWISTP — a new model, TWIST-P, and the only data allowed to test it

## Why it exists, stated plainly
The Twist (v5) predicts n_s ≈ 0.965; Planck + ACT DR6 + SPT-3G + DESI prefer ≈ 0.973–0.975 (D131). The Twist cannot raise
n_s inside itself (D132). TWIST-P was built AFTER seeing that data, to address it. Its agreement with any data public at the
lock time is therefore worth nothing as evidence, and is excluded from every reading below.

## The model (theory/twistp/)
Same superpotential as the Twist v5, W = √3 m S T exp(−n(1 − e^{−πT/4})), n ≈ 125, and a new Kähler potential
K = −3 ln(u − e^{β/u} g SS̄ + ζ e^{2β/u} (SS̄)²) + β/u,   u = T + T̄, g = 1 + u/2μ, μ = 1, ζ = 3×10⁴.
The extra pole-order-3 term β/u changes only the inflaton's kinetic term deep on the plateau (a polynomial attractor there);
V along real T is identical to the Twist's (checked to 10⁻⁶ in full SUGRA); the tail, dark energy, matter and dark-matter
sectors are unchanged. One new parameter, β.

## Allowed range of β (fixed by the model's own consistency, not by data)
The angle must stay heavy at the CMB point (m_y² > 9/4 H², so it makes no isocurvature) and S must stay heavy:
β ≤ 2.2×10⁻³ (results/twistp_scan.txt). β ≥ 0 (β = 0 is the Twist).

## Locked predictions (kination +1.2 e-folds, heat 0.8%; twistp_scan.txt)
| β | n_s | r |
|---|---|---|
| 0 (Twist) | 0.9649 | 0.0036 |
| 1.0×10⁻⁴ | 0.9652 | 0.0036 |
| 4.6×10⁻⁴ | 0.9667 | 0.0039 |
| 1.0×10⁻³ | 0.9679 | 0.0044 |
| 2.2×10⁻³ | 0.9691 | 0.0052 |
Plus the D77 loop shift +0.000…+0.003 on n_s. So TWIST-P lives on the segment n_s 0.965–0.972, r 0.0036–0.0052, with r rising
as n_s rises. Late universe: identical to PURE-TWIST (w0 −0.90, wa −0.14) — already locked in PREREG_WATCH_PURE_DR3.

## Eligible data
Only CMB results whose n_s or r constraints are first made public after this lock commit (e.g. Simons Observatory,
BICEP/Keck or SPT-3G releases after the lock, LiteBIRD, CMB-S4, a later ACT/Planck re-analysis). Everything public before the
lock — including P-ACT, P-ACT-LB, CMB-SPA and their DESI combinations — is excluded.

## Readings (on the first eligible joint n_s–r result; its own published central values and errors, Gaussian)
Distance d = the smallest Mahalanobis distance from the published (n_s, r) to the locked segment (loop band included).
- **CONSISTENT** if d ≤ 2.
- **TENSION** if 2 < d ≤ 3.
- **DISFAVOURED** if d > 3.
If only n_s is published: same thresholds on n_s alone against 0.965–0.972. If r is detected with r > 0.010 at > 3σ, or
excluded below 0.0030 at 95%, TWIST-P (and the Twist) is DISFAVOURED regardless.

## Not claimed
TWIST-P does not reach n_s = 0.974: its ceiling inside the allowed β is ≈ 0.969 (+ loops ≤ 0.972). A light-angle extension
(β up to ~0.02, n_s ≤ 0.9713, r ≤ 0.011) needs an isocurvature calculation that has not been done and is not part of this lock.

## Failure handling
No changes after the lock; corrections only in PREREG_TWISTP_DEVIATIONS.md, written before any scoring.
