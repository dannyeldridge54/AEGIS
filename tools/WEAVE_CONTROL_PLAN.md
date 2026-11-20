# Weave Control — one model driving all four toolkits (plan, 20 Nov 2026)
Danny 04:36–04:37 CT: "Build a model that controls them all with full display capabilities like Janus but for each level in each category … wire them to feed each other more data. Think about what our model says, list [50] unique things, then ask how our tools could do their jobs individually but better."
(Read "listv59" as "list 50"; one extra is added as a cross-cutting item.)

Labels: **P** = prediction (could fail), **F** = fitted or chosen (not a test), **G** = open gap, stated honestly. Sources are the register (WEAVE_POSTULATES.md) and the D-notes cited.

## Part 1 — 51 things the Weave says, and which tool tests each

### A. Inflation and the loom (Janus)
| # | the Weave says | label | tool | data that tests it |
|---|---|---|---|---|
| 1 | The inflaton's energy is the running of the species scale, V₀ ∝ \|∇ln Λ_sp\|² (Zhinü) | P (structure) | Janus | the n_s–r–α_s point it forces |
| 2 | r = 5.4 × 10⁻⁴ in a 10D phase, 1.07 × 10⁻³ in a 6D phase | P | Janus | LiteBIRD, CMB-S4 (σ_r ~ 5 × 10⁻⁴) |
| 3 | r ladder r_D = r₁₀ · 8/(D − 2): the dimension at horizon exit is readable from r | P | Janus | same, two r values a factor 2 apart |
| 4 | Running α_s ≈ −9.7 × 10⁻⁴ at n_s 0.9706 | P | Janus | CMB-S4 + SPHEREx (σ_α ~ 2 × 10⁻³) |
| 5 | n_s ≈ 0.9706 | **F** (Ushas tilt chosen) | Janus | none (a fit) |
| 6 | Bridge B1: r − 3(1 − n_s)² ≈ −0.9 × 10⁻⁴; B2: α_s + ½(1 − n_s)² ≈ 0 | P (null tests) | Janus | joint n_s, r, α_s posterior |
| 7 | N* ≈ 50.4–50.6, fixed by the reheating history (not free) | P | Janus ↔ Hyperion | n_s–r position at fixed model |
| 8 | Reheating T_rh ≈ 9 × 10⁸ GeV, heat share 0.65–0.8% | P | Janus ↔ Hyperion | gravitino/moduli limits, BBN |
| 9 | The TCC is not a law: any r detection falsifies the TCC, not the Weave | P | Janus | any r > 10⁻³⁰ |
| 10 | One-loop signs: D = 8 positive everywhere; D = 6 positive once the T⁴ volume exceeds ~1.6 ℓ_s⁴ | P (math) | serapis_calc | Narain-lattice computation |
| 11 | A 6D phase at horizon exit needs two anisotropic LVS cycles with M_KK < H | C | Janus | the r node |

### B. Flavour (new level; currently no toolkit — Janus "Flavour" panel proposed)
| # | the Weave says | label | tool | data |
|---|---|---|---|---|
| 12 | Koide Q = 2/3 from Z₃ equipartition | P | Flavour panel | m_τ (Belle II, BES III) |
| 13 | Koide holds for POLE masses (Sumino-type family bosons cancel QED running) | C | Flavour | running vs pole comparison |
| 14 | Brannen phase δ = 2/9 | P (no mechanism yet) | Flavour | lepton masses |
| 15 | Neutrino mixing is TM1; exact TM2 is excluded by JUNO | P | Flavour | JUNO sin²θ₁₂ to ±0.5% |
| 16 | δ_CP on the lower TM1 branch, 262°–286° | P | Flavour | T2K+NOvA, DUNE, Hyper-K |
| 17 | Modular S₄ at the vacua ρ and i | C | Flavour | mixing pattern |
| 18 | τ_ν offset 1.0685i | F (fitted to sin²θ₁₂) | Flavour | — |
| 19 | CKM phase J = 3.1 × 10⁻⁵ with θ̄ = 0 | P | Flavour | CKMfitter |
| 20 | Family gauge bosons (triglavon) above ~10² TeV | P | CERN+1 (FCC-hh) | flavour-violating decays |

