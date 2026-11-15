# SERAPIS — one-page prediction sheet (R6)

Frozen 15 Nov 2026; harmonised with the R8 referee fixes (R8b, D636/D637) (locks D605 τ=i, D615 ρ, D633 + addendum running; hashes in MANIFEST.md).
Scored only on data published after that date. ε is not retuned; any revision is a new model.
Labels: **computed** = from locked scripts (exact Mukhanov–Sasaki, D588); **estimate** = analytic/order-of-magnitude.

## Headline numbers
| Quantity | τ = i branch (Chronos) | ρ branch | Kairos (untilted, reference) | Label |
|---|---|---|---|---|
| n_s | 0.970–0.975 | 0.969–0.972 | 0.959–0.961 (D637, N* 46–49) | computed |
| r | (4.8–5.7)×10⁻⁴ | (4.6–5.1)×10⁻⁴ | (3.3–3.7)×10⁻⁴ (D637) | computed |
| α_s = dn_s/dln k (lock D633, N* 47–50; −(8.8–10.2)×10⁻⁴ at N* 46–49, D642) | −(8.6–9.9)×10⁻⁴ (lock D633; D605's −(3–5)×10⁻⁴ was an attractor estimate, superseded) | −(8.5–9.5)×10⁻⁴ | ≈ −2/N*² | computed |
| m_ν1 (Affleck–Dine LH_u, computed D646) | 2×10⁻¹³–9×10⁻¹¹ eV (T_R 1e3–1e5; thermal effects negligible, D653) → Σm_ν ≈ 0.0588 eV IF normal ordering (ordering is input from data, not predicted; lock D605 states NO) | same | — | estimate (D646/D646a) |
| f_NL^local / isocurvature | ≈ 0.01 / ~10⁻⁸ of ζ (D587; lock D605 said ≲10⁻¹⁰) | ≈ 0.01 | — | estimate/computed |
| Superpartners | covariant completion (adopted, D647–D650): m3/2 ~ (2.5–11)×10⁵ GeV, scalars ~ m3/2, wino LSP 0.66–2.9 TeV, gluino 4.7–21 TeV (estimates); constant-W0 chain (lock D605 P5): none below ~10⁸ GeV | same | — | estimate |
| Reheating | T_R 10³–10⁵ GeV, stiff phase w ≈ 0.55, N* 46–49 | w = 5/7 | — | computed/estimate |

## Parameter-free consistency relation (Janus, D635)
From n_s and r alone: ρ = 2√r/(1−n_s), x = (ρ−1)/(1+ρ/2), A = (1−n_s)/(1−x/2),
**α_s = −(A²/2)(1+x/4)(1+x)**. Accurate to 11–13 % against the exact numerics.
Offset-corrected (D640, c = ln1728/2π, u = 1/I*): 1−n_s = 8u²[(2−x)+cu(5−x)], r = 64u⁴(1+x)²(1+2cu), α_s = −32u⁴(1+x)[(4+x)+cu(23+2x)] — invert (n_s, r) → (u, x), predict α_s to ~2 % (0.2–0.4 % on the 8 test points).
A measured α_s outside this band (given measured n_s, r) rejects the whole family.

## Kill conditions (as in the locks; ≥3σ unless a CL is stated)
- r < 2.4×10⁻⁴ (τ = i, D605) / 2.3×10⁻⁴ (ρ, D615) at 95 % CL, or r detected > 1.1×10⁻³.
- n_s measured > 3σ outside the predicted band 0.969–0.975 (paper table wording).
- α_s > −3×10⁻⁴, or α_s violating the Janus relation (long term: needs σ(α_s) ~ 2×10⁻⁴).
- Σm_ν > 0.07 eV. (Lock D605 also lists inverted ordering; that tests the NO input, and with m_ν1 ≈ 0 IO already implies Σm_ν ≈ 0.10 eV.)
- |f_NL^local| > 5.
- Covariant completion: no wino up to 2.9 TeV and no gluino up to 21 TeV (FCC-hh reach), or a wino above 2.9 TeV overclosing; lock D605 P5 (constant W0): superpartners below 10⁸ GeV.

## Who tests what (rough reach figures; quote published forecasts in any external text)
| Experiment | Observable | Expected reach | What SERAPIS needs |
|---|---|---|---|
| Simons Observatory SATs | r | σ(r) ~ 2–3×10⁻³ | no detection (consistent) |
| BICEP/Keck + SPT-3G | r | σ(r) ~ 3×10⁻³ | no detection |
| LiteBIRD | r | σ(r) ≲ 10⁻³ (check current forecast) | no detection; r ≳ 10⁻³ detected rules it out |
| (CMB-S4 — DOE/NSF support ended 2025) / future σ(r) ~ 10⁻⁴ mission | r, α_s | not currently planned | r ≈ 5×10⁻⁴ at ~5σ |
| ACT/SPT/SO LAT + Planck | n_s, α_s | σ(n_s) ~ 0.002 | n_s ≈ 0.97 |
| DESI, Euclid | Σm_ν | σ ~ 0.02 eV | ≈ 0.059 eV |
| JUNO, DUNE, Hyper-K | ordering | NO vs IO at > 3σ | tests the NO input (not a model output) |
| 21-cm / SPHEREx | α_s, f_NL | σ(f_NL) ~ 1 | f_NL ≈ 0 |

## What is NOT predicted (stated limits)
- The size of ε (the tilt strength) is fitted to the low-T_R window, not derived; its microscopic origin is open (D620–D629).
- Superpartner window assumes the modular-covariant completion, X-independent gauge kinetic functions (anomaly-mediated gauginos) and initial conditions 6–12 e-folds before horizon exit, higgsino threshold (window ends ×2); dilaton–LSP bound disappears (winos re-thermalise, D652); gravitinos decay before BBN (D651); AD thermal effects negligible (D653); Weinberg operator non-zero at i with k_L = k_Hu = 1 (D654a); covariant completion: centre gives ordinary matter parity at ρ (D661) but not at τ = i with singlets (D663); dim-5 coefficients ≲ 5e-3 (D657).
- Preheating inefficient (q ≲ 2e-4 for m0 ≲ m_φ) and φ → gravitino + inflatino closed (m_inflatino = 4/3 m3/2) — estimates, D641. If either were efficient, N* would rise 6–9 e-folds and Chronos would leave its band.
- Collider signals: none expected at LHC/FCC energies.
