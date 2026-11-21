# The Weave test battery: every major test a physicist would throw at it (v1, 21 Nov 2026, 16:55 CT)
Danny 16:47: "every major astrophysics, quantum physics test that's currently being … or is currently constructed … set them up and test the equation."
Danny 16:48: three fields in tandem (UFE v4 §7).

Each test is tagged with the field it probes:
- **S**: dilaton, time and cosmology
- **T**: volumes, forces and scales
- **U**: matter and flavour
- **S–T, T–U, S–U**: the interfaces between them

That way a failure points to its own term.

**Status:**
- **RUN**: the Weave has a number and the data exist, so it can be scored now.
- **FUT**: the Weave has a number and the experiment is future, so lock it now.
- **NEED**: the Weave has no number yet. A referee would flag this, so a derivation is owed.
- **DONE**: already scored.

**Rule for each RUN test:**
1. Fetch the current data value from three sources and triangulate it (Rule 6h; consensus means within 0.3 dex or 1σ).
2. Lock it (PREREG + sha256).
3. Score it.
4. Fingerprint it into the compass.

Only post-lock data counts as strict evidence (G6).

## A. Cosmology (S and S–T)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| A1 | n_s | Planck PR4 + ACT DR6 + SPT-3G; CMB-SPA + DESI | 0.9706 | S | DONE (0.8σ) |
| A2 | r | BICEP/Keck BK18 (< 0.036); LiteBIRD, CMB-S4, SO | 5.4e-4 | S | DONE (bound) / FUT |
| A3 | running dn_s/dlnk | Planck, ACT; SPHEREx, CMB-S4 | −9.7e-4 | S | RUN |
| A4 | f_NL (local, equilateral) | Planck PR4; SPHEREx | ≈ 0 | S | RUN |
| A5 | isocurvature | Planck | 0 | S | RUN |
| A6 | ΔN_eff | Planck + ACT; SO, CMB-S4 | 0 | S–T | DONE / FUT |
| A7 | BBN Y_p, D/H | PRIMAT, EMPRESS, Cooke D/H | standard (ω_b input) | S–T | RUN |
| A8 | BBN with late decays (gravitino τ ~ 1.6e-3 s) | Kawasaki–Kohri–Moroi bounds | must pass | S–T | **DONE: PASS** (τ = 1.4e-3 s < 0.1 s, D1946) |
| A9 | lithium-7 | stellar Li | no Weave fix | — | NEED (honest null) |
| A10 | CMB spectral distortions μ, y | FIRAS; PIXIE (proposed) | ≈ ΛCDM | S | RUN |
| A11 | CMB lensing amplitude A_L | Planck, ACT DR6 | standard | S–T | RUN |
| A12 | BAO distances | DESI DR2 (DR3 later) | ΛCDM plus the thread | S | RUN (thread OPEN) |
| A13 | supernovae | Pantheon+, DES-SN5Y, Union3 | ΛCDM plus the thread | S | RUN (thread OPEN) |
| A14 | w₀–w_a | DESI + CMB + SNe | needs λ ≈ 0.95 | S | NEED (non-Kähler thread) |
| A15 | H₀ tension | SH0ES vs Planck | not resolved | S | RUN (honest null) |
| A16 | S₈ tension | KiDS, DES Y6, HSC, Euclid | not resolved | S–T | RUN (honest null) |
| A17 | Σm_ν | DESI + CMB; KATRIN, Project 8 | 0.0587 eV (NO) | U | RUN |
| A18 | baryon asymmetry η_B | Planck ω_b | non-thermal leptogenesis | S–T | NEED (ring 3) |
| A19 | dark-matter relic Ω_DM | Planck | asymmetric 12.8 GeV plus winos 10–40 % | S–T | RUN |
| A20 | stochastic GW background | NANOGrav 15-yr, IPTA, EPTA; LISA | no walls, no strings | S–T | RUN |
| A21 | cosmic strings (D-strings, Gμ) | Planck, PTA | must pass Gμ bounds | S–T | NEED |
| A22 | cosmic birefringence β | ACT + Planck (0.3°); LiteBIRD | carrier unsettled | S–T | NEED |
| A23 | 21 cm / reionisation | HERA, SKA | standard | — | FUT |
| A24 | primordial black holes, magnetic monopoles | microlensing, MACRO, IceCube | none (inflation dilutes) | S | RUN |

