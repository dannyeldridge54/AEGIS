# The Twist — guide for professional reviewers

Author: Danny Eldridge (independent researcher). Analysis and code were AI-assisted (Anthropic's Claude); every
number below comes from a script and a result file in this repository. Branch: `unify-bg`. Date: 13 November 2026.

**Read in this order:** (1) this guide; (2) the paper, `Twist_one_field_2026-11-13.pdf` (Zenodo draft); (3)
`CURRENT_MODEL.md` (every locked result, newest last). Older material in the repository (EDE "Locked Twist",
TorsionΛ, UFE, n = 3 early field) is superseded unless listed here.

---

## 1. The model in ten lines

- Field: one chiral superfield T = x + i y built from the Barbero–Immirzi parameter (Gates–Ketov–Yunes form);
  x = exp(√(2/3) φ). Kähler potential K = −3 ln(T + T̄ − S S̄) (no-scale, α = 1).
- Superpotential W = √3 m S F(T); along S = 0: V = m² |F(T)|² / (4x²), m ≈ 5×10¹³ GeV from A_s.
- F(T) = T / √(1 + T/μ) · exp(−n(1 − e^{−πT/4})): plateau (inflation), cliff at x ≈ 0.01 (end of inflation), tail.
  (Cliff factor reshaped 13 Nov from exp(−nT/(T + m2)) after TAIL-F; Development 79.)
- Angle coupling to matter: Nieh–Yan, c_A = √(3/8), L ⊃ c_A ∂y · J₅ / M_P; angle period 8 → A = π/4.
- Kick: hidden axion σ with Λ⁴ e^{−A x} [1 − cos(A y − σ/f)] (form of SU(8) gaugino condensation, f = T).
- Matter: lepto-axiogenesis (Weinberg operator, μ_ℓ/μ_A = 0.523, sphalerons 28/79).
- Reheating: instant preheating, g ≈ 0.1, χ decay distance computed → T_RH ≈ 2.1–3.7×10¹⁴ GeV.
- Dark matter: gravity-only (Planckian-interacting) fermion, about 1×10⁸–6×10⁸ GeV at that T_RH once the kination phase
  is included (3.5×10⁶–1.9×10⁷ GeV without it; Development 85, estimate).
- Dark energy: the tail; n ≈ 127 is **chosen** to give its size (not predicted, Development 74); μ ≲ 1 puts today's slope at √(2/3) (PURE-TWIST);
  optional dark-matter coupling β (FLAG-1: κ = 1, β ≈ 0.04).
- Late-time versions tested: PURE-TWIST (κ = √(2/3), β = 0; zero extra parameters), K816 (κ = √(2/3), β free),
  FLAG-1 (κ = 1, β free). **The theory's own prediction is PURE-TWIST (β = 0)** — with one condition found 13 Nov (Development 78): the
  slope √(2/3) holds only if the field freezes far down the tail (heat share ≲ 0.01%); at the computed heat share 0.13%
  the cliff's leftover steepens today's tail: w₀ ≈ −0.74, w_a ≈ −0.34 (full tail shape, Development 78b; the heat
  share picks a point on one (w₀, w_a) curve). Also: gravity-only dark matter cannot
  couple to the twist field, and natural modular weights give β = 0 or |β| ≥ 0.41 (Development 64). K816's small
  β ≈ 0.03 is a data preference the theory does not explain (it holds on DES Y5 and Union3, where PURE-TWIST is
  strained). FLAG-1's κ = 1 is not the base slope.

## 2. Status of each claim

Labels: **derived** (follows from the base theory), **chosen** (a modelling choice, stated), **fitted** (from data),
**estimate** (order of magnitude), **locked** (pre-registered test, rule hashed before its data).

| Claim | Label | Evidence | Status |
|---|---|---|---|
| α = 1 field space, slope √(2/3) | derived | Gates–Ketov–Yunes; `theory/` | base input |
| n_s 0.963–0.965, r 0.0034–0.0040 | derived, locked | `PREREG_TWIST_INFLATION.md`, `twist_inflation.json` | r pending; n_s: agrees with Planck PR4 + DESI (ΛCDM 0.9635, `ns_pure.json`), ~4σ from CMB-SPA + DESI 0.974 |
| Late universe, PURE-TWIST | locked | `PREREG_PURE_TWIST.md`, `pure_twist.json` | **PREFERRED** (Δχ² −3.37, compressed likelihood); full PR4 likelihood Δχ² −3.85 (`ns_pure.json`) |
| Flagship FLAG-1 on Planck PR4 | locked | `PREREG_V6_PR4.md`, `selfcheck_v6.json` | **HOLDS ON PR4** (Δχ² −7.81) |
| Supernova-set robustness | locked | `PREREG_DESY5_SWAP.md`, `PREREG_SN_SWAP.md`; `desy5_swap.json`, `sn_swap_union3.json` | DES Y5: PURE −11.19 (STRAINED vs w₀w_a −16.17), FLAG-1 −14.88 (HOLDS); Union3: PURE −5.29 (STRAINED), FLAG-1 −8.87 (HOLDS); K816 (base slope, β 0.030) on DES Y5: −12.79, **HOLDS** (`desy5_k816.json`); Dovekie: PURE −5.06, FLAG-1 −7.38 vs w₀w_a −8.78, both **HOLD** (`sn_swap_dovekie.json`); K816 on Union3: −7.28, **HOLDS** (`sn_k816_union3.json`); K816 on Dovekie: -8.02, **TWIST HOLDS ON DOVEKIE** (`sn_k816_dovekie.json`) |
| Matter asymmetry | derived + chosen + estimate | `theory/matter/`, matter doc D35–D50 | at the computed heat share (0.13%) a pre-stated check gave 0.87× at m_σ = 6×10⁹ GeV (predicted 1.0×), so m_σ ≈ 5×10⁹ GeV for 1× (`confirm_f0013_m6e9.txt`); yield is not monotonic in the heat share |
| Reheating | derived (g, h chosen) | `theory/inflation/reheating_derived.py`, `chi_decay_distance.py` | 0.04–0.4% heat at g = 0.1; T_RH 2.1–3.7×10¹⁴ GeV |
| Dark matter, gravity-only fermion (see D106: the reheating field's fermion partner may overproduce it) | estimate | `pidm_abundance.py`, `dm_inflation_production.py`, `dm_kination.py` | 3.5×10⁶–1.9×10⁷ GeV with radiation after reheating; ≈ 1×10⁸–6×10⁸ GeV once kination is included (Development 85) |
| w_a ceiling ≥ −0.40 | locked | `PREREG_WA_CEILING.md`, `effective_w.json` | pending DESI DR3 (today's −0.73 would be a tension) |
| Kination after the cliff adds ~2 e-folds | derived | `theory/inflation/kination_Nstar.py` | n_s 0.9654, r 0.0035 at the computed heat share (instant-reheating 0.9642); with loops (D77) ≈ 0.965–0.968 — an upward systematic found after locking (Development 84) |
| n_s is fixed by the e-fold count | derived | `theory/inflation/kahler_correction_ns.py` | deforming the 3 moves n_s by < 0.002 (α 0.5–5); 0.973 unreachable |
| Neutrinos: normal ordering, Σm_ν 0.059–0.064 eV, Majorana | derived (from the matter mechanism) | Development 69 | testable by JUNO, cosmology, 0νββ |
| w_a for the theory's own β = 0 version | derived | `theory/darkenergy/tail_bend_wa.py` | between about −0.15 and 0 (w₀ ≥ −0.90); the tail's bend only moves w toward −1 |
| Full tail at the computed heat share | locked | `PREREG_TAIL_F.md`, `tail_f.json` | **DISFAVOURED** (Δχ² +29.2); free heat share → 0.01% (PURE-TWIST limit) |
| Birefringence β = 0 | locked | `PREREG_BIREF_NULL.md` | pending; measured 0.28 ± 0.06° (4.9σ tension) |
| Six lab nulls | locked | `PREREG_LAB_NULLS.md` | consistent with all bounds |
| Growth (fσ₈ −3%, E_G +5%) | frozen | `pure_twist_growth.json` | pending DESI full-shape, Euclid |

## 3. Results that go against the model (read these)

- **DATA-GENERATIONS: DOES NOT HOLD.** On pre-DESI BAO + supernova data, FLAG-1 is disfavoured (Δχ² +2.8 and +6.5);
  its preference appears only with DESI-era data (`datagen.json`).
- **DESI-HOLDOUT Test A: ΛCDM PREDICTS DESI BETTER.** Fitted without BAO, FLAG-1 predicts DESI DR2 worse than ΛCDM
  (Δ +12.5); its DESI-era edge comes from fitting DESI, not foreseeing it (`desi_holdout.json`).
- **Look-elsewhere (V7): NOT SIGNIFICANT.** 64 variants were tried on the same data; local 2.6–3.2σ becomes global
  0.7–1.7σ (`v7_look_elsewhere.json`).
- **M1 jackknife: PARTLY CONCENTRATED.** About 60% of FLAG-1's edge sits in DESI's z ≈ 0.71 bin.
- **TOURNAMENT:** no Twist version both predicts held-out BAO and earns its parameter (reading PREDICTS BUT NOT
  PREFERRED). **KAPPA-ALPHA1: NOT PREDICTIVE.**
- **NS-PURE: NO VERDICT** (gate missed by 0.0005); the late-time Twist moves n_s up, not down.
- **TAIL-F: FULL TAIL DISFAVOURED (Δχ² +29.2).** With the computed heat share (0.13%) the cliff's leftover slope
  makes today's dark energy too stiff (w₀ −0.74, w_a −0.34). Freed, the heat share runs to the lower edge (0.01%,
  the PURE-TWIST limit; Δχ² −2.79). PURE-TWIST therefore needs far less heat or a reshaped cliff (`tail_f.json`,
  Development 78b). **Response (Development 79, made after this result):** the cliff factor was reshaped to
  exp(−n(1 − e^{−πT/4})), which leaves inflation identical (n_s 0.9642, r 0.0038) and gives the PURE-TWIST tail at any
  heat share. A post-hoc change: only new data test it.
- **FIFTH FORCE (Development 90): UNSOLVED.** If T is today's dark energy, ordinary matter's mass depends on it
  (β ≈ 0.4 for the sequestered form; no modular weight gives β below Cassini's 3.4×10⁻³), and no standard screening
  mechanism applies to an exponential tail (Development 91). Parking the field in a valley meets the moduli problem unless
  inflation itself ends in the valley (Developments 94–95); the author keeps the light tail and states this as the
  theory's main open problem (decision 13 Nov). The late-time fits assume ordinary matter is uncoupled, i.e. they test the
  tail's shape given a working shield (Development 97); no choice of modular weights provides one (Development 96). Narrowed (Development 103): the coupling comes from putting
  the Standard Model inside the no-scale supergravity; coupled minimally in the Einstein frame it vanishes at tree level, and
  what remains needs a supersymmetry-breaking scale independent of T (e.g. D-term breaking) — open. **Proposed
  resolution (Development 104, estimate):** the Standard Model is not supersymmetric and couples minimally to the
  Einstein-frame metric; then only a χ-loop coupling survives, below Cassini and MICROSCOPE if the χ–SM Yukawa h ≲ 0.05 and
  the SM–χ cutoff is ≲ the GUT scale — or χ reaches the SM only gravitationally, which still reheats (heat share ≈ 0.8%) and makes
  the residue Planck-suppressed (Development 105). The tail's quantum stability then reduces to the field-dependent part of
  the cosmological-constant problem (generic, open). To be confirmed: matter yield at the larger heat share (queued).
- **Withdrawn numbers:** the hidden mass 3–6×10⁹ GeV (a pre-stated check failed; corrected to ~3×10¹⁰ GeV);
  several earlier developments (D26 gravitino, D31) superseded. All kept in the matter doc and git history.

## 4. Assumptions a reviewer should challenge

0. The data mildly prefer a dark-matter coupling β ≈ 0.03 that the theory does not produce (Development 64).
1. μ ≲ 1 (tail on its slope today) was chosen knowing PURE-TWIST was preferred; only new data (DESI DR3) can test it.
2. The hidden SU(8) is matched in form (gaugino-condensation cross term), not constructed in full; its required height
   (~10⁻¹⁸ M_P⁴) is reached without tuning if the hidden branes wrap a separate stabilised cycle of size τ ≈ 30, with
   the gravitino factor m₃/₂/M_P included (Development 70, following arXiv:2303.03414) — an assumption, not derived.
3. Heavy superpartners (m ≈ 10¹¹–10¹³ GeV) at T_RH need R-parity violation (window 10⁻⁵–10⁻³, estimate).
4. Instant preheating: χ's couplings g ≈ 0.1 and Yukawa h = 0.1–1 are natural choices, not derived.
5. The dark-matter fermion argument and PIDM threshold factor are estimates.
6. The helper field S is tachyonic (m_S² ≈ −2H²) with K exactly as written; a standard quartic term ζ(SS̄)² inside
   the log with ζ ≳ 3×10⁴ (m_S²/H² ≈ −2 + 8ζx on the plateau; Development 81) makes it heavy and leaves every number at S = 0 unchanged (Development 72, chosen).
7. Ordinary matter must not feel the tail field: natural bulk weights give a fifth force ×120–360 over Cassini, so
   the Standard Model must be sequestered (D3 branes, T-independent Higgs sector). An assumption (Development 73). And T
   must not be a string volume modulus, or the string scale itself moves with x (β ≈ 0.61, Development 89); even in a pure
   4D supergravity reading, dimensionful matter parameters scale as x^{−1/2}. Kaplunovsky–Louis anomaly terms make
   Λ_QCD move with x for every modular weight but 3/4 (Development 90): no weight shields matter. **The fifth-force
   problem is unsolved — the main open problem of the one-field Twist.**
8. The field moves Δφ ≈ 19–21 M_P from the CMB point to today, in tension with the swampland distance conjecture —
   generic to one-field inflation-plus-quintessence models; open (Development 75).
9. The twist angle y is heavy during inflation (m_y² = 4H²) but tachyonic on the tail for x ≲ 500 (x today ≈ 360 at the computed heat share: mildly, −0.8H²); it is stable
   today only if x today ≳ 3000, which is also what the √(2/3) slope needs — a condition, not yet derived from the
   dynamics (Development 76).
10. The reheating field χ must be supersymmetric, or its loop energy destroys the plateau; with it, n_s shifts by
   about +0.002 (estimate, Development 77).
11. Today's slope depends on reheating (Development 78): PURE-TWIST's √(2/3) needs heat share ≲ 0.01%; at the
   computed 0.13% the full tail gives w₀ ≈ −0.74, w_a ≈ −0.34 (D78b). A correction to Backlog L, which kept only the μ factor.
12. The cliff factor exp(−n(1 − e^{−πT/4})) (Development 79) was chosen after TAIL-F; its SU(8)-condensate form and
   period-8 angle are motivation, not derivation.
13. Quantum stability of the tail (Development 80): tree level is safe (no-scale cancels any constant W₀), but any
   particle heavier than ~6 meV with an x-dependent mass would swamp the tail through loops. Needs the SM and the
   superpartners sequestered from T — not shown; the generic quintessence (Kolda–Lyth) and cosmological-constant
   problems.
14. Link to loop quantum gravity (Development 83): the Barbero–Immirzi superfield is from the literature; its
   identification with the whole model's modulus, W and F are assumptions. Today the angle sits at y = 0, so the
   field does not take LQG's black-hole value γ ≈ 0.24 under the mapping used before (1/γ = y/x) — an open mismatch.
15. Compressed CMB likelihood (θ*, ω_b, ω_b + ω_c) in TOURNAMENT-family tests; full-likelihood tests are V6 and NS-PURE.

## 5. How to reproduce

- Rules: `field_tests/rules/PREREG_*.md` with `.sha256`; each lock is a git commit made before the run (check with
  `git log --format='%h %ci' -- field_tests/rules/<RULE>`). Deviations: `*_DEVIATIONS.md`, each written before a rerun.
- Late-time (cloud): AxiCLASS build with the coupled scalar field (`cmb-fit/axiclass`, `field_tests/missing_piece`);
  `python tournament.py`, `pure_twist.py`, `desy5_swap.py`, `sn_swap.py` (SNSET=UNION3|DOVEKIE), `pure_mcmc.py`.
- Full CMB (PC): Cobaya + Planck PR4 NPIPE CamSpec; `field_tests/selfcheck/v6_pr4_fit.py`, `ns_pure_fit.py`.
- Theory: `theory/inflation/*.py`, `theory/matter/*.py`, `theory/darkenergy/*.py` (plain Python + SciPy).
- Data: Cobaya packages (Planck 2018/PR4, DESI DR2 BAO, Pantheon+, DES Y5, Union3, DES-Dovekie).

## 6. What would falsify the model

n_s confirmed ≈ 0.973 by Simons Observatory; r < 0.002 or > 0.008 (95%) once σ(r) ≤ 0.002; DESI DR3 w_a + 3σ <
−0.40; a calibration-independent birefringence ≥ 5σ; a confirmed fifth force, equivalence-principle violation,
α drift or dark-matter detection.