### C. Dark sector and late universe (Hyperion + CLASS + CERN+1)
| # | the Weave says | label | tool | data |
|---|---|---|---|---|
| 21 | The reverse thread: dark energy never has w < −1 | P | CLASS / dashboard | DESI DR3, Euclid |
| 22 | (w₀, w_a) ≈ (−0.79, −0.36) | P | dashboard | DESI DR3 |
| 23 | Apparent w crosses −1 near z ≈ 0.6 only through mis-modelling, never in the field | P | CLASS | reconstruct w(z) |
| 24 | Arthur-field coupling b_A to dark matter | P → **currently consistent with 0 (D1725)** | CLASS | full Planck + DESI + SN |
| 25 | Dark matter clusters with G_eff = G(1 + 2b²) | P | Hyperion halos | S₈ (KiDS, DES, Euclid) |
| 26 | Negative space: effective Λ negative above z†, deepening as (1+z)³ | P (needs b_A < 0) | CLASS | H(z) at z 2–5: DESI Lyα BAO, 21 cm |
| 27 | Closed form (1+z†)³ ≈ Ω_φ/[Ω_c(e^{\|b\|Δφ} − 1)] | P (math) | Weave Control | — |
| 28 | Only dark matter feels the coupling; baryons don't (no fifth force for us) | P | Hyperion | MICROSCOPE, Cassini, clocks |
| 29 | Clock bridge (α̇/α)/[H₀√(3Ω_DE(1+w₀))] = ζ ≲ 3.6 × 10⁻⁶ | P | Hyperion | optical clocks |
| 30 | Birefringence β² = 2.5 × 10⁻³ (c_γ/f)²(1 + w₀) deg² | P | Janus/CMB | ACT, SPT, LiteBIRD β |
| 31 | β_reio/β_rec = 0.997–0.999 (nearly equal at two epochs) | P | Janus/CMB | LiteBIRD |
| 32 | Dark matter = mirror baryons 0.94 GeV, OR a minimal dark sector at 5 GeV / X at 12.8 GeV (sarion) | P (two branches) | Hyperion + CERN+1 | SuperCDMS, TESSERACT, CRESST |
| 33 | n_X/n_B = 11/28 from our own chemical equilibrium | P | Hyperion | — |
| 34 | Dark photon (cassion) in the dim strip ε ≲ 3 × 10⁻⁹ to 8 × 10⁻⁷ | P | CERN+1 / Hyperion | beam dumps, direct detection |
| 35 | Dark sector is cold: ΔN_eff ≤ 0.086, from the brane split (visible D3, dark D7) | P | Hyperion | CMB-S4 σ(N_eff) ≈ 0.03 |
| 36 | Portal X²LH/M with M ≈ 10¹⁰–10¹² GeV (saulon) | P | Hyperion | — |
| 37 | Leptogenesis: heavy N (waaqino) M ∈ [1.9 × 10¹⁰, 2.5 × 10¹²] GeV, ε = 1.8 × 10⁻⁶ → η = 6.1 × 10⁻¹⁰ | P | Hyperion | η from CMB/BBN |
| 38 | Wino (SERAPIS-E) is thermal near 2.25 TeV; lighter winos are a fraction (M/M_th)² | P | CERN+1 + Hyperion | disappearing tracks; HESS/CTAO gamma line |
| 39 | The dark dimension scenario is ruled out for us | P | — | — |
| 40 | Λ's size | **G** (set by hand) | — | — |

### D. Matter genesis and stars (Hyperion)
| # | the Weave says | label | tool | data |
|---|---|---|---|---|
| 41 | Y_p from our network (0.2445 + corrections) | P | Hyperion | LBT, Aver |
| 42 | Lithium problem reproduced (×2.7), NOT solved; mirror sector moves Li by ~10⁻⁵ | P (honest null) | Hyperion | Spite plateau |
| 43 | Dilution D ≤ 10³; ΔN* = −⅓ ln D; DM mass ∝ D; leptogenesis yield × D | P (links) | all | shared quantities |
| 44 | Moduli decay before BBN (T_decay ≥ 5 MeV), residual displacement ≲ 10⁻⁷–10⁻⁵ M_P | P | Hyperion | BBN |
| 45 | Kination after inflation → blue-tilted gravitational-wave background | P | Hyperion gwb | LISA, ET, PTA |
| 46 | Isocurvature within Planck limits | P | Janus | Planck isocurvature |
| 47 | Species-scale black hole (Māui knot): the smallest hole that holds the weave | C | Hyperion compact | — |

### E. Cross-cutting
| # | the Weave says | label | tool | data |
|---|---|---|---|---|
| 48 | One thread (coupling) runs through every level; shared quantities: N*, heat share, kination, x_E, v, λ, D, DM mass, η, c_γ/f | structure | Weave Control | all of the above at once |
| 49 | String flags reported, not used to veto: TCC, distance conjecture, dS slope, axion WGC | P | Janus | — |
| 50 | Every claim locked before computing; NULL results kept | method | all | — |
| 51 | The uncoupled thread beats ΛCDM in two codes (Δχ² −2.6 / −8.1 / −3.4) but trails w0wa | result | dashboard | DESI DR3 |