## B. Particle physics and colliders (T, T–U)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| B1 | α_s(M_Z) | PDG world average 0.1180 ± 0.0009 | 0.1142 | S–T | DONE (**FAIL −4.2σ**) |
| B2 | sin²θ_W and α at M_Z | PDG | inputs to the running | T | DONE (inputs) |
| B3 | Higgs mass 125.1 GeV | ATLAS, CMS | split SUSY, tan β 1–4 | T | RUN |
| B4 | Higgs couplings and self-coupling | LHC Run 3, HL-LHC | SM-like (heavy scalars) | T | RUN / FUT |
| B5 | wino, disappearing tracks | ATLAS (660 GeV, 2201.02472); ATLAS + CMS ~700 GeV (2507.15934) | 0.687 TeV | T | **INDETERMINATE**: on the edge (D1947) |
| B6 | gluino searches | ATLAS, CMS | 4.93 TeV | T | RUN |
| B7 | W mass (CDF vs ATLAS/CMS) | PDG | SM-like | T | RUN |
| B8 | muon g−2 | FNAL final (2025) + lattice | SM-like (PeV scalars) | T | RUN |
| B9 | electron g−2 and α | Harvard, Berkeley/Paris | SM | T | RUN |
| B10 | proton decay | Super-K (e⁺π⁰ > 2.4e34 yr, K⁺ν̄); Hyper-K, DUNE | 1.6e35 yr (G-branch) | T | DONE / FUT |
| B11 | vacuum stability (m_t, m_h) | PDG | stable with PeV scalars | T | RUN |
| B12 | top mass | PDG | input | — | — |
| B13 | magnetic monopoles from GUT breaking | MACRO, IceCube | none | T | RUN |

## C. Flavour and precision (U, T–U)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| C1 | quark masses and CKM | PDG, FLAG, CKMfitter, UTfit | one spurion, natural | U | DONE (PHEN) |
| C2 | CKM first-row unitarity | superallowed β, K_ℓ3 | SM | U | RUN |
| C3 | B_s → μμ, b → sℓℓ | LHCb, CMS | SM | T–U | RUN |
| C4 | μ → eγ, μ → 3e, μ–e conversion | MEG II, Mu3e, Mu2e, COMET | suppressed (PeV sleptons) | T–U | RUN |
| C5 | K → πνν̄ | NA62, KOTO | SM | T–U | RUN |
| C6 | ε_K, ΔM_{d,s} (SUSY FCNC) | lattice + data | suppressed (PeV) | T–U | RUN |
| C7 | neutron EDM | PSI n2EDM | θ̄ = 0 ⇒ ~1e-32 | U | DONE (lock) / FUT |
| C8 | electron EDM | ACME III, JILA HfF⁺ | 5e-34 – 4e-33 | T–U | RUN (bound) |
| C9 | atomic parity violation (Cs) | Wood et al., new measurements | SM | T | RUN |
| C10 | Koide, m_τ | Belle II, BESIII | Q = 2/3 | U | RUN |
| C11 | QCD axion searches | ADMX, HAYSTAC, CASPEr | no QCD axion needed (θ̄ = 0) | U | RUN (predicts null) |

## D. Neutrinos (U, S–U)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| D1 | sin²θ₁₂ (TM1) | NuFIT 6; JUNO | 0.3184 | U | RUN / FUT (the decisive one) |
| D2 | θ₂₃, θ₁₃, δ_CP | NuFIT; T2K, NOvA, DUNE, Hyper-K | TM1 curve, δ 255–295° | U | RUN |
| D3 | mass ordering | JUNO, DUNE, ORCA | normal | U | FUT |
| D4 | 0νββ | KamLAND-Zen (< 28–122 meV), LEGEND-200/1000, nEXO | 1.6–3.8 meV | U | RUN / FUT |
| D5 | β-decay mass | KATRIN (< 0.45 eV), Project 8 | 8.8 meV | U | RUN |
| D6 | sterile neutrinos | MicroBooNE, SBN, KATRIN | none | U | RUN |
| D7 | astrophysical ν, SN1987A, IceCube | — | standard | — | RUN |

