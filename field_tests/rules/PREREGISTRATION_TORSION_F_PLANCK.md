# TF-P: the derived Planck-length value F = (4/π)√(3/2) M_Pl. Pre-registration (addendum to TF)

**Locked:** 2026-11-02 14:55:36 (time from Get-Date). Written after TF (locked 14:51:28) and **before any TF fit has finished**:
0 F-fixed results exist at lock time.

**Why a third value:** TF's two values were heuristic. NIEH_YAN_PERIOD.md (`nieh_yan_period.py`) then derived the
period of the Twist angle from the Nieh–Yan index. With the Nieh–Yan length equal to the Planck length √G and minimal
charge ν = 1, it gives **F_P = (4/π)√(3/2) M_Pl = 1.5594 M_Pl** (log₁₀ F = 0.1930). This is the principled value; F₁
and F₂ stay as locked.

## Runs (same settings as TF: `_nlfix`, F fixed via `_fF`, m free, best of 4)

| SN sample | Run |
|---|---|
| DES Y5 | ax_spa_latetwist_fF0.1930_desy5_nlfix |
| Pantheon+ | ax_spa_latetwist_fF0.1930_nlfix |
| Union3 | ax_spa_latetwist_fF0.1930_union3_nlfix |

## Rule

- **Thresholds:** identical to TF (D_F, G_F; SUPPORTED, CONSISTENT, DISFAVOURED or EXCLUDED, judged on DES Y5).
- **Look-elsewhere:** **three** F values have now been declared in total (F₁, F₂, F_P). Any "SUPPORTED" is reported
  with that count.
- **Honesty note:** the DES Y5 and Pantheon+ grids include log₁₀ F = 0.2, which is 0.007 dex from F_P, so those two
  results are close to known. **Union3 is the blind part.**
- **Assumptions behind F_P** (any one failing changes the number):
  1. the Mercuri–Taveras coupling (1/2κ)β·N;
  2. Pontryagin integrals quantised in units of 8π² with minimal difference ν = 1;
  3. the angle is genuinely periodic, which requires an instanton-generated periodic potential;
  4. the Nieh–Yan length equals the Planck length √G.
