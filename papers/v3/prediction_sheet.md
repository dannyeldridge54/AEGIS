# SERAPIS — one-page prediction sheet (R6)

Frozen 15 Nov 2026; harmonised with the R8 referee fixes (R8b, D636/D637) (locks D605 τ=i, D615 ρ, D633 + addendum running; hashes in MANIFEST.md).
Scored only on data published after that date. ε is not retuned; any revision is a new model.
Labels: **computed** = from locked scripts (exact Mukhanov–Sasaki, D588); **estimate** = analytic/order-of-magnitude.

Status note (16 Nov 2026, D841, decision rule committed first): the τ = i branch (Chronos) is a CONDITIONAL variant: its ε has no derived source and it needs a 2⊕1 heavy-ν structure not required at ρ. No frozen number below changes.

## Headline numbers
| Quantity | τ = i branch (Chronos) | ρ branch | Kairos (untilted, reference) | Label |
|---|---|---|---|---|
| n_s | 0.970–0.975 | 0.969–0.972 | 0.959–0.961 (D637, N* 46–49) | computed |
| r | (4.8–5.7)×10⁻⁴ | (4.6–5.1)×10⁻⁴ | (3.3–3.7)×10⁻⁴ (D637) | computed |
| α_s = dn_s/dln k (lock D633, N* 47–50; −(8.8–10.2)×10⁻⁴ at N* 46–49, D642) | −(8.6–9.9)×10⁻⁴ (lock D633; D605's −(3–5)×10⁻⁴ was an attractor estimate, superseded) | −(8.5–9.5)×10⁻⁴ | ≈ −2/N*² | computed |
| m_ν1 (Affleck–Dine LH_u at τ = i, D646 yield at corrected T_R, D900; conditional at i, D903; ρ: 2×10⁻¹¹–9×10⁻¹⁰ eV, D895) | 1.6×10⁻¹⁰–2.7×10⁻⁹ eV (T_R (0.8–3)e6 GeV; thermal effects negligible, D653/D900; was 2×10⁻¹³–9×10⁻¹¹ at the superseded T_R 1e3–1e5) → Σm_ν ≈ 0.0587 eV IF normal ordering (D786: the NO floor; status D824) (ordering is input from data, not predicted; lock D605 states NO) | same | — | estimate (D646/D646a) |
| β_s = d²n_s/dln k² (lock D667) | −(3.0–4.6)×10⁻⁵ | same | −4/N*³ | computed |
| f_NL^local / isocurvature | ≈ 0.01 / ~10⁻⁸ of ζ (D587; lock D605 said ≲10⁻¹⁰) | ≈ 0.01 | — | estimate/computed |
| Superpartners | covariant completion (adopted, D647–D650; windows as in v3.1, D808): wino LSP 0.67–1.85 TeV (Einasto; up to 2.9 TeV only for cored halos), m3/2 ≈ (2.5–7)×10⁵ GeV, scalars ~ m3/2, gluino 4.7–13 TeV (estimates; Fermi-LAT 2507.15934 excludes 1.85 TeV to the thermal mass; ATLAS 2603.08315 excludes < 670 GeV; a sub-component of DM, D713/D784); SERAPIS-E at ρ with fast reheating (D725–D735, estimates): gravitino→wino plus H.E.S.S. line limit narrow this to wino 0.66–0.8 TeV (Einasto; any mass for kpc cores), ~15% of DM, heavy neutrinos ~1e12 GeV; constant-W0 chain (lock D605 P5): none below ~10⁸ GeV | same | — | estimate |
| SERAPIS-E (loop-motivated branch, lock D693, frozen after the data; scored on future data only) | n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4; Janus κ=1 (p=2√2) ≤6%; N* 48.4–49.9 | — | — | computed |
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
- Neutrino sector (D750, derived, not frozen): normal ordering, m₁ ≈ 1e-4 – 4.4e-3 eV, m_ββ ≤ 7.5 meV (no signal at LEGEND-1000/nEXO/CUPID), m_β ≈ 9–10 meV (null at KATRIN/Project 8), Σm_ν 0.0586–0.064 eV: a robust cosmological bound Σ < 0.058 eV falsifies the model.
- SERAPIS-E at ρ (D735–D736, estimate, post-hoc): no disappearing-track wino at 0.67–1.85 TeV (thermal, D784) in Run-3/HL-LHC data falsifies the cuspy-halo version (ATLAS 2603.08315 now excludes < 670 GeV).
- Covariant completion: no wino up to 2.9 TeV and no gluino up to 21 TeV (FCC-hh reach), or a wino above 2.9 TeV overclosing; lock D605 P5 (constant W0): superpartners below 10⁸ GeV.

## Who tests what (forecasts: 2212.04115 Table 5 halved to 1σ; SO 2503.00636; LiteBIRD/JAXA; D705)
| Experiment (era) | Observable | 1σ reach | What SERAPIS needs / outcome |
|---|---|---|---|
| SO LAT + SPHEREx (~2030) | n_s, α_s | σ(n_s) ≈ 8e-4, σ(α_s) ≈ 1.2e-3 | n_s 0.970–0.975: 2.3–8.5σ from today's CMB-only 0.9682 — first decisive test |
| SO SATs, BICEP/Keck + SPT-3G (2020s) | r | σ(r) ~ 2–5e-3 | no detection (consistent) |
| LiteBIRD (launch JFY 2032, results ≳ 2035) | r | total δr = 1e-3 including systematics and margin; σ_stat = 6e-4 at r = 0 (2406.02724) | SERAPIS r ≈ (4.6–5.7)e-4 is BELOW 1σ: not detectable by LiteBIRD alone. LiteBIRD tests SERAPIS by EXCLUSION (r ≳ 1e-3 detected → model out). Corrected D820; the earlier '5e-5, ~10σ' entry was wrong |
| CMB-S4 | — | DOE/NSF support ended 2025 | — |
| DESI, Euclid | Σm_ν | σ ~ 0.02 eV | ≈ 0.059 eV |
| JUNO, DUNE, Hyper-K | ordering | NO vs IO at > 3σ | tests the NO input (not a model output) |
| Janus α_s test | α_s | needs σ ~ 1e-4 (D670) | beyond funded experiments |

## What is NOT predicted (stated limits)
- The size of ε (the tilt strength) is fitted to the low-T_R window, not derived; its microscopic origin is open (D620–D631, D684–D687: not from the supergravity sector; tilt shape identified with the N = 2 threshold at ρ). SERAPIS-E (D689–D693) derives a tilt of natural size from the Berg–Haack–Körs one-loop Kähler correction, Im S·Im ρ ≈ 190–245 N; plateau placement in the uplift is still by hand.
- Superpartner window assumes the modular-covariant completion, X-independent gauge kinetic functions (anomaly-mediated gauginos) and initial conditions 6–12 e-folds before horizon exit, higgsino threshold (window ends ×2); dilaton–LSP bound relaxes to m_Y ≳ 35 H_end (winos re-thermalise, but gravitinos from Y decays do not; D652, D658); gravitinos decay before BBN (D651); AD thermal effects negligible (D653); Weinberg operator non-zero at i with k_L = k_Hu = 1 (D654a); covariant completion: centre gives ordinary matter parity at ρ (D661) and at τ = i with Γ2 doublets (D663–D664); dim-5 coefficients ≲ 5e-3 (D657).
- Preheating inefficient (q ≲ 2e-4 for m0 ≲ m_φ) and φ → gravitino + inflatino closed (m_inflatino = 4/3 m3/2) — estimates, D641. If either were efficient, N* would rise 6–9 e-folds and Chronos would leave its band.
- Collider signals: none expected at LHC/FCC energies.


## Post-hoc ρ baryogenesis inside the frozen band (D880, corrected D880a/D895; NOT locked)
LH_u Affleck–Dine at ρ with the band-safe late reheating T₂ = 1e5–1e6 GeV: needs m_ν₁ ≈ 2×10⁻¹¹–9×10⁻¹⁰ eV (same no-thermal yield as τ = i, D895), keeping the frozen n_s, r, α_s and the Σm_ν NO floor 0.0587 eV. Conditions: Γ₂-singlet leptons, two extra Z₃-neutral singlets, E₄(ρ) = 0 protection lifted by ε ≈ 1.6×10⁻⁴ (fitted, D896), and an instanton-only Weinberg term with action S ≳ 14–19 (D897). This supersedes the self-diluted history below as ρ's preferred route.

## Post-hoc ρ-branch alternative (D792–D793, 16 Nov 2026; NOT locked, scored only on future data; SUPERSEDED as preferred route by D880/D895, kept for the record)
"SERAPIS-E/ρ, self-diluted". The Z₃-charged inflaton acts as an Affleck–Dine condensate; the late, string-scale-suppressed decays of the Z₃-charged heavy ν dilute and release the baryon asymmetry (T₂ ≈ 150–1100 GeV).
- n_s = 0.966–0.970; r = (5.2–5.7)×10⁻⁴; α_s = −(1.08–1.18)×10⁻³ (exact MS, D813; outside the frozen D693 band; inside the family strip and cap).
- Wino: thermal, 0.67–1.85 TeV (5–41% of DM).
- Baryogenesis: spontaneous CP (initial offset ≥ 0.15 from Re τ = ½); no extra fields.


## Data check D805 (16 Nov 2026; comparison only, frozen predictions unchanged)
2512.05108: CMB-SPA 0.9693 ± 0.0029, CMB-SPA+DESI 0.9737 ± 0.0025 (shifts +0.3σ from the references). Frozen band 0.970–0.975: −1.48 … +0.52σ vs CMB-SPA+DESI (centred). Post-hoc ρ self-diluted 0.966–0.970 (MS, D813): −3.1 … −1.5σ vs CMB-SPA+DESI.


## Error budgets of the frozen bands (D821, 16 Nov 2026; frozen numbers unchanged)
Theory uncertainty on the band EDGES (not on the parameter, which spans the band). Each entry: size, source, label.

### τ = i band (lock D605: n_s 0.970–0.975, r 4.8–5.7e-4)
| Source | δn_s | δr/r | Basis |
|---|---|---|---|
| Reheating (N* bracket 46.1–49.2) | spans 0.0029 (inside the band) | spans −8% | MS slopes dn_s/dN* = 9.3–9.6e-4, d ln r/dN* = −2.6% (D642, D815) [derived] |
| Corrected T_R (stiff phase, N* ≈ 50.3) | +0.0013 to +0.0018 shift | −4 to −5% | D729/D815: only ε 1.40–1.45e-4 stays in band [derived] |
| Slow roll (lock) vs exact MS | ≤ 0.0004 beyond edges | ≈ +1.5% | D642/D815/D817 [derived] |
| Pivot / N* matching convention (±0.5 e-fold) | ±0.0005 | ±1.3% | [estimate] |
| Parameter ε (1.3–1.6e-4) | spans 0.0028 | spans +10% | defines the band [derived] |
| Plateau functional form | not quantifiable | — | the plateau is chosen by hand (paper: by choice) |
Edge uncertainty (convention ⊕ SR): ±0.0006 in n_s, ±2% in r.

### SERAPIS-E band (lock D693: n_s 0.970–0.975, r 4.55–5.12e-4, α_s −(9.4–10.6)e-4)
| Source | δn_s | δr/r | Basis |
|---|---|---|---|
| Reheating (N* 48.4–49.9) | spans 0.0014–0.0015 | spans −4% | MS (D692) [derived] |
| Late Z₃ decay (T₂) | frozen band holds for T₂ ≳ 1e5 GeV; below that, the band shifts to the self-diluted 0.966–0.970 | +10% | D781, D813 [derived] |
| Exactness | none (band computed with MS) | — | D692 [derived] |
| Pivot / N* matching convention (±0.5 e-fold) | ±0.0005 | ±1.4% | [estimate] |
| Parameter C (1.0–1.3e-6) | spans 0.0030 | spans +8% | defines the band [derived] |
| Two-loop Kähler terms (~C²E²) | ≲ 1e-4 | ≲ 0.1% | [estimate] |
Edge uncertainty: ±0.0005 in n_s, ±1.5% in r. Largest conditional risk: the T₂ condition, not a numerical error.


## Σm_ν status (D824, 16 Nov 2026)
Frozen 0.0587 eV (NO floor) vs the strongest 95% bound < 0.0592 eV (DESI DR2 + Lyα AP, ΛCDM; 2607.27410): alive by 0.0005 eV. The data prefer an effective Σm_ν < 0 (2610.20977); if that persists, Advanced SO + DESI DR3 would reject 0.058 eV at ~3σ (forecast). That would test NO + ΛCDM generally, not SERAPIS specifically. τ = i with m₁ free: only m₁ ≲ 5.6e-4 eV survives (D786).
Data check 16 Nov 2026 (D902): CMB-SPA + DESI DR2 + DES Y5 gives Σm_ν < 0.052 eV (ΛCDM, adiabatic, prior extending to zero; 2606.17994), below the NO floor; the same paper gives < 0.092 eV with a hierarchy-informed prior and calls the 0.052 eV value a prior artefact. Status of the floor: under pressure from zero-prior combinations, alive under physical priors. Frozen value unchanged.

## Independent reproduction (16 Nov 2026, D953–D962)
n_s and r for SERAPIS-E, Chronos, Kairos and SERAPIS-ρ reproduced by separately written code (tools/serapis_calc). α_s agrees to ~10%; both codes show ~10% sensitivity of α_s to the Bunch–Davies start (D958); convergence test D960 pending. Frozen values unchanged.

## Project H sibling (17 Nov 2026, D976–D978; post-hoc, scored only on future data)
If the plateau comes from Project H at its largest allowed loop coupling (λ′ ≈ 0.17, locked refit C = λ′C₀): n_s ≈ 0.9714, r ≈ 5.0e-4 — a sibling of SERAPIS-E inside the frozen band. Fixed-C variant excluded (≈41 e-folds). Frozen SERAPIS-E values unchanged.

## Reproduction follow-ups (17 Nov 2026, D979–D980)
- N*: exact end of inflation puts SERAPIS-E's N* bracket 0.17 e-folds above D719 (N* = 46.46–51.04 for T_R = 1e4–1e10 GeV); Δn_s ≈ +1.5e-4, inside the frozen band.
- α_s: convergence tests (D974, D980) do not pin it below ~10%; published α_s consistent at that level. Next: wide-grid fit (new lock).
