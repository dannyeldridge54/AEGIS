# TF: does the late Twist still fit with its decay constant fixed at a torsion-natural value? Pre-registration

**Locked:** 2026-11-02 14:51:28 (time from Get-Date). Danny: "ok" to the plan in NEXT_MODELS_DESIGN.md (committed 14:48, which
declared the two values before this rule).

## The two candidate values (declared before any fit)

| Label | F (M_Pl) | log₁₀ F | Origin |
|---|---|---|---|
| F₁ | √(3/2) = 1.2247 | 0.0880 | torsion-generated kinetic term, angle of period 2π |
| F₂ | √6 = 2.4495 | 0.3891 | Nieh–Yan-enhanced decay constant with M = M_Pl (Adshead, Brahma & Das 2026) |

## Honesty note (what is already known)

- The free (F, m) grid already exists for Pantheon+ and DES Y5. **For Pantheon+, F₂ is 0.011 dex from the grid best
  (log₁₀ F = 0.4)**, so its Pantheon+ result is essentially known in advance.
- DES Y5 grid points at log₁₀ F = 0, 0.2 and 0.4 are known too.
- This is therefore **a consistency test on already-profiled data**: can a derived F replace a fitted one? It is
  not a blind test.
- **The blind part is Union3**, where only one late-field point (from LU) is being fitted now.

## Runs (corrected code, `_nlfix`; F fixed via `_fF<log10 F>`, m free on the prior −0.5 ≤ log₁₀ m ≤ 1.5; best of 4)

| SN sample | F₁ run | F₂ run | ΛCDM reference |
|---|---|---|---|
| DES Y5 | ax_spa_latetwist_fF0.0880_desy5_nlfix | ax_spa_latetwist_fF0.3891_desy5_nlfix | ax_spa_lcdm_halofit_desy5 |
| Pantheon+ | ax_spa_latetwist_fF0.0880_nlfix | ax_spa_latetwist_fF0.3891_nlfix | ax_spa_lcdm_halofit |
| Union3 | ax_spa_latetwist_fF0.0880_union3_nlfix | ax_spa_latetwist_fF0.3891_union3_nlfix | ax_spa_lcdm_halofit_union3 |

## Rule

- **Measures, for each F value and each SN sample:**
  - D_F = χ²(F fixed, m free) − χ²(best free fit on that sample). The best free fit is the lowest χ² among the grid,
    the edge points and the F-fixed runs. For Union3 it is the lowest of the LU point and the two F-fixed runs.
  - G_F = χ²(F fixed, m free) − χ²(ΛCDM reference).
- **Verdict per F value**, on DES Y5 (the sample with the late-field signal):
  - **SUPPORTED** if D_F ≤ 1 and G_F ≤ −4: a derived F loses nothing and still beats ΛCDM.
  - **CONSISTENT** if D_F ≤ 1 but G_F > −4.
  - **DISFAVOURED** if 1 < D_F ≤ 4.
  - **EXCLUDED** if D_F > 4.
- **Also reported:** Pantheon+ and Union3 D_F and G_F, for information.
- **Look-elsewhere:** two F values were tested. "At least one SUPPORTED" is reported together with that count. No third
  value is added after seeing these results.
- **A failed or non-finite run** counts as EXCLUDED for that F (code-limited) and is not retried with new settings.

## Expectation (logged before running; not a rule)

- **DES Y5:** F₁ CONSISTENT or SUPPORTED (the DES Y5 grid best is at F = 1.0, close to 1.22). F₂ CONSISTENT
  (grid points near log₁₀ F = 0.4 are somewhat worse on DES Y5).
- **Pantheon+:** both near a tie with ΛCDM.
- **Union3:** unknown (the blind part).
