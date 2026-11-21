# PREREG_RW10_DR3_TILT — forward tilt (β = 2√2, ζ(3) copy) vs mirror tilt (β′ = 4√2, ζ(5) copy) on data released after this lock
Locked 21 Nov 2026 before any DESI DR3 / Euclid cosmology release. AI-assisted. Scored only on post-lock data.

## Frozen now (from field_tests/results/rw5_zeta5.json, sha256 first 16 hex: 6febd28ea7124fbe)
- Forward: β = 2√2, DR2 best fit (Ω_m, amp) = (0.3049, 0.1739), χ² 1638.32 (Δ vs ΛCDM −7.01).
- Mirror: β′ = 4√2, DR2 best fit (Ω_m, amp) = (0.3061, 0.0780), χ² 1638.10 (Δ vs ΛCDM −7.22).
- A and the height norm do not enter at leading order (D1854 R0), so only the tilt is tested.

## Scoring (when DESI DR3 BAO, or a new SN compilation, is public)
Likelihood: the D1692 code path (field_tests/scripts/realdata/run.py) with the new data files substituted, no CMB.
1. Refit both one-parameter threads (Ω_m, amp) and ΛCDM. Δ_tilt = χ²(4√2) − χ²(2√2).
   - MIRROR PREFERRED if Δ_tilt ≤ −2; FORWARD PREFERRED if Δ_tilt ≥ +2; UNDECIDED otherwise.
2. Frozen-parameter check (no refit): χ² of each frozen DR2 point on the new data. Reported, not scored.
3. If either thread is worse than ΛCDM by Δχ² > +2 after refit, that thread is DISFAVOURED regardless of 1.
Thresholds will not be changed after the data appear; a scoring bug needs a DEVIATIONS file first.
Not duplicated: PREREG_DR3_FORECAST (thread vs CPL/ΛsCDM, forward tilt only) and PREREG_V1_DESI_DR3 (flagship).
