# The Weave — full test plan (21 Nov 2026)
Danny 08:13: "list all the tests we're going to need … when a tick is null, work on the tests and get them prepared."
Rule for every test: a PREREG lock (prediction, data, pass/fail threshold) is committed BEFORE the data or the computation; scored ONLY on data released after the lock counts as strict evidence.
Toolkits we already have: **Janus** (inflation, N*, late-time thread), **Hyperion** (BBN, galaxy γ-line, neutron stars), **CERN+1** (lhc_xsec / lifetime / dt_limit / future), **Flavour panel**, **Weave Control** engine (all levels at once), **evidence atlas** (strict count), **CubeMind** (self-derivation + data pool), **Mapper** (sky).
Status: **R** ready (tool + lock exist) · **L** tool ready, lock to write · **T** tool to build · **W** waiting for data.

## A. Early universe
| Test | Weave number | Data / experiment | Tool | Status |
|---|---|---|---|---|
| A1 tensor ratio r | 5.41e-4 (10D); 5.7–5.9e-4 with τ_q (J1); 1.07e-3 if 6D | BICEP/Keck now; SO, LiteBIRD (σ_r ≈ 5e-4–1e-3) | Janus, weave_rladder | R (W for LiteBIRD) |
| A2 running α_s | −9.7e-4 | CMB-S4 / SPHEREx (σ ~ 1e-3) | Janus | L → **R** (21 Nov 10:22: PREREG_A2_RUNNING locked, band −1.05e-3 to −0.95e-3) |
| A3 n_s | FITTED — not a test | — | — | — |
| A4 f_NL | ≈ 0 (single field) | Planck, SPHEREx | Janus | L |
| A5 isocurvature | ≈ 0 | Planck PR4 | Janus | R |
| A6 ΔN_eff | ≈ 0 (brane split) | ACT/SPT now; SO, CMB-S4 (σ ≈ 0.03) | Hyperion BBN + engine | L → **R** (21 Nov 10:23: PREREG_A6_NEFF — ΔN_eff = 0 if ε ≥ 1.5–9.5e-11, else ≤ 0; never positive; FAIL if > 0 at 3σ) |
| A7 Y_p, D/H | standard at ω_b | PRIMAT + Planck | hyperion_bbn | R |
| A8 Li-7 | postulate C7 (stellar depletion) | stellar Li surveys | — | T |
| A9 no modular domain walls | no nHz wall signal (D1753 R3) | NANOGrav 20-yr, IPTA DR3 spectral shape (SMBH vs walls) | to build: wall-spectrum template | T |
| A10 large-scale CMB cut | none needed (D1753 R4) | Planck PR4 low-ℓ | Janus | L |

## B. Flavour, quarks, leptons
| Test | Weave number | Data | Tool | Status |
|---|---|---|---|---|
| B1 Koide Q | 2/3 (needs |ε| ≲ 6e-5 at ρ) | m_τ (Belle II, BESIII) | weave_koide / slip | L |
| B2 TM1 sin²θ₁₂ | 0.3184 | JUNO 6-yr (±0.0015) | Flavour panel | L (strongest near-term test, ~6σ if centre holds) |
| B3 δ_CP branch | lower branch at s²₂₃ 0.561 | DUNE, Hyper-K | Flavour panel | L → **R** (21 Nov 10:24: PREREG_B3_DCP_FUTURE, δ ∈ 255–295° on the TM1 curve) |
| B4 Σm_ν | 0.0587 eV (NO, m₁ = 0) | DESI DR3 + CMB; KATRIN/Project 8 | engine flavour | L → **R** (21 Nov 10:23: PREREG_B4_SUMMNU — scored in w0waCDM; FAIL if 95 % limit < 0.055 eV, Σ > 0.10 eV at 3σ, or IO at 3σ; m_β = 8.8 meV) |
| B5 0νββ m_ββ | 1.59–3.80 meV (D1755; fail if a signal > 7.6 meV) | LEGEND-1000, nEXO ⇒ predict NULL | weave_mbb | R (locked PREREG_B5) |
| B6 CKM fit | hosted (best 1.82, rung 4) | PDG/CKMfitter | weave_ckm, pool | L (locked re-check of the 1.82 point) |
| B7 R_μμ / b→sμμ | = SM | LHCb Run 3 | engine quarks | R |
| B8 θ̄ = 0 ⇒ neutron EDM | d_n from CKM only (~1e-32 e·cm) | n2EDM (PSI), ~1e-27 | to build | T |
| B9 electron EDM | unobservable (~1e-40) | ACME III, JILA | to build | T |
| B10 proton decay | safe | Hyper-K, DUNE | — | L |
| B11 gauge couplings | D3 at ρ fails ×28 ⇒ visible on D7 (D1753 R1) | α_s, sin²θ_W, α | to build: RG + Kähler-volume tool | T |