## E. Dark matter and the dark sector (S–T, T)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| E1 | direct detection, 12.8 GeV | LZ 2024/25, XENONnT, PandaX-4T; XLZD | below LZ; in XLZD reach | T | RUN |
| E2 | wino indirect: γ-lines | H.E.S.S. GC, Fermi; CTA | wino 10–40 % of the DM at 0.69 TeV | T | **OPEN**: H.E.S.S. 1808.04388 is not valid below 1 TeV; signal ∝ f² = 0.01–0.16; the Fermi dwarf limit is next (D1946) |
| E3 | wino indirect: dwarf continuum | Fermi-LAT dwarfs, MAGIC | — | T | RUN |
| E4 | antiprotons | AMS-02 | — | T | RUN |
| E5 | DM self-interaction σ/m | clusters, dwarfs | ≤ 2e-3 cm²/g | T | DONE |
| E6 | dark photon 0.3–12.8 GeV | BaBar, Belle II, NA64, LHCb; SHiP | window | T | RUN |
| E7 | small-scale structure (Lyα, satellites) | Lyα forest, DES dwarfs | cold (12.8 GeV) | S–T | RUN |
| E8 | CMB DM annihilation/decay energy injection | Planck | asymmetric ⇒ none; winos? | S–T | RUN |
| E9 | neutron lifetime anomaly (dark decay) | UCNτ, BL3 | none | U | RUN |

## F. Gravity and fundamental symmetries (S, S–T)
| # | test | experiment / data | Weave value | field | status |
|---|---|---|---|---|---|
| F1 | equivalence principle | MICROSCOPE (\|η\| < 1e-15); MICROSCOPE-2 | no violation (thread sequestered) | S–T | RUN |
| F2 | PPN γ, β | Cassini (\|γ−1\| < 2.3e-5), LLR, Mercury | GR (the Kähler thread is excluded) | S–T | RUN |
| F3 | Ġ/G | LLR, pulsars, BBN | ≈ 0 | S | RUN |
| F4 | short-range gravity | Eöt-Wash (~50 μm) | moduli are heavy ⇒ none | T | RUN |
| F5 | α drift | Al⁺/Hg⁺ clocks, Yb⁺ E3/E2, ESPRESSO quasars | ζ = 3.8e-10 | S–T | RUN |
| F6 | GW speed | GW170817 (\|c_g/c − 1\| < 1e-15) | c | S | RUN |
| F7 | GW polarisations, ringdown | LIGO-Virgo-KAGRA O4 | GR | S | RUN |
| F8 | Lorentz invariance | Fermi GRB, LHAASO | exact | S | RUN |
| F9 | black-hole superradiance (ultralight axions) | spin measurements | photon-axion m 1e-33 eV: outside | S–T | RUN |
| F10 | moduli problem (cosmological moduli) | BBN, CMB | moduli heavy (m ~ m₃/₂ or above) | T | **DONE: PASS** (lightest ≥ 2.6e5 GeV, D1946) |
| F11 | swampland / TCC | theory | flags (r, dS) | S | DONE (flags) |

## G. Quantum and laboratory
| # | test | experiment | Weave value | field | status |
|---|---|---|---|---|---|
| G1 | CPT tests (antihydrogen, K mesons) | ALPHA, BASE | exact | — | RUN |
| G2 | quantum-gravity phenomenology (spacetime foam, decoherence) | Fermi, MAGIC, interferometers | none at accessible scales | S | RUN |
| G3 | fifth-force atom interferometry | MAGIS, AION | thread sequestered | S–T | FUT |

## Order of work (centre outwards, cheapest decisive first)
1. **Classic "you missed this" checks:** E2 (wino γ-lines), A8 (BBN with late gravitino decays), F10 (moduli problem), B3/B11 (Higgs mass and stability), B8 (muon g−2), C4/C6 (SUSY flavour), A21 (cosmic strings).
2. **The NEED items:** A14 (the thread), A18 (η_B), A22 (birefringence).
3. **The remaining RUN tests**, 3 per tick.

Every result is fingerprinted into the compass with its field tag.
