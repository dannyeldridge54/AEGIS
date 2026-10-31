# SPT-3G results for the pre-registered predictions (logged as each one is decided)

Data and settings: PREREGISTRATION_SPT3G_N9.md, with the deviations in PREREGISTRATION_SPT3G_DEVIATIONS.md:
- SPT-3G D1 TT/TE/EE lite
- τ ~ N(0.051, 0.006)
- DESI DR2 + Pantheon+, no SH0ES

Source files: `cmb-fit/results/cmp_spt_*.json` (AEGIS).

## 2026-10-31 ~14:45 CT: N = 9 prediction (DOI 10.5281/zenodo.23838969): **FAIL**

| Model | χ² | H₀ | f_EDE | θ_i |
|---|---|---|---|---|
| ΛCDM (`spt_lcdm`) | 1576.57 | 68.28 | | |
| N = 9 Twist, 1 setting (`spt_edelock_F9`) | 1577.09 | 70.49 | 0.077 | 2.787 |

**The rule:**
- Δχ² = χ²(Twist) − χ²(width constraint, 0.001) − χ²(ΛCDM) = **+0.52**.
- ΔAIC = Δχ² + 2 = **+2.52**.
- PASS needed Δχ² < −2 and ΔAIC < 0. FAIL is Δχ² ≥ 0. **FAIL.**

**By data set (Twist − ΛCDM):** SPT-3G +0.44, DESI −0.27, Pantheon+ +0.34. SPT-3G's CMB data do not prefer the
Twist.

**Notes beside the verdict (not part of it):**
- **A ceiling on any re-fit.** The N = 9 Twist contains ΛCDM as a limit: a small starting angle switches the early
  energy off. So a perfect minimisation could at best bring Δχ² to about 0.
  - The +0.52 means the fitter stayed near the Planck/ACT-like point (f_EDE 0.077, θ_i 2.79) where it started.
  - A deeper search could lower Δχ² to about 0, but under the rule that is still FAIL (Δχ² ≥ 0). Passing would need
    a new early-energy minimum below −2, which this fit gives no sign of.
- **How it compares with earlier data:** the N = 9 Twist improved P-ACT by −6.14 and Planck by −4.46. On the first
  fully independent CMB data set it gives no improvement.
- **The silver angle check** (from PREREGISTRATION_SPT3G_SILVER.md; the zero-setting silver fit itself is still
  running): best-fit θ_i on SPT-3G is 2.787, which is |2.787 − 2.414| = 0.373 rad from the silver ratio. That is
  beyond 0.35, so the angle check is **inconsistent**.

**What this means:** the one-setting N = 9 Twist did not pass on independent data. As the pre-registration says, the
N = 9 idea is dropped publicly. The 2-setting Locked Twist is judged separately: the width check and the free-width
fit (`spt_edelock`) are still queued.

## 2026-10-31 ~16:05 CT: silver-ratio prediction (DOI 10.5281/zenodo.23839507): **FAIL**

| Model | χ² | H₀ | f_EDE | θ_i |
|---|---|---|---|---|
| ΛCDM (`spt_lcdm`) | 1576.57 | 68.28 | | |
| Zero-setting Twist (`spt_edelock_th2.41421_F9`) | 1577.00 | 69.13 | 0.035 | 2.414 (fixed) |

**The rule:**
- Δχ² = 1577.0014 − 0.0002 (width constraint) − 1576.5702 = **+0.43**.
- Zero extra settings, so ΔAIC = Δχ² = **+0.43**.
- PASS needed Δχ² < −2. FAIL is Δχ² ≥ 0. **FAIL.**
- The angle check was already **inconsistent** (0.373 rad, above).

**By data set (Twist − ΛCDM):** SPT-3G +0.26, DESI +0.15, Pantheon+ +0.02.

**Reported beside the verdict (PREREG_S8.md):**
- S8: 0.815 (Twist) vs 0.803 (ΛCDM).
- Penalty against DES+KiDS (A) is +1.39; against KiDS-Legacy (B) it is −0.33. The S8 verdict depends on which survey is
  right.
