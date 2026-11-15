# SERAPIS — one-page prediction sheet (R6)

Frozen 15 Nov 2026 (locks D605 τ=i, D615 ρ, D633 + addendum running; hashes in MANIFEST.md).
Scored only on data published after that date. ε is not retuned; any revision is a new model.
Labels: **computed** = from locked scripts (exact Mukhanov–Sasaki, D588); **estimate** = analytic/order-of-magnitude.

## Headline numbers
| Quantity | τ = i branch (Chronos) | ρ branch | Kairos (untilted, reference) | Label |
|---|---|---|---|---|
| n_s | 0.970–0.975 | 0.969–0.972 | 0.961–0.963 | computed |
| r | (4.8–5.7)×10⁻⁴ | (4.6–5.1)×10⁻⁴ | (3.0–3.3)×10⁻⁴ | computed |
| α_s = dn_s/dln k | −(8.6–9.9)×10⁻⁴ | −(8.5–9.5)×10⁻⁴ | ≈ −2/N*² | computed |
| Σm_ν (Affleck–Dine LH_u) | 0.059–0.060 eV, normal ordering, m_ν1 ≲ 10⁻⁸ eV | same | — | estimate |
| f_NL^local | ≈ 0.01 | ≈ 0.01 | — | estimate |
| Superpartners | none below ~10⁸ GeV (soft masses ~10⁹ GeV) | same | — | estimate |
| Reheating | T_R 10³–10⁵ GeV, stiff phase w ≈ 0.55, N* 46–49 | w = 5/7 | — | computed/estimate |

## Parameter-free consistency relation (Janus, D635)
From n_s and r alone: ρ = 2√r/(1−n_s), x = (ρ−1)/(1+ρ/2), A = (1−n_s)/(1−x/2),
**α_s = −(A²/2)(1+x/4)(1+x)**. Accurate to 11–13 % against the exact numerics.
A measured α_s outside this band (given measured n_s, r) rejects the whole family.

## Kill conditions (each disfavours SERAPIS at ≥3σ)
- r < 2.3×10⁻⁴ at 95 % CL, or r > 10⁻³ detected.
- n_s outside 0.966–0.978 at > 3σ.
- α_s > −3×10⁻⁴, or α_s violating the Janus relation.
- Σm_ν > 0.07 eV, or inverted ordering established.
- |f_NL^local| > 5.
- Superpartners found below 10⁸ GeV.

## Who tests what, and when (estimates of reach; check against each collaboration's current forecasts before citing)
| Experiment | Observable | Expected reach | What SERAPIS needs |
|---|---|---|---|
| Simons Observatory SATs | r | σ(r) ~ 2–3×10⁻³ | no detection (consistent) |
| BICEP/Keck + SPT-3G | r | σ(r) ~ 3×10⁻³ | no detection |
| LiteBIRD | r | σ(r) ≲ 10⁻³ | hint at r ~ 5×10⁻⁴ |
| CMB-S4-class / SO upgrades | r, α_s | σ(r) ~ 10⁻⁴ | r ≈ 5×10⁻⁴ at ~5σ |
| ACT/SPT/SO LAT + Planck | n_s, α_s | σ(n_s) ~ 0.002 | n_s ≈ 0.97 |
| DESI, Euclid | Σm_ν | σ ~ 0.02 eV | ≈ 0.059 eV |
| JUNO, DUNE, Hyper-K | ordering | NO vs IO at > 3σ | normal ordering |
| 21-cm / SPHEREx | α_s, f_NL | σ(f_NL) ~ 1 | f_NL ≈ 0 |

## What is NOT predicted (stated limits)
- The size of ε (the tilt strength) is fitted to the low-T_R window, not derived; its microscopic origin is open (D620–D629).
- Sequestering of the visible sector is assumed.
- Collider signals: none expected at LHC/FCC energies.
