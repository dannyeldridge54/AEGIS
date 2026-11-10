# DESI-MOCK: would a DESI-style analysis of a flagship universe "discover" evolving dark energy?

**Status: LOCKED** on Danny's word ("Get papers ready and start next steps", 10 Nov 2026, 17:45 CT). The next step
proposed to him beforehand was this test. AI-assisted. No mock fit exists at lock.

**Not blind.** Known at writing:
- FLAG-1's effective w0 ≈ −0.85, wa ≈ −0.33 (`field_tests/desi_w0wa/flagship_w0wa.json`), from a direct conversion.
- DESI DR2 + CMB + Pantheon+: w0 = −0.838 ± 0.055, wa = −0.62 ± 0.21, about 2.8σ.

This test asks a sharper question than the conversion: what the DESI-style **fit** recovers, and how strongly.

## Truth
The FLAG-1 Pantheon+ best fit (`cmp_ax_spa_spiraltwist_kappa1_nlfix_s8y6`), computed with its own build. From it:
- DESI DR2 BAO observables at the DR2 redshifts and quantities;
- Pantheon+ distance moduli (any M);
- a compressed CMB vector: 100θ*, ω_b and ω_bc,early. The CDM density used is the one the CMB sees, ρ_cdm(z = 1090)
  scaled to today as a⁻³, because the coupled CDM density is not constant.

## Mock
Noiseless ("Asimov") data at the truth, with the real covariances:
- DESI DR2 BAO: the ALL covariance;
- Pantheon+: STAT+SYS, z > 0.01, non-calibrators, M marginalised analytically;
- CMB compressed: σ = 0.00030 / 0.00015 / 0.0011, uncorrelated.
The Asimov Δχ² is the expected significance for the real errors.

## Fits (DESI convention: uncoupled CDM, plain CLASS build)
- **ΛCDM**: h, ω_b, ω_c.
- **w0waCDM**: the same plus w0 ∈ [−3, 1], wa ∈ [−3, 2] (PPF).
- Nelder–Mead from three starts; the lowest χ² counts.

## Readings
Δχ² = χ²(ΛCDM) − χ²(w0wa) on the mock; the significance is from χ² with 2 degrees of freedom.
- **REPRODUCES DESI'S SIGNAL**: significance ≥ 2σ, recovered wa < 0 and w0 > −1 (a crossing in the fitted form).
- **PARTIAL**: significance 1–2σ with the same signs.
- **DOES NOT**: anything else.
- Reported: recovered (w0, wa), their distance from DESI DR2 + CMB + Pantheon+ (one parameter at a time), and
  significance with BAO + CMB only (without SNe).

## What may not happen
No change of truth, data vectors, covariances, priors or thresholds after any result. No second truth (Dovekie or
Union3 best fit) to chase a reading; those may be run afterwards as reported extras, clearly marked. Counted +1 in V7.

## Code
`field_tests/desi_mock/desi_mock.py` (cloud).
