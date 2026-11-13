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
- F(T) = T / √(1 + T/μ) · exp(−nT/(T + m2)): plateau (inflation), cliff at x ≈ m2 (end of inflation), tail.
- Angle coupling to matter: Nieh–Yan, c_A = √(3/8), L ⊃ c_A ∂y · J₅ / M_P; angle period 8 → A = π/4.
- Kick: hidden axion σ with Λ⁴ e^{−A x} [1 − cos(A y − σ/f)] (form of SU(8) gaugino condensation, f = T).
- Matter: lepto-axiogenesis (Weinberg operator, μ_ℓ/μ_A = 0.523, sphalerons 28/79).
- Reheating: instant preheating, g ≈ 0.1, χ decay distance computed → T_RH ≈ 2.1–3.7×10¹⁴ GeV.
- Dark matter: gravity-only (Planckian-interacting) fermion, about 3.5×10⁶–1.9×10⁷ GeV at that T_RH.
- Dark energy: the tail; n ≈ 127 sets its size; μ ≲ 1 puts today's slope at √(2/3) (PURE-TWIST);
  optional dark-matter coupling β (FLAG-1: κ = 1, β ≈ 0.04).
- Late-time versions tested: PURE-TWIST (κ = √(2/3), β = 0; zero extra parameters), K816 (κ = √(2/3), β free),
  FLAG-1 (κ = 1, β free). **The theory's own prediction is PURE-TWIST (β = 0)**: gravity-only dark matter cannot
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
| Supernova-set robustness | locked | `PREREG_DESY5_SWAP.md`, `PREREG_SN_SWAP.md`; `desy5_swap.json`, `sn_swap_union3.json` | DES Y5: PURE −11.19 (STRAINED vs w₀w_a −16.17), FLAG-1 −14.88 (HOLDS); Union3: PURE −5.29 (STRAINED), FLAG-1 −8.87 (HOLDS); K816 (base slope, β 0.030) on DES Y5: −12.79, **HOLDS** (`desy5_k816.json`); Dovekie: PURE −5.06, FLAG-1 −7.38 vs w₀w_a −8.78, both **HOLD** (`sn_swap_dovekie.json`); K816 on Union3: −7.28, **HOLDS** (`sn_k816_union3.json`); K816 on Dovekie running |
| Matter asymmetry | derived + chosen + estimate | `theory/matter/`, matter doc D35–D50 | observed amount for m_σ ≈ 3×10¹⁰ GeV at heat share 1.5%; at the computed share (~0.1%) ≈ 6×10⁹ GeV (check running); yield is not monotonic in the heat share |
| Reheating | derived (g, h chosen) | `theory/inflation/reheating_derived.py`, `chi_decay_distance.py` | 0.04–0.4% heat at g = 0.1; T_RH 2.1–3.7×10¹⁴ GeV |
| Dark matter, gravity-only fermion | estimate | `pidm_abundance.py`, `dm_inflation_production.py` | 3.5×10⁶–1.9×10⁷ GeV |
| w_a ceiling ≥ −0.40 | locked | `PREREG_WA_CEILING.md`, `effective_w.json` | pending DESI DR3 (today's −0.73 would be a tension) |
| w_a for the theory's own β = 0 version | derived | `theory/darkenergy/tail_bend_wa.py` | between about −0.15 and 0 (w₀ ≥ −0.90); the tail's bend only moves w toward −1 |
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
- **Withdrawn numbers:** the hidden mass 3–6×10⁹ GeV (a pre-stated check failed; corrected to ~3×10¹⁰ GeV);
  several earlier developments (D26 gravitino, D31) superseded. All kept in the matter doc and git history.

## 4. Assumptions a reviewer should challenge

0. The data mildly prefer a dark-matter coupling β ≈ 0.03 that the theory does not produce (Development 64).
1. μ ≲ 1 (tail on its slope today) was chosen knowing PURE-TWIST was preferred; only new data (DESI DR3) can test it.
2. The hidden SU(8) is matched in form (gaugino-condensation cross term), not constructed in full.
3. Heavy superpartners (m ≈ 10¹¹–10¹³ GeV) at T_RH need R-parity violation (window 10⁻⁵–10⁻³, estimate).
4. Instant preheating: χ's couplings g ≈ 0.1 and Yukawa h = 0.1–1 are natural choices, not derived.
5. The dark-matter fermion argument and PIDM threshold factor are estimates.
6. Compressed CMB likelihood (θ*, ω_b, ω_b + ω_c) in TOURNAMENT-family tests; full-likelihood tests are V6 and NS-PURE.

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