- The Planck-angle contrast (`spt_edelock_th2.78_F9`, not a prediction): Δχ² +0.35 (see the next entry).

**What this means (silver):** as the pre-registration says, the silver-ratio mapping is dropped publicly. The Tree's 1 ± √2
modes remain an exact piece of graph mathematics, but they do not set the field's starting angle. The Locked Twist
itself never depended on this number.

## 2026-10-31 ~17:05 CT: free-width Locked Twist on SPT-3G (`spt_edelock`), and what it decides

| Model | χ² | Δχ² vs ΛCDM | H₀ | f_EDE | θ_i | implied N |
|---|---|---|---|---|---|---|
| ΛCDM (`spt_lcdm`) | 1576.57 | 0 | 68.28 | | | |
| Locked Twist, width free (2 settings) | 1575.30 | **−1.27** | 69.60 | 0.0449 | **3.10** (prior edge) | **24.05** |
| N = 9, θ_i = 2.78 fixed (`spt_edelock_th2.78_F9`), NOT a prediction | 1576.92 | +0.35 | 70.43 | 0.076 | 2.78 | 9 |

**By data set (free width − ΛCDM):** SPT-3G −1.28, DESI −0.23, Pantheon+ +0.24.

### Verdicts (pre-registered rules applied as written)

| Test | Rule | Result | Verdict |
|---|---|---|---|
| **Letters** (PREREGISTRATION_SPT3G_LETTERS.md) | PASS if \|f − 0.0154\| < 0.015; FAIL if > 0.04 | \|0.0449 − 0.0154\| = 0.0295 | **INCONCLUSIVE** |
| **Width check for N = 9** (PREREGISTRATION_SPT3G_N9.md) | consistent if N in 8–10; inconsistent outside 7–11 | N = 24.05 | **INCONSISTENT** |
| **Torus Test B, N = 7** (PREREGISTRATION_SPT3G_TORUS.md) | consistent if N in 6–8; inconsistent outside 5–9 | N = 24.05 | **INCONSISTENT** |
| Torus Test A (N = 7 fit) | Δχ² < −2 and ΔAIC < 0 | still running | pending |

**The free-width model itself** (descriptive; the P-ACT rule, Δχ² < −4 and ΔAIC < 0, quoted only for context):
Δχ² = −1.27, ΔAIC = −1.27 + 4 = **+2.73**. SPT-3G does not prefer the Locked Twist. On P-ACT the same model gave
−7.23.

### Notes beside the verdicts (not part of them)

- **The fit ran to the edge of its prior.** θ_i = 3.10 is the prior maximum (`cmbfit.py`: 0.1–3.1), right next to the
  hilltop at π. With the width free, SPT-3G pushes the field towards a narrow (N ≈ 24, F = 0.051 M_Pl), nearly
  balanced-on-the-hilltop start with a small energy share (4.5%). The true minimum may lie beyond the prior edge.
- **Fragmentation risk is higher there.** The stability check (STABILITY_FIRST_PASS.md) covered θ_i ≤ 3.0 at N = 9;
  growth rises steeply towards π. The linear fits are least trustworthy at this point. A width this far from 9 also
  leaves the earlier stability numbers untested.
- **The improvement is small.** −1.27 with two extra settings is what fitting noise alone would often give, so
  nothing here should be read as a hint either way. SPT-3G simply does not see the early energy that Planck and ACT
  lean towards.
- **The letters number** sits closer to this fit (0.045) than the Planck/ACT values (0.074–0.086) suggested, but
  still 0.03 away: inconclusive, as the rule says.
- **The 2.78 contrast** (Planck-preferred angle with N = 9, not a prediction) also fails to improve on ΛCDM (+0.35).

**What this means:** on the first fully independent CMB data, every tested version of the Locked Twist fits no better
than ΛCDM: N = 9 (+0.52), the silver angle (+0.43), the Planck angle (+0.35) and the free width (−1.27, ΔAIC +2.73).
The Planck/ACT preference is not confirmed by SPT-3G. The N = 9 and N = 7 width ideas are both inconsistent with
SPT-3G's preferred width. The letters prediction is undecided.
