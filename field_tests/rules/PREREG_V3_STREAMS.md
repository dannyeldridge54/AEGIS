# V3: does dark matter feel a force stars do not? (prediction on record, scored against published stream results)

**Status: LOCKED** on Danny's word (8 Nov 2026: "Go ahead. Get them ready then"). No published constraint was scored
and no stream data were analysed before the lock.

## Why this form
An own measurement would need N-body models of the Sagittarius stream to turn tail shapes into a force limit; the
Twist's effect is about ten times smaller than the best published bound. So the honest test is a frozen prediction,
scored mechanically when published stream analyses (Gaia DR4 era) report a limit or a detection. Our own Gaia download
(PC collector) continues as a cross-check and is reported, but it does not decide the verdict.

## Prediction (fixed now)
Fitted coupling across all current fits: β = 0.037–0.053 (Spiral 0.042–0.049, S8-J 0.037–0.042, S8-L 0.050–0.053).
Extra attraction between dark-matter particles, as a fraction of gravity: **2β² = 0.28–0.56%**, in the convention
m_c ∝ exp(β φ / M_P) with M_P the reduced Planck mass. Stars and gas feel no extra force (no baryon coupling).
Equivalent Kesden–Kamionkowski parameter (dark-matter force = (1 + β_KK²) × gravity): **β_KK = 0.053–0.075**.

## Gate (before any scoring)
Confirm from the coupled AxiCLASS source that `scf_coupling_beta` follows the convention above. If it does not, the
numbers are converted once, the conversion is logged, and the prediction is restated before any published value is
read.

## Scoring (mechanical)
For each published stream analysis that reports a constraint on a dark-matter-only fifth force (converted to β_KK with
the paper's own definition, conversion written down before reading its value):
- **FAIL** if it excludes β_KK ≥ 0.053 at 95% (the whole predicted range ruled out), or detects β_KK > 0.15 at ≥ 3σ
  (far too large for the Twist).
- **CONSISTENT** if its 95% range contains any of 0.053–0.075.
- **CANNOT TELL** if its bound is weaker than 0.075 (as for β_KK < 0.2, arXiv:0807.4363).
Every scored paper is listed, including those that cannot tell.

## Known now (not a verdict)
Published Sagittarius bound β_KK < 0.2 (arXiv:0807.4363): CANNOT TELL.

## Gate result (checked before the lock, 8 Nov)
`AxiCLASS_coupled_nlfix/source/background.c` line 448: ρ_cdm a³ ∝ exp(β (φ − φ_ini)); line 3273: Klein–Gordon source
−3 a² β ρ_cdm in CLASS units (8πG = 1, so φ is in reduced Planck masses). This is m_c ∝ exp(β φ / M_P): **convention
confirmed, no conversion needed.**