## Part 2 — each tool doing its own job better than the specialists
What people complain about in the leading tools (from the U-reviews already done and the published code papers), and the answer each AEGIS tool gives:

**Janus (vs CAMB/CLASS inflation modules, ASPIC, Cobaya):**
1. N* is a free knob in most tools → Janus takes N* from the reheating history (#7, #8).
2. Slow-roll only → exact Mukhanov–Sasaki already; add the ±σ band from N* uncertainty.
3. One data set at a time → every n_s/r set at once, overlap-aware (done, J3).
4. No consistency checks → B1/B2 bridges reported as null tests on every run.
5. Prediction vs fit not marked → done (J3b); extend to every model.
6. New: birefringence and isocurvature outputs from the same model (#30, #31, #46).

**Hyperion (vs PRyMordial, PArthENoPE, AlterBBN, DarkSUSY, micrOMEGAs):**
1. BBN codes take ΔN_eff as a number → Hyperion takes it from the dark sector it models (#35).
2. Reaction-rate uncertainties are rarely propagated → Monte Carlo over rates, with error bars on Y_p and D/H.
3. DM tools and BBN tools are separate → one package: relic, Sommerfeld, J-factor, gamma line, BBN.
4. Gamma-line limits need the halo profile chosen by hand → profile bracket (NFW/Einasto/Burkert) shown together.
5. New: G_eff(b_A) → halo growth and S₈ shift (#25); clock and fifth-force bridge (#28, #29).

**CERN+1 (vs SModelS, CheckMATE, MadAnalysis, pyhf alone):**
1. Long-lived particles are poorly covered in recast tools → CERN+1 is built on disappearing tracks and lifetimes.
2. No future-collider reach in one place → run presets from Run 2 to FCC-hh (done).
3. Simplified likelihoods often missing → R5 (queued).
4. Inputs are SLHA files from elsewhere → also takes the Weave's own wino mass and fraction (#38).
5. New: triglavon and cassion reach (#20, #34) at FCC-hh and beam dumps.

**Mapper (vs Stellarium, SkySafari, Aladin, Telescopius):**
1. Finder charts are separate apps → finder charts built in (done, M1b).
2. No science context → overlay where the model is tested: DESI and Euclid fields, the Galactic-centre gamma-line region, LiteBIRD/CMB-S4 sky patches.
3. Online-only image surveys → offline pack (queued M1g).
4. Plans ignore the target's science value → rank tonight's targets by relevance to open Weave tests.

## Part 3 — what the tools feed each other (the wiring)
| from → to | quantity | Weave item |
|---|---|---|
| Janus → Hyperion | N*, T_rh, heat share → ΔN_eff and BBN | #7, #8, #35, #41 |
| Hyperion → Janus | ΔN_eff → CMB damping-tail shift for the n_s comparison | #35 |
| Dark-sector settings → Hyperion + CERN+1 | m_X (12.8 GeV), ε, ΔN_eff → direct detection, beam dumps, BBN | #32–#35 |
| CERN+1 → Hyperion | wino mass and fraction → gamma-line σv × J vs HESS/CTAO | #38 |
| Hyperion → Mapper | J-factor region, dwarf targets → sky overlays and finder charts | #38 |
| CLASS (b_A) → Hyperion | G_eff → S₈; z† → H(z) at z 2–5 vs DESI Lyα | #24–#26 |
| Late universe → Mapper | DESI/Euclid footprints → overlays | #22, #26 |
| All → Weave Control | one parameter set; each level shows inputs, outputs, data, pull, status | #48 |

## Part 4 — build order (Weave Control)
1. **Engine** tools/weave_control/engine.py: one parameter set → levels (Inflation, Flavour, BBN, Late universe, Colliders, Galaxy & dark matter, Stars, Sky), each tagged with its category (A–E) and returning inputs, outputs, data with sources, pulls and status.
2. **Links**: ΔN_eff (dark sector → BBN), wino mass (colliders → gamma line), J-factor region (galaxy → sky), b_A → z† and G_eff.
3. **Server + control panel**: local server with /api/run; a panel per level with its controls and its own chart (n_s–r plane, BBN pulls, Δχ² bars, reach curve, J-factor and σv, finder chart), plus a summary scorecard across categories. Light/dark, phone.
4. **Verify**: tests per level, Playwright desktop + phone, numbers checked against their sources.
