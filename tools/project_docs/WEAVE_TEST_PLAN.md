# The Weave: test plan v2, one test per UFE term (21 Nov 2026, 16:50 CT)
Danny 16:45: "a test plan for each stage or each part … when we publish this, I want all the data … to be irrefutable."

This plan maps every term of **UFE v4** (WEAVE_UNIFIED_EQUATION.md) to the test that could kill it. It replaces v1 (08:13), whose stale rows are listed in §4.

## 0. The standard: what "irrefutable" can mean
No physical theory can be made irrefutable; a theory that could not be refuted would not be science. What can be made unassailable is **the record**: every number reproducible, every test fixed before its data, every failure shown. Each published claim must clear six gates.

| gate | requirement | how we meet it |
|---|---|---|
| G1 Pre-registered | prediction, data, threshold and null fixed before the data or computation | PREREG + sha256, pushed first (in place since D1873) |
| G2 Reproducible | one command regenerates every number from the repo; no typed-in values | scoreboard script + results files; a values-file engine (queue item) |
| G3 Triangulated | three independent vectors, converged to 7 nulls (Rule 6h) | TRIANGULATE: line in every D-note |
| G4 Refereed | an independent, fresh-context referee on every scoreboard change | done every ≤ 4 ticks (D1897, D1909, D1920, D1923, D1927, tick 16) |
| G5 Falsifiable | a stated observation that would kill the term, by a named experiment and date | the KILL column below |
| G6 Honest count | only post-lock data counts as evidence; fits, bounds and naturalness bars are shown as such | evidence classes below; FAILs are reported, not hidden |

**Evidence classes:**
- **P**: a prediction scored on future data (the only strict evidence).
- **D**: a pull against existing data (counts, but was not blind).
- **B**: a bound passed.
- **N**: naturalness.
- **I**: internal consistency.
- **T**: TRUST, an input with no test.

## 1. Test plan by UFE term (centre outwards)
| ring | UFE term | Weave value | class | test (data, experiment) | KILL condition | lock | status |
|---|---|---|---|---|---|---|---|
| 0 | quark spurion, \|u\| ∈ [0.02588, 0.02740] | f7 22–23 %, fJ 61–66 % | N (PHEN) | Lattice and PDG quark masses and CKM; the window must stay natural when the inputs update | No natural assignment in the window after the next PDG/FLAG update | PREREG_D1932 | ● converged |
| 0 | quark spurion's home | open | T | U₃ near i or a twisted modulus must give \|u\| ≈ 0.0266 | No geometric source of that size | to write | OPEN |
| 0 | θ̄ = 0 (anomaly-free weights) | d_n ~ 1e-32 e·cm | P | n2EDM (PSI) | d_n > 1e-26 e·cm | PREREG_B8B9_EDM | R |
| 1 | charged leptons at ρ (3 rungs) | natural 5.3 % | N | — | — | D1877 | modest |
| 1 | Koide Q = 2/3 | m_τ = 1776.969 MeV | P | Belle II, BESIII m_τ | m_τ off by > 3σ | PREREG_B1_KOIDE_MTAU | R |
| 1 | Koide δ = 2/9, c_e | input | T | none until derived | — | — | TRUST |
| 1 | neutrinos at i, TM1 | sin²θ₁₂ = 0.3184 | **P** | **JUNO 6-yr (±0.0015)** | JUNO centre > 3σ from 0.3184 | PREREG_TM1_JUNO | **R: the strongest near-term test** |
| 1 | δ_CP branch | 255–295° | P | DUNE, Hyper-K | outside at 3σ | PREREG_B3 | R |
| 1 | Σm_ν (NO, m₁ = 0) | 0.0587 eV | P | DESI DR3 + CMB | 95 % limit < 0.055 eV, or IO at 3σ | PREREG_B4 | R |
| 1 | 0νββ | m_ββ 1.59–3.80 meV | P | LEGEND-1000, nEXO (predicts NULL) | a signal > 7.6 meV | PREREG_B5 | R |
| 1 | neutrino ratio | 1.3 % natural | N | — | — | D1821 | ↑ thin (0.12 dex) |
| 2 | m₃/₂ (KKLT, N = 6, χ = 48) | 2.58e5 GeV | I | through the spectrum | — | D1871 | TENSION |
| 2 | **wino** (AMSB) | **0.687 TeV** | **P** | ATLAS/CMS disappearing tracks (Run 3, HL-LHC); CTA γ-line | excluded below 0.70 TeV, or no signal up to 1.0 TeV at HL-LHC | to refresh (C5) | **↑ 2 % margin: the nearest collider kill** |
| 2 | gluino | 4.93 TeV | B → P | HL-LHC / FCC-hh | found below 3 TeV | to write | ● |
| 2 | **α_s(M_Z)** | **0.1142** | **D** | PDG world average 0.1180 ± 0.0009 | already **FAILS at −4.2σ** | PREREG_D1929 | **↑! open: needs Δ₃** |
| 2 | Δ₃ threshold | −0.094 (bar −0.05) | I | brane-native D7 computation | no D7 spectrum reaches −0.05 | to write | ↑! |
| 2 | proton decay (G-branch) | 1.6e35 yr | P | Hyper-K, DUNE | e⁺π⁰ seen below 1e35 yr on the G-branch | PREREG_B10 | R |
| 3 | inflation plateau E(S, 3/2) | n_s 0.9706 | D | CMB-SPA + DESI 0.9728 ± 0.0027 | > 3σ off with future CMB-S4 | weave_derivation_v4 | ● soft ↑ |
| 3 | r | 5.4e-4 | **P** | **LiteBIRD, CMB-S4 (σ_r ≈ 5e-4)** | r excluded below 2.5e-4, or r > 1.5e-3 | PREREG A1 | R |
| 3 | running α_s(k) | −9.7e-4 | P | CMB-S4, SPHEREx | outside −1.05e-3 to −0.95e-3 at 3σ | PREREG_A2_RUNNING | R |
| 3 | f_NL, isocurvature | ≈ 0 | P | SPHEREx, Planck | f_NL^local > 1 at 3σ | PREREG_A4 | R |
| 3 | **T_R** | **3.7e8 GeV** | I | through N* (n_s) and leptogenesis | no consistent baryogenesis path | to write (ring 3) | **↑! strongest pointing** |
| 3 | dark matter, asymmetric | m_X = 12.8 GeV | **P** | LZ, XENONnT, XLZD | excluded at 12.8 GeV down to the ε floor, or annihilation seen | PREREG_C1, C4 | R |
| 3 | dark photon | 0.3–12.8 GeV | P | SHiP, NA64, Belle II | — (a window, not a kill) | PREREG_C2 | R |
| 3 | ΔN_eff | 0 (never positive) | P | SO, CMB-S4 (σ 0.03) | ΔN_eff > 0 at 3σ | PREREG_A6 | R |
| 4 | dark-energy thread | non-Kähler, λ ≈ 0.95 | — | DESI DR3, Euclid w₀–w_a | (after derivation) | five must-tests locked | OPEN |
| 4 | α drift ζ | 3.8e-10 | P | atomic clocks, ESPRESSO | ζ > 1e-8 detected | D1887 | ● |
| 4 | equivalence principle | no violation | P | MICROSCOPE-2 | \|η\| > 1e-17 | PREREG_D4 | R |
| 4 | no domain walls | — | P | NANOGrav, IPTA | DW vs SMBHB Bayes factor ≥ 100 | PREREG_A9 | R |
| 4 | GW speed, polarisations | standard | P | LIGO-Virgo-KAGRA | deviation | PREREG_D6 | R |

