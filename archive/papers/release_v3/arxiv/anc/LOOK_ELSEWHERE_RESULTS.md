# A2: look-elsewhere correction (PREREGISTRATION_LOOK_ELSEWHERE.md)

The eight fixed-angle combined fits finished by 1 November 2026, about 06:30 CT. Calculator: `look_elsewhere.py`
(Gross & Vitells 2010, 1 degree of freedom, half-χ² for the f ≥ 0 boundary).

| θ_i | q = χ²(ΛCDM) − χ²(θ) | f_EDE | H₀ |
|---|---|---|---|
| 0.5 | 0.00 | 0.023 | 68.83 |
| 1.0 | 0.43 | 0.022 | 68.87 |
| 1.5 | 0.09 | 0.020 | 68.65 |
| 2.0 | 0.34 | 0.034 | 69.15 |
| 2.4 | 1.65 | 0.058 | 69.75 |
| **2.7** | **5.64** | 0.075 | 70.29 |
| 2.741 (free) | 5.63 | 0.070 | 70.15 |
| 2.9 | 3.03 | 0.063 | 69.97 |
| 3.05 | 1.33 | 0.021 | 68.79 |

**Results:**
- **Local:** at the best angle, max q = 5.64, so p_local = 0.0088 and Z_local = 2.38.
- **Global**, with 1 upcrossing at both reference levels:
  - u₀ = 0.5: p = 0.085, Z = 1.37;
  - u₀ = 1.0: p = 0.107, **Z = 1.24 (the conservative value)**.

**Verdict (rule):** Z_global = 1.24, which is in the 1–2 band: **a weak hint.**

## Notes beside the verdict

- **The preference is confined to a narrow band of angles,** θ_i ≈ 2.4–3.0 near the hilltop. Elsewhere the data see
  nothing. Having had the freedom to pick that angle is what costs the significance.
- **The earlier figures were upper estimates,** as the reviewer said. "1.9σ" (χ²₂) and "2.4σ" (the A1 profile) shrink
  to about 1.2–1.4σ once the angle search is counted.
- **Caveats:** the method is asymptotic, N₀ comes from one realisation, and the 8-point grid is coarse. The A1 profile
  found the true minimum at f ≈ 0.08 (q = 5.98), which would raise Z_global only slightly (to about 1.3–1.5).
- **No fixed-angle run beat the free fit by more than 0.5.**
