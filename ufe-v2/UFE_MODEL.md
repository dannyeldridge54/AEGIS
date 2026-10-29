# The UFE model: torsion-born early dark energy with a locked switch-on
*Danny Lee Eldridge · 29 October 2026 · every number from the saved fits in cmb-fit/results*

## Components (flat space)
H²(a) = (8πG/3) [ ρ_r(a) + ρ_m(a) + ρ_φ(a) + ρ_Λ ]
- **Radiation:** ρ_r ∝ a⁻⁴, with ω_r = 2.4728×10⁻⁵ (1 + 0.22711 N_eff), N_eff = 3.044.
- **Matter:** ρ_m ∝ a⁻³, with ω_m = ω_b + ω_c.
- **The field (the Twist):** φ = √(3/2) M_Pl arsinh(1/γ), V(φ) = Λ⁴ [1 − cos(φ/F)]³ (n = 3). Fluid form after release:
  ρ_φ(a) = 2 ρ_φ(a_c) / [ (a/a_c)^{9/2} + 1 ], with ⟨w⟩ = (n − 1)/(n + 1) = 1/2.

## The lock
The field is released at matter–radiation equality, a_c = a_eq = ω_r / ω_m, which removes z_c as a free setting.
Best fit: z ≈ 3,560 (Planck 2018 + DESI DR2 + Pantheon+).

## Fitted values (Locked Twist)
| quantity | Planck 2018 + DESI DR2 + Pantheon+ | P-ACT (blind) |
|---|---|---|
| f_EDE (at release) | 0.078 | 0.075 |
| θ_i | 2.77 rad | 2.71 rad |
| H₀ (km/s/Mpc) | 70.53 | 70.43 |
| 100 θ* | 1.0408 | — |
| Δχ² vs ΛCDM (same data, same polish) | −4.70 | −7.23 |
| ΔAIC (2 extra settings) | −0.70 | −3.23 |

## The width module
- With the width fixed at F = √(3/2) M_Pl / 9 = 0.1361 M_Pl, one free setting remains (θ_i). Results:
  Δχ² −4.46 (ΔAIC −2.46) on Planck; Δχ² −6.14 (ΔAIC −4.14, p = 0.013) on the blind P-ACT data.
- Fitted freely, the width gives N = 8.5 (Planck, CAMB) and 8.0 (P-ACT), so the "9" is not yet derived.

## Mechanism (why H₀ rises)
- The field adds energy just before recombination and shrinks the sound horizon (r_s 144.9 → 140.7 Mpc, −2.9%).
- The CMB fixes the angle θ* = r_s / D_M, so D_M shrinks by the same fraction and H₀ rises.
- The acoustic peak positions (ℓ = 220, 536, 813, 1127, 1421, 1727, 2011) are unchanged; their mean spacing
  (298.5) matches ℓ_A = π/θ* ≈ 301.8.

## Status
| test | result |
|---|---|
| Blind P-ACT (rule written first: Δχ² < −4) | passed |
| Fair Planck; three supernova sets (DES Y5, DES-Dovekie, Union3) | passed (−4.70; −4.55 / −5.08 / −4.91) |
| Weak lensing S8 (penalty limit 2) | +2.41 vs DES Y3 + KiDS-1000 (over); +0.39 vs KiDS-Legacy → **verdict: tie** |
| Field must start near its hilltop | required (Δχ² +4 to +6 for distant starts) |
| Pure torsion width F = √(3/2) M_Pl | failed (Δχ² +13.8) |
| Origin of the 1/9 width and of the lock | open (hypotheses/HOLD_RELEASE.md) |
