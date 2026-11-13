LOCKED 2026-11-13 (time = lock commit) by the development driver on Danny's word ("develop theory", 13:58 CT) under
STANDING_LOCK_AUTHORITY.md

# PREREG_TWISTL — TWIST-L, a rung-3 model with a logarithmic helper-field metric, and the only data allowed to test it

## Why it exists, stated plainly
The Twist's n_s (0.964–0.965) failed the locked NS-SPA test (D157). TWIST-P (locked 12:23) raises n_s by changing T's own kinetic
term, which takes it off the seven-disk ladder. TWIST-L was built AFTER seeing the same data, keeps T's geometry exactly (rung 3),
and instead lets the helper field's Kähler metric carry a logarithmic factor, as a loop or running-coupling correction would.
Its agreement with any data public at the lock time is worth nothing as evidence and is excluded from every reading.

## The model (theory/twistl/)
TWIST-K (D159) with S's metric multiplied by L(u) = 1 + b/(1 + ln(1 + 2/u)), u = T + T̄:
K = −3 ln(u − g E L SS̄ + ζ (E L)² (SS̄)²), W = √3 m S T. On the plateau V ≈ V₀(1 − b/ln(1/x)) = V₀(1 − b/(c|φ|)): a polynomial
(k = 1) approach in the canonical field while T's own geometry is untouched; on the tail L → 1 + b (dark energy unchanged).
One new parameter, b ≥ 0. Full SUGRA check at the CMB point (twistl_sugra_check.txt): S heavy (m_S²/H² 8–24 for b = 1–10), angle +4H².

## Locked predictions (kination +1.2 e-folds, heat 0.8%; twistl_scan.txt; loop shift negligible, D156)
| b | n_s | r |
|---|---|---|
| 0 (TWIST-K) | 0.9649 | 0.0036 |
| 1 | 0.9688 | 0.0048 |
| 2 | 0.9715 | 0.0061 |
| 3 | 0.9735 | 0.0073 |
| 5 | 0.9762 | 0.0095 |
| 10 | 0.9791 | 0.0140 |
The segment through these points (linear interpolation) is the prediction. r rises with n_s along a curve that differs from
TWIST-P's (at n_s = 0.971 TWIST-L needs r ≈ 0.006, TWIST-P r ≈ 0.011).

## Eligible data
Only CMB results whose n_s or r constraints are first made public after this lock commit (Simons Observatory, BICEP/Keck, SPT-3G
releases after the lock, LiteBIRD, CMB-S4, later ACT/Planck re-analyses). Everything public before the lock is excluded.

## Readings (first eligible joint n_s–r result; its published central values and errors, Gaussian)
d = smallest Mahalanobis distance from the published (n_s, r) to the locked segment.
- CONSISTENT d ≤ 2.45 (95% in two dimensions); TENSION 2.45 < d ≤ 3.44; DISFAVOURED d > 3.44.
- If only n_s is published: one-dimensional thresholds 2 / 3 against n_s 0.9649–0.9791.
- Kill clauses: r excluded below 0.0030 at 95% → DISFAVOURED. A result with n_s ≥ 0.972 at > 2σ AND r < 0.006 at 95% → DISFAVOURED.
- Versus TWIST-P: if both are scored on the same result, both readings are reported; neither is chosen after the fact.

## Not claimed
The size of b (b ≈ 2–5 would be needed for n_s ≈ 0.972–0.976) is not derived; a one-loop log correction of that size needs a
large multiplicity of fields. Stated as an open naturalness question.

## Failure handling
No changes after the lock; corrections only in PREREG_TWISTL_DEVIATIONS.md, written before any scoring.
