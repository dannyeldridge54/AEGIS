# Pre-registration: the one-setting Locked Twist (width = torsion ÷ 9) on SPT-3G

**Written:** 31 October 2026, before any SPT-3G fit of this model was run or looked at.
**Authors:** Danny Lee Eldridge, with Claude.
**Locking:** this file is SHA-256 hashed and git-committed at the time of writing, and must not be edited
afterwards. Any deviation goes in a separate, dated file.

## The prediction

The Locked Twist with every shape setting fixed in advance:

| Setting | Value | How it is fixed |
|---|---|---|
| Potential | V = Λ⁴ [1 − cos(d/F)]³ | as in all earlier fits |
| Switch-on | a_c = ω_r / (ω_b + ω_cdm), ω_r = 2.4728×10⁻⁵ (1 + 0.22711 N_eff) | matter–radiation equality (PREREGISTRATION_ZEQ.md) |
| Width | **F = 1.2247 / 9 = 0.13608 M_Pl** (N = 9) | committed here |
| Free extra setting | θ_i only (f_EDE follows from the potential height) | **1 extra setting over ΛCDM** |

**Where N = 9 comes from (disclosed):**
- It was read off the Planck free fit (1.2247 ÷ F = 8.97). It is not derived from physics.
- In the Cube Mind framework, 9 = 7 colours + 2 poles. That is a label, not a derivation, and it is not counted as
  evidence.
- Earlier results with N = 9 fixed:
  - Planck + DESI DR2 + Pantheon+: Δχ² −4.46, ΔAIC −2.46 (not blind)
  - P-ACT: Δχ² −6.14, ΔAIC −4.14, 2.5σ (blind for the width)
- On ACT the free width drifted to N ≈ 8.0. That is the main risk to this prediction.

## Data (new to this model)

**Primary test:** SPT-3G D1 TT/TE/EE (no Planck high-ℓ). Add:
- a τ prior from Planck low-ℓ EE;
- DESI DR2 BAO;
- Pantheon+.

No SH0ES.

**Secondary test:** the full SPT + Planck + ACT combination ("spa" in AEGIS), with DESI DR2 and Pantheon+. This shares
data with earlier fits, so it is reported, but it is not decisive.

## Method

- CAMB + Cobaya, the same settings as the P-ACT fits.
- ΛCDM and the one-setting Twist are polished the same way on the same data, with at least 4 restarts each.
- Δχ² is reported both likelihood-only and with priors (χ²_eff).

## Pass / fail (primary test only)

| Outcome | Rule |
|---|---|
| **PASS** | Δχ² < −2 **and** ΔAIC < 0 vs ΛCDM (the Twist-1 bar in PREREGISTRATION_ZEQ.md) |
| **FAIL** | Δχ² ≥ 0 (no improvement at all) |
| **INCONCLUSIVE** | −2 ≤ Δχ² < 0 |

**Width check** (free-width Locked Twist on the same primary data; implied N = 1.2247 / F):
- **Consistent:** N within 9 ± 1.
- **Inconsistent:** N outside 7–11.
- **Not decisive:** anywhere in between.

## Always reported beside the verdict

- H₀ for both models.
- The S8 penalty against DES Y3 + KiDS-1000 and against KiDS-Legacy, as in PREREG_S8.md.
- Any change of data, likelihood or settings from this file, with its reason.

## What each result would mean

- **PASS:** "With only one free setting, the Twist fits independent CMB data better than ΛCDM." This would be the
  first fully blind confirmation. It still would not show that torsion is the cause or explain why the number is 9.
- **FAIL:** "Fixing the width at 1/9 does not hold up on independent data." The N = 9 idea is dropped, and that is
  said publicly.
- **INCONCLUSIVE:** "SPT-3G cannot decide." Wait for Simons Observatory.