## 2. The five tests that decide it (ranked by power and date)
1. **JUNO sin²θ₁₂ = 0.3184** (data in hand around 2027–2030, about 6σ separation if the centre holds). This is the cleanest prediction the Weave makes.
2. **The wino at 0.687 TeV**, with a 2 % margin over the current disappearing-track limit. HL-LHC either finds it or kills the spectrum.
3. **α_s**: already failing at −4.2σ. Publishing honestly means either a derived Δ₃ that closes it, or showing the failure.
4. **r = 5.4e-4** at LiteBIRD / CMB-S4.
5. **12.8 GeV asymmetric dark matter** at XLZD.

## 3. Before publication (the irrefutability checklist)
- [ ] One-command reproduction: the scoreboard plus every locked script, run from a clean clone, matching the stored results (D1898 did this once; repeat it on the final version).
- [ ] Values file: no number typed into the paper; every paper number pulled from results files (queue item 9).
- [ ] Every UFE term with a TRIANGULATE: line converged to 7 nulls.
- [ ] Final independent referee pass on the whole paper (fresh context, a heterogeneous model).
- [ ] The evidence count shown by class (P/D/B/N/I/T), with the FAILs in the abstract.
- [ ] The look-elsewhere / trials ledger reported for every headline coincidence.
- [ ] Every prediction in §1 locked with a date before its data release.

## 4. Stale rows from v1 (superseded)
- **D1** thawing thread w₀ ≈ −0.79: the Kähler thread is excluded (D1906). It is OPEN now (ring 4).
- **D5** birefringence: the carrier cycle is unsettled after D1793. It is held until ring 4.
- **B11** "α_s 0.1158, consistent": superseded. The gauge term (D1881b) and the gluino at its own scale give **0.1142, FAIL** (D1929).
- **C5** wino 0.67–1.0 TeV: now 0.687 TeV from the derived chain. The lock needs a refresh.
- **B6** CKM: closed in v1. The quark term is now the single spurion (D1932), which is naturalness, not a fit.
- **B10** proton: the G-branch is 1.6e35 yr (two-loop), not 2.5–3.2e34.
