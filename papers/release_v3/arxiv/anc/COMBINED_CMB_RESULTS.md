# Results: all three CMB telescopes together (PREREGISTRATION_COMBINED_CMB.md)

**Data:** Planck (P-ACT cut) + ACT DR6 + SPT-3G D1 lite + ACT × Planck lensing + DESI DR2 + Pantheon+, no SH0ES.
**Source:** AEGIS `cmb-fit/results/cmp_spa_*.json`.

## 2026-10-31 ~20:30 CT: Test 2, late evolving dark energy (w0–wa): **PASS**

| Model | χ² | Δχ² | ΔAIC | H₀ | S8 | w0 | wa |
|---|---|---|---|---|---|---|---|
| ΛCDM (`spa_lcdm`) | 2402.40 | 0 | 0 | 68.17 | 0.817 | | |
| w0–wa (`spa_w0wa`) | 2391.51 | **−10.89** | **−6.89** | 67.65 | 0.829 | −0.837 | −0.619 |

**The rule:**
- Δχ² = −10.89 < −4 and ΔAIC = −6.89 < 0, so it is a **PASS**.
- With 2 extra settings, Δχ² = −10.89 corresponds to p ≈ 0.004, about 2.9σ.

**Where the improvement comes from (w0–wa − ΛCDM):**

| Data | Δχ² |
|---|---|
| DESI BAO | −3.53 |
| Pantheon+ | −2.19 |
| Planck low-ℓ EE | −2.06 |
| ACT DR6 | −1.58 |
| SPT-3G | −1.41 |
| ACT lensing | −0.26 |
| Planck low-ℓ TT | +0.22 |

Every data set except Planck low-ℓ TT moves the same way.

**Restart agreement:** all four minimiser restarts agree to within 0.14 in −log posterior for w0–wa, and to within 0.38
for ΛCDM.

**The forecast** (written in the pre-registration before running) was "INCONCLUSIVE or PASS, with w0 > −1 and
wa < 0":
- **Right:** w0 = −0.84 and wa = −0.62 are in the predicted direction, and the outcome is one of the two forecast.
- This agrees with the published picture: DESI DR2 with CMB and Pantheon+ at about 2.5–3σ.

**Notes beside the verdict:**
- Late dark energy **lowers** H₀ (67.65 against 68.17). It does not help the Hubble tension; it fits the shape of the
  expansion history better.
- The result depends on the supernova sample in the published work (DES Y5 gives more, Pantheon+ less). Only
  Pantheon+ was used here, as pre-registered.


## 2026-10-31 20:43 CT (result file time): Test 1, the Locked Twist on all three CMB telescopes: **PASS**

| Model | χ² | Δχ² | ΔAIC | H₀ | S8 | f_EDE | θ_i | z_c (locked) |
|---|---|---|---|---|---|---|---|---|
| ΛCDM (`spa_lcdm`) | 2402.40 | 0 | 0 | 68.17 | 0.817 | | | |
| Locked Twist (`spa_edelock`) | 2396.77 | **−5.63** | **−1.63** | 70.15 | 0.828 | 0.070 | 2.74 | 3534 |

**The rule:** Δχ² = −5.63 < −4 and ΔAIC = −1.63 < 0, so it is a **PASS**.
- With 2 extra settings, p ≈ 0.06, about 1.9σ.
- The restarts agree to within 0.30 in −log posterior.

**Where the improvement comes from (Twist − ΛCDM):**

| Data | Δχ² |
|---|---|
| Planck high-ℓ (cut) | −2.66 |
| Planck low-ℓ EE | −2.08 |
| ACT DR6 | −1.57 |
| DESI | −0.76 |
| Planck low-ℓ TT | −0.63 |
| ACT lensing | +0.19 |
| Pantheon+ | +0.33 |
| **SPT-3G** | **+1.55** |

SPT-3G still disfavours the Twist even inside the combination. The gain comes from Planck and ACT.

**Claude's forecast** (written before running) said INCONCLUSIVE, with f between 0.02 and 0.06 and H₀ between 68.8 and
69.8. **Wrong:** the result was a PASS, with f = 0.070 and H₀ = 70.15, slightly above both forecast ranges. The data
were kinder to the Twist than I predicted.

**Context:** the SPT-3G collaboration's own analysis of the same three CMB data sets gives f_EDE < 0.070 (95%), and
with DESI added, f differs from zero at only 1.2σ. Our best-fit f = 0.070 sits at their 95% edge. Best fits and
posteriors differ (prior-volume effects), so this is consistent, but it shows the preference is modest.

## Test 3, early vs late: **the data prefer late**

ΔAIC(Twist) = −1.63; ΔAIC(w0–wa) = −6.89. The late model is lower by **5.26** (more than 2), so the **data prefer late
evolving dark energy**.

**Forecast** ("no preference, or a slight preference for late"): half right. The preference for late is clear, not
slight.

## Plain summary

On all the data together, the Locked Twist now passes its own pre-registered rule, the first pass on independent CMB
data combined. But late evolving dark energy fits better still. SPT-3G on its own still pulls against the early burst.

## Deep search (PREREGISTRATION_DEEP_SEARCH.md): stopped

The runs `spa_lcdm_deep`, `spa_edelock_deep` and `spt_lcdm_deep` were stopped at 20:56 CT, at Danny's request, to focus
on plan step 3b. No results were read. `spt_edelock_F9_deep` was removed from the queue before it started. They can be
re-queued later.
