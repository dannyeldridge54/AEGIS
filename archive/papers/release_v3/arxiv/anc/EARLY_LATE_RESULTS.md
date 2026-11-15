# A3: early and late together (PREREGISTRATION_EARLY_LATE.md)

**Runs:** four AxiCLASS fits, finished 1 November 2026 between 06:29 and 06:57 CT.

**Data:** Planck low-ℓ + ACT DR6 + SPT-3G D1 lite + DESI DR2 + Pantheon+.

**A crash, and how the results were recovered:**
- The four fits converged, but the script crashed while writing its JSON summaries (a Cobaya `OnePoint` object has no
  `keys()`).
- Cobaya had already saved each minimum in `results/chains/cmp_<name>.minimum.txt`.
- The JSONs were rebuilt from those files with `early_late_spa.py save`. No fit was rerun or changed.
- The bug is logged in PREREGISTRATION_SPT3G_DEVIATIONS.md.

| Model | χ² | H₀ | σ8 | Early: f_EDE, θ_i | Late: w0, wa |
|---|---|---|---|---|---|
| ΛCDM | 2402.99 | 68.12 | 0.814 | — | — |
| Late only (w0–wa) | 2392.04 | 67.62 | 0.815 | — | −0.829, −0.644 |
| Early only (Locked Twist) | 2396.94 | 70.39 | 0.827 | 0.080, 2.717 | — |
| **Early + late** | **2388.39** | 69.40 | 0.828 | 0.069, 2.686 | −0.858, −0.477 |

## Verdict (rule applied as written)

- D = χ²(early + late) − χ²(late only) = 2388.39 − 2392.04 = **−3.65**.
- ΔAIC_early = D + 4 = **+0.35**.
- **Rule:** SURVIVES needs D < −4; NOT NEEDED means D ≥ −1. D = −3.65 lies in between, so the verdict is **MILD**.
  - Adding early energy still improves the fit by 3.65 once late dark energy is in.
  - That is not quite enough to pay for its two extra settings (AIC +0.35, close to a tie).

## Cross-checks (agree if within 1.0)

| Comparison | AxiCLASS | CAMB | Gap | Agree? |
|---|---|---|---|---|
| Early − ΛCDM | −6.05 | −5.63 | 0.42 | Yes |
| Late − ΛCDM | −10.95 | −10.89 | 0.06 | Yes |

The AxiCLASS early-only value (−6.05) also matches the A1 profile minimum (−5.98).

## Notes beside the verdict

- **The early signal is not absorbed by late dark energy.** f_EDE only drops from 0.080 to 0.069, and θ_i stays near
  2.7. The early and late signals are largely independent.
- **Adding early energy weakens the late signal:**
  - wa moves from −0.64 to −0.48 (towards 0);
  - w0 moves from −0.83 to −0.86 (towards −1).

  This is what Wang & Piao (2025) found.
- **H₀:** late only 67.6; early + late 69.4.
- **The A2 caveat still applies:** the early improvement sits at θ_i ≈ 2.7, so the local Δχ² overstates the global
  significance.
- **Overall:** the hint persists, and on its own it does not earn its place.
