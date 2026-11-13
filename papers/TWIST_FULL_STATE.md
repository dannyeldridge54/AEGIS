# The Twist — the full state of the theory (13 Nov 2026, 13:45 CT)

One field — the Barbero–Immirzi parameter promoted to a supergravity superfield T — is asked to run inflation, end it, heat the
universe, make matter, and act as today's dark energy. This document follows it from the beginning to now, link by link, and
says for each link what is derived, what is assumed, what is tested, and what is open. Development numbers (D…) point to
theory/pending_docs/D72_D75_weak_spots.md; the model card (papers/MODEL_CARD_v5.md) holds the numbers.

---

## 0. The shape everything lives on

- **Field space.** K = −3 ln(T + T̄): a hyperbolic disk (Poincaré disk) of fixed curvature. It is rung 3α = 3 of the seven
  allowed rungs of maximal (N = 8) supergravity / M-theory, whose geometry is built on the octonions (Fano plane). (D138)
- **The cliff's variable.** In q = e^{−πT/4} the field space is exactly one disk: rim = the inflation plateau, centre = today's
  dark energy. The whole history is one inward spiral, rim → centre. (D139) In heterotic-string language q is the modular nome
  e^{−2πT_het}. (D153)
- **Symmetries.** Scaling T → λT and shift T → T + ic (the disk's isometries); an 8-fold repeat of the angle (Z₈); a mirror Z₂
  (S → −S). π enters structurally: everything switches off as e^{−πx/4}.
- **Dimensions.** T and the helper field S give 4 real dimensions with two angles: a 2-torus over a 2-d base.

## 1. The model

| Piece | Form | Status |
|---|---|---|
| Kähler potential | K = −3 ln(T + T̄ − SS̄(1 + (T+T̄)/2μ) + ζ(SS̄)²) | rung 3 (geometric); μ, ζ chosen |
| Superpotential | W = √3 m S T exp(−n(1 − e^{−πT/4})) | from a Z₂ racetrack of two hidden groups (D126) |
| Cliff exponent π/4 | 2π/8 (SU(8)); also the heterotic nome q | assumed; SU(8) weakly coupled if f = f₀ + T, f₀ ≳ 2 (D148) |
| Cliff depth n | ≈ 125 | **chosen** — a tuning of today's dark energy; cannot come from thresholds (D153) |
| Inflaton mass m | 2.1×10⁻⁵ M_P | set by data; related to a weak gauge coupling with a ~7% cancellation (D126, D136) |
| Reheating field χ | W ⊃ (h/2)(1 − e^{−2π(T−T₀)})χ² | assumed form; keeps the tail quantum-stable (D118) |
| Standard Model | neutral under the disk's isometries | the shield (D140–D142); candidate home: heterotic Z₃ (D152) |

## 2. The history, link by link

| Era | What happens | Status |
|---|---|---|
| Start | field near rest on the plateau, x ≈ 10⁻⁵–10⁻⁴ | assumed; fast starts excluded (S unstable there, D136); lumpy starts robust by analogy (D122) |
| Inflation | slow roll on the disk's rim | **derived**: N* 55.7–57, n_s 0.964–0.965 (loop shift negligible, D156), r ≈ 0.0036 |
| End | the cliff (x ≈ 0.01) | derived from W |
| Heating | χ's mass passes zero; instant preheating; ~0.8% of the energy becomes heat | derived from the assumed χ form (D105, D118, D121) |
| Hand-off to matter | χ decays to the Higgs via Planck-scale links | assumed (generic in quantum gravity, D110) |
| Matter | hidden axion σ kicks the angle; lepto-axiogenesis | mechanism derived; m_σ refit ≈ 6×10¹⁰ GeV, **confirmation running**; prediction at 0.8% heat MISSED (D124) |
| Dark matter | gravity-only fermion from χ̃ decays, ~100–500 TeV | conditional; out of the predictions table |
| Hidden leftovers | SU(8) glueballs decay before nucleosynthesis | estimate, fine (D98) |
| Nucleosynthesis → galaxies | standard physics | nothing new |
| Freezing | field stops at x ≈ 73 (at 0.8% heat) | derived |
| Today | thaws to x ≈ 89; dark energy w0 −0.90, wa −0.14 | **derived**; insensitive to heat share (D125); independently reproduced by the referee |

## 3. The fifth force — the hardest link, now built

1. **Problem.** A light dark-energy field normally pushes on ordinary matter (β ~ 1; Cassini needs < 3.4×10⁻³).
2. **Shield (D140–D142).** If ordinary matter is neutral under both isometries of the disk, only symmetry-breaking effects
   couple: the cliff's instanton (passes every test — quasars, Oklo, nucleosynthesis, clocks, MICROSCOPE — by 10¹⁹ or more) and
   perturbative leaks, which atomic clocks force to fall as 1/x⁴ or faster.
3. **Signature (locked, PREREG_SHIELD).** Any leak has one redshift shape: ~78% of the change after z = 1, nothing new above
   z ≈ 3, clocks tied to quasars.
4. **Where it can live.** Type IIB volume moduli fail at leading order (Burgess–Quevedo; D150–D151). The heterotic Z₃ orbifold
   keeps matter neutral: string scale set by the dilaton, no T-dependent gauge thresholds, untwisted masses T-independent,
   twisted ones instanton-suppressed (D152). Open: dilaton stabilisation; higher-order corrections.
5. **The frontier (D154).** No known string setting gives all three needs at once: rung 3 (A), a hidden gauge function linear in T
   for the cliff (B), and matter neutral under T (C). IIB volume: A+B, not C. Heterotic Z₃: A+C, not B. Heterotic M-theory: B, not C.
   Fibre moduli: C, not A.

## 3b. TWIST-K — the same model with no hidden forces (D159–D161)
The cliff can sit in the helper field's Kähler metric instead of the superpotential: K ⊃ E(u) SS̄ with E = exp(2n(1 − e^{−πu/8})),
W = √3 m S T. Full supergravity check: the potential along the inflaton's path equals the Twist's to 10 digits; S stays heavy; the
angle stays at +4H² everywhere (no cliff tachyon). No SU(8), no racetrack — the frontier's need B disappears, and the cliff's
e^{−πx/4} has the form of a worldsheet-instanton correction, available in the heterotic and IIA settings where matter is neutral.
n becomes the resummed instanton sum at small volume (a precise route to deriving it; not done). Matter must be recomputed
(D160, locked, running). Observables otherwise unchanged — including the failed n_s.

## 3c. TWIST-L — raising n_s while keeping rung 3 (D162–D163; locked PREREG_TWISTL, future data only)
A logarithmic factor in the helper field's metric, L = 1 + b/(1 + ln(1 + 2/u)), makes the plateau approach flat as 1/φ while T's
geometry stays on rung 3. b = 1–10 gives n_s 0.969–0.979 with r 0.0048–0.014 (S heavy, angle +4H², tail unchanged to ~10⁻⁵).
The inverse log is the shape of an IR-free running coupling at a T-set scale; b = 8π²C/|b_β| needs only C ≈ 0.03–1.3. Built after
seeing the n_s data, so only future CMB results can score it; TWIST-P is the alternative (higher r at the same n_s).

## 4. Assumptions (each a place it could fail)

1. SM neutral under the disk's isometries (shield) — candidate heterotic Z₃ home.
2. χ → −χ broken at the Planck scale (so χ decays).
3. χ's mass saturates via a single instanton, or SU(2) with an SM cutoff below ~10¹⁶ GeV.
4. The Z₂ racetrack of two hidden groups with a large operator coefficient (where n hides).
5. T's string home: heterotic Z₃ (not type IIB volume).
6. γ self-dual (±i) for black-hole entropy — a choice; the LQG link is motivation only.
7. χ̃ decays to SM fermions (dark matter).

## 5. What the data say now

- **Dark energy:** PURE-TWIST fits DESI DR2 + supernovae + CMB slightly better than ΛCDM (Δχ² −3.4; 0.7–1.7σ after look-elsewhere).
- **n_s — locked verdict: INCONSISTENT (D157).** Fixing n_s at the Twist's 0.964 costs Δχ² = 11.7 against CMB-SPA + DESI (threshold 9);
  ΛCDM at the same n_s costs 8.5. With n_s free, PURE-TWIST fits this full data set slightly worse than ΛCDM (+1.45). The
  Twist's inflation, as it stands, is disfavoured by current data; TWIST-P waits for future data. Per likelihood (D158) the Twist
  still wins the late-universe data (BAO + SN −3.2) and loses the precise CMB (+4.7).
- **Results against the model, kept on record:**
  - the original cliff failed TAIL-F (Δχ² +29), and the reshape that followed was after the fact
  - the γ = 1/4 idea failed
  - the n ≈ 124 leads failed
  - the matter prediction missed (7.5× against 2–3×)
  - an independent referee review led to corrections throughout

## 6. Locked predictions (scored only on future data)

| Lock | Prediction | Decided by |
|---|---|---|
| WATCH-PURE-DR3 | w0 −0.90, wa −0.14 | DESI DR3 (weaker test: it contains DR2) |
| PREREG_GW_FRICTION | no extra gravitational-wave friction, no birefringence | GW standard sirens |
| PREREG_SHIELD | no varying constants / EP violation; any leak has the fixed redshift shape | nuclear clocks, ELT quasars, MICROSCOPE-2 |
| PREREG_TWISTP (+_L) | separate model: n_s 0.965–0.971 with r 0.0036–0.011 rising together | Simons Observatory, LiteBIRD, CMB-S4 |
| r | ≈ 0.0036 (rung 3; other rungs 0.0012 × 3α) | LiteBIRD, CMB-S4 |

## 7. Open, in order of importance

1. n_s: the locked test says INCONSISTENT (D157). The inflation sector needs TWIST-P (future data) or a new idea.
2. n ≈ 125 is chosen (plays Λ's role); no route found (D109, D119, D153).
3. A string setting with rung 3 + linear-T hidden gauge function + neutral matter together (D154) — none known.
4. The cliff in heterotic language: the exponent fits (q), the depth does not.
5. Matter chain: m_σ confirmation, the new-form check, and the yield sensitivity (isocurvature) — all running.
6. Field distance (16 M_P) vs the distance conjecture — depends on the string home.

## 8. Running now

- m_σ confirmation (D124), then the new-form matter check (D129), then the yield-sensitivity test (D137).
- PURE parameter chain (3,000+ steps).
- Evidence fits (first of four models).