## C. Dark sector
| Test | Weave number | Data | Tool | Status |
|---|---|---|---|---|
| C1 12.8 GeV asymmetric DM, direct detection | σ_SI below LZ, inside XLZD reach for ε near the ceiling | LZ, XENONnT, XLZD | Hyperion galaxy / engine | L |
| C2 dark photon | 0.3–12.8 GeV, ε 1e-11 – LZ ceiling | SHiP, NA64, Belle II | to build: dark-photon window tool | T |
| C3 DM self-interaction σ/m | computable from α_D ≥ 4.7e-4, m_A′ | cluster/dwarf bounds (σ/m < ~1 cm²/g) | to build (arXiv:1403.1077 formulas) | T → **R** (weave_sidm; 21 Nov 10:22: at α_D = 0.022, σ/m ≤ 2e-3 cm²/g for every m_A′, D1795) |
| C4 no galactic-centre DM annihilation | asymmetric ⇒ none | Fermi GCE | — | L → **R** (21 Nov 10:24: PREREG_C4_NO_ANNIHILATION) |
| C5 wino 0.67–1.0 TeV | disappearing tracks; γ-line | ATLAS/CMS Run 3, HL-LHC; CTA | lhc_*, galaxy γ-line | R |
| C6 no dark neutron decay | none (D1753 R6) | UCNτ, BL3 beam | — | L → **R** (21 Nov 10:24: PREREG_C6_NO_DARK_NEUTRON) |

## D. Late universe and gravity
| Test | Weave number | Data | Tool | Status |
|---|---|---|---|---|
| D1 thawing thread w0, wa | w0 ≈ −0.79 | DESI DR2/DR3, Euclid | Janus late, engine | R |
| D2 negative space z† | conditional (coupling not detected) | Lyα BAO z 2–3 (DESI) | weave_negspace | L |
| D3 α drift | ζ ≲ 3.6e-6 needed ⇒ thread sequestered or axion-like | atomic clocks, quasar spectra (ESPRESSO) | Janus clocks | R |
| D4 equivalence principle | no violation | MICROSCOPE-2 | — | L → **R** (21 Nov 10:24: PREREG_D4_EQUIV, |η| < 1e-18) |
| D5 cosmic birefringence (21 Nov 10:22: carrier is now the photon-axion on its OWN cycle ≈ 36–39, m 1e-33–9e-32 eV, c_γ ≈ 4.2/Δθ — D1793–D1795; the thread is sequestered) | bridge β² = 2.5e-3 (c_γ/f)²(1+w0) deg² ⇒ c_γ/f ≈ 12 at β = 0.277°; ratio β_reio/β_rec = 0.997–0.999 (locked D404) | ACT+Planck now; LiteBIRD (both bumps) | bridges D403/D404 | R (thread must be axion-like with c_γ/f ≈ 12; LiteBIRD ratio test) |
| D6 GW speed = c, no extra polarisations | standard | LIGO-Virgo-KAGRA | — | L |
| D7 Hubble / S8 tensions | not resolved by the thread | SH0ES, JWST, DES/KiDS | Janus | L (honest null) |

## E. Matter, nuclei, atoms, chemistry
| Test | Weave number | Data | Tool | Status |
|---|---|---|---|---|
| E1 m_p response to quark slips | σ_πN, σ_s propagation | lattice QCD | weave_proton | R |
| E2 atomic/molecular constants | follow from α, m_e, m_p | CODATA | weave_atomic | R |
| E3 nuclear window (deuteron binding, Hoyle state) | the Weave's quark-mass freedom must stay inside | nuclear lattice EFT | to build | T |

## F. Whole-model tests
| Test | Data | Tool | Status |
|---|---|---|---|
| F1 every level at once (one consistent knob set) | all above | Weave Control engine + CubeMind pool | R (running, 17k+ universes) |
| F2 strict evidence count | only post-lock data | evidence atlas | R |
| F3 joints (every shared number agrees) | — | joint audit (D1750–D1752) | R |

**Next to prepare on null ticks (in order):** D5 birefringence bridge tool + lock · B5 m_ββ tool + lock (predict NULL for LEGEND/nEXO) · B2 JUNO lock refresh · C3 σ/m tool · B11 gauge-coupling (D7 volume) derivation · A9 wall-spectrum template · B6 locked re-check of the 1.82 CKM point.

## Y. Flavour model-building tests (added 21 Nov 10:22)
| Test | Result | Status |
|---|---|---|
| Y1–Y3 theta/orbifold/hosting | D1783–D1785 | done |
| Y4 odd flux M=9 Z₃ at ρ, Haar Higgs | FAIL (not natural; r₂₃ ≥ 0.20) | done (D1790) |
| Y4b same, optimised Higgs | HOSTED (exact fit, all 9 pairs) | done (D1792) |
| Y5 T²/Z₂ at ω, 4-4-8 | HOSTED (tuned fit; control passes) | done (D1791) |
| Y6 (future) | a symmetry that fixes the Higgs direction ⇒ 0-parameter lepton test | T (no mechanism in the literature, D1796) |

**21 Nov 10:22 corrections:** Λ is an INPUT (D1795: the dark-cycle axion oscillates, m ≈ 64 H₀), so no Λ-size test exists; the twin-cycle tie (forces = birefringence = α_D) is broken (D1793) and is not a test any more.
