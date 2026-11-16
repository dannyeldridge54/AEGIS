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
| β_s = d²n_s/dln k² (lock D667) | −(3.0–4.6)×10⁻⁵ | same | −4/N*³ | computed |
| f_NL^local / isocurvature | ≈ 0.01 / ~10⁻⁸ of ζ (D587; lock D605 said ≲10⁻¹⁰) | ≈ 0.01 | — | estimate/computed |
| Superpartners | covariant completion (adopted, D647–D650): m3/2 ~ (2.5–11)×10⁵ GeV, scalars ~ m3/2, wino LSP 0.66–2.9 TeV, gluino 4.7–21 TeV (estimates; Fermi-LAT 2507.15934 excludes winos 1.85–2.86 TeV and thermal wino DM ⇒ surviving wino 0.66–1.85 TeV, m3/2 ≈ (2.5–7)×10⁵ GeV, extra DM component needed, D713); SERAPIS-E at ρ with fast reheating (D725–D735, estimates): gravitino→wino plus H.E.S.S. line limit narrow this to wino 0.66–0.8 TeV (Einasto; any mass for kpc cores), ~15% of DM, heavy neutrinos ~1e12 GeV; constant-W0 chain (lock D605 P5): none below ~10⁸ GeV | same | — | estimate |
| SERAPIS-E (derived branch, lock D693, post-hoc) | n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4; Janus κ=1 (p=2√2) ≤6%; N* 48.4–49.9 | — | — | computed |
| Reheating | T_R 10³–10⁵ GeV, stiff phase w ≈ 0.55, N* 46–49 | w = 5/7 | — | computed/estimate |

## Parameter-free consistency relation (Janus, D635)
From n_s and r alone: ρ = 2√r/(1−n_s), x = (ρ−1)/(1+ρ/2), A = (1−n_s)/(1−x/2),
**α_s = −(A²/2)(1+x/4)(1+x)**. Accurate to 11–13 % against the exact numerics.
Offset-corrected (D640, c = ln1728/2π, u = 1/I*): 1−n_s = 8u²[(2−x)+cu(5−x)], r = 64u⁴(1+x)²(1+2cu), α_s = −32u⁴(1+x)[(4+x)+cu(23+2x)] — invert (n_s, r) → (u, x), predict α_s to ~2 % (0.2–0.4 % on the 8 test points); the same relation fits ρ to 1 % (D666). β_s ≈ 128u⁶(1+x)(2x² − 5x − 16) (D666, lock D667).
A measured α_s outside this band (given measured n_s, r) rejects the whole family.

## Kill conditions (as in the locks; ≥3σ unless a CL is stated)
- r < 2.4×10⁻⁴ (τ = i, D605) / 2.3×10⁻⁴ (ρ, D615) at 95 % CL, or r detected > 1.1×10⁻³.
- n_s measured > 3σ outside the predicted band 0.969–0.975 (paper table wording).
- Strip (lock D679, exact D678): joint (n_s, r) off the band r ≈ (4.4–5.3)×10⁻⁴ at n_s = 0.970 (width ≤ 21% at fixed n_s; edge formulas in the lock) excludes the τ = i family; ρ strip identical within 2.2% (D680, lock D681 for both vacua).
- Family-wide, any ε, both vacua (locks D675, D677; exact D674, D676): n_s > 0.985 or r > 8.3×10⁻⁴ at ≥3σ excludes home-safe SERAPIS (caps: τ = i 0.9836 / 8.2e-4, ρ 0.9844 / 8.3e-4).
- α_s > −3×10⁻⁴, or α_s violating the Janus relation (long term: needs σ(α_s) ~ 1×10⁻⁴, D670).
- Σm_ν > 0.07 eV. (Lock D605 also lists inverted ordering; that tests the NO input, and with m_ν1 ≈ 0 IO already implies Σm_ν ≈ 0.10 eV.)
- |f_NL^local| > 5.
- SERAPIS-E at ρ (D735–D736, estimate, post-hoc): no disappearing-track wino at 0.67–0.80 TeV in Run-3/HL-LHC data falsifies the cuspy-halo version (ATLAS 2603.08315 now excludes < 670 GeV).
- Covariant completion: no wino up to 2.9 TeV and no gluino up to 21 TeV (FCC-hh reach), or a wino above 2.9 TeV overclosing; lock D605 P5 (constant W0): superpartners below 10⁸ GeV.

## Who tests what (forecasts: 2212.04115 Table 5 halved to 1σ; SO 2503.00636; LiteBIRD/JAXA; D705)
| Experiment (era) | Observable | 1σ reach | What SERAPIS needs / outcome |
|---|---|---|---|
| SO LAT + SPHEREx (~2030) | n_s, α_s | σ(n_s) ≈ 8e-4, σ(α_s) ≈ 1.2e-3 | n_s 0.970–0.975: 2.3–8.5σ from today's CMB-only 0.9682 — first decisive test |
| SO SATs, BICEP/Keck + SPT-3G (2020s) | r | σ(r) ~ 2–5e-3 | no detection (consistent) |
| LiteBIRD (launch 2032, results ≳ 2035) | r | forecast σ(r) ≈ 5e-5 (r = 0 fiducial); requirement δr < 1e-3 | SERAPIS-E r ≈ 4.7e-4 at ~10σ (optimistic); r ladder 4.7/3.4/2.5e-4 resolvable at ~2σ per step; nothing seen at the requirement level |
| CMB-S4 | — | DOE/NSF support ended 2025 | — |
| DESI, Euclid | Σm_ν | σ ~ 0.02 eV | ≈ 0.059 eV |
| JUNO, DUNE, Hyper-K | ordering | NO vs IO at > 3σ | tests the NO input (not a model output) |
| Janus α_s test | α_s | needs σ ~ 1e-4 (D670) | beyond funded experiments |

## What is NOT predicted (stated limits)
- The size of ε (the tilt strength) is fitted to the low-T_R window, not derived; its microscopic origin is open (D620–D631, D684–D687: not from the supergravity sector; tilt shape identified with the N = 2 threshold at ρ). SERAPIS-E (D689–D693) derives a tilt of natural size from the Berg–Haack–Körs one-loop Kähler correction, Im S·Im ρ ≈ 190–245 N; plateau placement in the uplift is still by hand.
- Superpartner window assumes the modular-covariant completion, X-independent gauge kinetic functions (anomaly-mediated gauginos) and initial conditions 6–12 e-folds before horizon exit, higgsino threshold (window ends ×2); dilaton–LSP bound relaxes to m_Y ≳ 35 H_end (winos re-thermalise, but gravitinos from Y decays do not; D652, D658); gravitinos decay before BBN (D651); AD thermal effects negligible (D653); Weinberg operator non-zero at i with k_L = k_Hu = 1 (D654a); covariant completion: centre gives ordinary matter parity at ρ (D661) and at τ = i with Γ2 doublets (D663–D664); dim-5 coefficients ≲ 5e-3 (D657).
- Preheating inefficient (q ≲ 2e-4 for m0 ≲ m_φ) and φ → gravitino + inflatino closed (m_inflatino = 4/3 m3/2) — estimates, D641. If either were efficient, N* would rise 6–9 e-folds and Chronos would leave its band.
- Collider signals: none expected at LHC/FCC energies.
