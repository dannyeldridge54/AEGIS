# The Twist: a no-scale supergravity field for inflation and a thawing dark-energy tail, with pre-registered tests

Danny Lee Eldridge (independent researcher) · 13 November 2026 · version 5 (consolidated after an independent referee review)

## Abstract

We study one complex field in no-scale supergravity, T = x + iy with Kähler potential K = −3 ln(T + T̄). Its field space has curvature −2/3 (the α = 1 attractor). Earlier work showed that this is the field space of the "Spiral Twist": a dilaton φ and a Barbero–Immirzi angle θ. We take the angle's coupling to the fermion axial current from the Nieh–Yan term, c_A = √(3/8). This value holds for the canonically normalised angle, a normalisation we choose and state.

One explicit construction, TWIST-K, gives a potential that goes plateau → cliff → tail. In it, the cliff sits in the Kähler metric of a stabiliser field.

The plateau predicts n_s = 0.9642–0.9654 and r = 0.0035–0.0038 with no fitted parameter. This prediction failed its own pre-registered test against current data: on Planck + ACT DR6 + SPT-3G + DESI DR2 + Pantheon+, fixing n_s at the Twist value costs Δχ² = 11.7, against a locked threshold of 9.

The tail is thawing quintessence with slope √(2/3) and no coupling to dark matter. On a compressed late-time likelihood it was preferred to ΛCDM by Δχ² = −3.4. This is 1.8σ locally and 0.6–1.0σ after correcting for the number of late-time variants tried. The tail shape and the choice μ = 1 were fixed after related data had been seen. On the full CMB + DESI + supernova data, the same tail fits worse than ΛCDM (Δχ² = +1.45). We therefore claim no evidence for the tail on current data.

Every late-time result assumes that ordinary matter does not feel the field (a "shield"). We could not realise that shield in any string setting we examined, so it is an effective-theory assumption.

What the paper offers:
- a single-field supergravity embedding with a derived axial coupling;
- a set of predictions locked before the data that will judge them: r, the tail's w(z), no cosmic birefringence from this field, and the redshift shape of any shield leak;
- the negative results, reported in full.

Matter genesis, dark matter, the string-theory search and post-data variants are in a separate exploratory note.

## 1. Introduction and scope

Inflation, the matter–antimatter asymmetry and today's accelerated expansion usually get three separate explanations. We ask how far one supergravity field can go toward all three, and we score every data comparison against a rule written and hashed before the comparison ran.

What is claimed:
1. The Twist's two-field geometry is the field space of no-scale supergravity at α = 1. With T = x + iy and x = e^{√(2/3)φ}, K = −3 ln(T + T̄) reproduces the metric exactly.
2. One explicit construction (TWIST-K, Section 2) gives a plateau, a cliff and a √(2/3) tail. It does so with the stabiliser field heavy and the angle non-tachyonic throughout, checked in full two-field supergravity.
3. Its inflation and late-time predictions are definite and falsifiable (Section 6).

What is not claimed:
- No evidence against ΛCDM (Section 4.3).
- No derivation of the cliff depth n, which plays the role of the cosmological constant.
- No ultraviolet (string) completion.
- No solution of the fifth-force problem beyond an assumed symmetry.
- The inflation prediction for n_s is currently disfavoured (Section 3.2).

How the work was done. Each data test has a written rule fixed by a SHA-256 hash before its numbers were computed. Rules are never edited. Deviations go in a separate file written before any rerun, and each test is reported once. Theory calculations are labelled computed, estimate or assumption. The author is an independent researcher. The calculations, code and drafting were done with substantial help from an AI system (Claude, Anthropic), under the author's direction and the rules above. Code, rule files and hashes are archived with this record (Section 8).

## 2. The model

### 2.1 Field space

The Twist has a dilaton φ and an angle θ with kinetic metric

(1) ds² = dφ² + e^{λφ} dθ², λ = −2√(2/3),

in reduced Planck units (M_P = 2.435×10¹⁸ GeV). Its Gaussian curvature is −λ²/4 = −2/3.

Writing T = x + iy with x = e^{√(2/3)φ} and θ = √(3/2) y, the Kähler metric K_TT̄ = 3/(T + T̄)² gives exactly (1). The inflaton is Re T and the angle is Im T. This identification is the starting point of this work, not a result of it. It rests on the Barbero–Immirzi chiral superfield of Gates, Ketov & Yunes [1], with K_ΦΦ̄ = 3/(Φ + Φ̄)².

### 2.2 Coupling to matter (explicit form)

With fermions present, the Nieh–Yan term couples the angle to the axial current [2, 3]. Written in the variables of the model, the coupling used throughout is

(2) ℒ ⊃ (c_A / M_P) e^{λφ/2} ∂_μθ J₅^μ = (c_A / M_P) √(3/2) (∂_μ y / x) J₅^μ, c_A = √(3/8).

A rolling angle then acts as an axial chemical potential μ₅ = c_A v_θ H, where v_θ ≡ √(3/2) ẏ/(x H M_P) is the angle's canonical speed in units of H M_P.

Two choices are made here, and both are stated:
- **The Nieh–Yan current couples to the canonically normalised angle.** The alternative reading, which couples to ∂(y/x) through the mapping 1/γ_BI = y/x, adds a term −(y/x)ẋ/x that is not small after inflation. That alternative was not computed.
- **Hence c_A = √(3/8) is fixed only given this normalisation.**

Only the exploratory matter mechanism uses (2). The inflation and late-time results do not depend on it.

### 2.3 The potential: TWIST-K

A stabiliser field S keeps the dynamics on S = 0:

(3) K = −3 ln( T + T̄ − g E(u) S S̄ + ζ E(u)² (S S̄)² ),  W = √3 m S T,

with u = T + T̄, g = 1 + u/(2μ) and E(u) = exp(2n(1 − e^{−πu/8})). Along S = 0 and real T this gives

(4) V(x) = m² x² / [4x² (1 + x/μ)] · exp(−2n(1 − e^{−πx/4})).

The pieces of (4) do the following:
- **The plateau** is at small x, mirrored relative to the usual placement (T → 1/T). There V is an α = 1 E-model.
- **The cliff factor** ends inflation and lowers the energy by e^{−2n}.
- **The tail** at x ≫ μ goes as V ∝ e^{−2n} e^{−√(2/3)φ}. The cliff's leftover slope dies like e^{−πx/4}.

The full two-field supergravity calculation reproduces (4) to ten digits. Along the whole history:
- S stays heavy: m_S²/H² ≈ 30 at the CMB point, up to ~7×10⁴ through the cliff, and 2.6×10³ today.
- The angle's mass squared stays positive (+4H² to +8H²).

The cliff's form e^{−πx/4} is assumed. It has the form of a worldsheet-instanton correction to a Kähler metric, but no string computation produces it or its depth (Section 7).

### 2.4 Parameters (single source for every number in this paper)

| Symbol | Meaning | Value | Status |
|---|---|---|---|
| m | inflaton mass scale | 2.1×10⁻⁵ M_P | fixed by the scalar amplitude A_s = 2.1×10⁻⁹ |
| n | cliff depth | 124.6 (≈ 125) | chosen to give today's dark-energy density (Δn ≈ 0.35 per factor 2 in ρ_DE). Without the 1/(1 + x/μ) factor the same condition gives 126.9 |
| μ | Kähler constant setting where the tail starts | 1 | chosen after seeing late-time data (Section 4.3) |
| ζ | quartic stabiliser term | 3×10⁵ | chosen; keeps S stable for x > 1/(4ζ) = 8×10⁻⁷ |
| π/4 | cliff exponent | — | assumed form |
| f_heat | share of the inflaton energy turned into radiation | 0.65–0.8% | derived from the reheating field's decay (exploratory note) |
| T_RH | reheating temperature | 5.5–5.8×10¹⁴ GeV | from H_end = 5.2×10¹² GeV and f_heat. Instant reheating (f = 1) would give 1.9×10¹⁵ GeV |
| N* | e-folds before the end of inflation at k* = 0.05 Mpc⁻¹ | 55.7 (instant) to 57.6 (derived f_heat, including kination) | computed |
| x_f, x₀ | where the tail field freezes after kination, and its value today | 73, 89 | computed at f_heat = 0.8% |
| Δφ | field distance from the CMB point to today | ≈ 16 M_P | computed |

In the numerical studies of the cliff a depth n = 10 was used for speed. All numbers quoted here are for n = 124.6 unless stated.

## 3. Inflation

### 3.1 Predictions

The α = 1 plateau gives n_s ≈ 1 − 2/N* and r ≈ 12/N*², evaluated exactly along the trajectory:

| Reheating | N* | n_s | r |
|---|---|---|---|
| instant (f = 1) | 55.7 | 0.9642 | 0.0038 |
| derived (f_heat = 0.8%, with the kination phase after the cliff) | 57.6 | 0.9654 | 0.0035 |

Other observables at N* = 57.6:
- running dn_s/dln k = −6.0×10⁻⁴;
- tensor tilt n_t = −r/8 = −4.4×10⁻⁴;
- squeezed f_NL ≈ 0.014.

The scalar amplitude fixes the scales: V*^{1/4} ≈ 7.9×10¹⁵ GeV and H* ≈ 1.5×10¹³ GeV.

The loop correction from the reheating field is negligible once that field's mass saturates (exploratory note). Earlier estimates of a +0.002 shift are withdrawn. During inflation the angle is heavy along its valley (m/H ≈ 2 or more), so it carries no isocurvature at leading order.

The pre-registered inflation rule (TWIST-INFLATION) froze the leading-order band r = 0.0037–0.0040. It reads SUPPORTED if a future measurement with σ(r) ≤ 0.002 finds r consistent with that band within 2σ, and RULED OUT if r < 0.002 or r > 0.008 at 95%. The rule is scored as written. Note that the derived-reheating value, 0.0035, lies just below the frozen band.

### 3.2 The pre-registered n_s test failed

PREREG_NS_SPA (scored 13 Nov 2026) used ACT DR6 + SPT-3G + Planck low-ℓ + ACT lensing + DESI DR2 BAO + Pantheon+ + DES Y6 S₈, with the Twist's own late universe. Fixing n_s = 0.964 costs Δχ² = 11.7 relative to n_s free (best fit 0.9756). The locked threshold for INCONSISTENT is 9. The reading is **INCONSISTENT**: the inflation sector, as it stands, is disfavoured by current data at the pre-registered level. ΛCDM at the same fixed n_s costs 8.5.

Context, which does not soften the reading: the high n_s comes mostly from combining the CMB with DESI BAO [4, 5].
- The Twist is −0.3σ from ACT alone.
- It is −1.7σ from CMB-SPA alone (0.9693 ± 0.0029).
- It is −3.7σ from CMB-SPA + DESI (0.9737 ± 0.0025).
- Against Planck 2018 (0.9649 ± 0.0042) it is within 0.5σ.
- Against Planck + ACT + DESI (0.9743 ± 0.0034) it is 2.7–3.3σ low.

The Twist's evolving dark energy does not remove the shift.

n_s cannot be raised inside the model. Every exponential plateau gives n_s ≈ 1 − 2/N*, and reaching n_s ≈ 0.973 would need N* ≈ 74. The other routes are too small:
- a stiff post-inflation era adds at most +0.0007;
- second-order slow roll adds ~10⁻⁵;
- softening the cliff lowers n_s.

Variants that change the superpotential or Kähler potential to reach higher n_s were built after seeing these data. They are recorded in the exploratory note and can be scored only on future data.

## 4. The late universe

### 4.1 The tail and its slope

After the cliff, the field runs through a kination phase and freezes. It then thaws today on V ∝ e^{−2n} / (1 + x/μ). The local slope is √(2/3) · x/(x + μ):

| μ | x | Share of √(2/3) |
|---|---|---|
| 1 | 73–89 (computed at f_heat = 0.65–0.8%) | 98.6–98.9% |
| 1 | 2 | 67% |
| 10⁴ (earlier choice) | — | 0.02–3%; the tail is almost a cosmological constant |

A share of 97% or more needs x ≳ 30. The value μ = 1 was adopted after the late-time data had been seen (Section 4.3).

The tail slope √(2/3) equals 2/√(6α) at α = 1 [6]. It also equals the asymptotic Trans-Planckian Censorship bound 2/√((d−1)(d−2)) in four dimensions [7].

At its best fit the tail gives:
- w = −0.899 today, rising from −0.996 at z = 3;
- a CPL fit over z < 2 to the field's own w of w₀ = −0.900, w_a = −0.143;
- an observer who assumes ordinary dark matter and fits uniformly in a over z ≤ 2 (the convention of the locked WA-CEILING rule) gets w_a ≈ −0.10.

These are the same model under two fitting conventions. The dark-energy curve hardly depends on the heat share: w₀ ≈ −0.90 and w_a ≈ −0.14 from f_heat = 0.01% to 0.8%.

### 4.2 Data and tests

The late universe is described by a scalar with V ∝ e^{−κφ}, optionally coupled to dark matter with strength β_DM. The supergravity model predicts κ = √(2/3) and β_DM = 0. The coupling β_DM is zero because masses in this supergravity class do not depend on the inflaton [8].

The compressed likelihood combines:
- Pantheon+ supernovae, with the absolute magnitude marginalised;
- CMB distance priors;
- BAO from DESI DR2, or from SDSS DR12/DR16.

Each version is fitted three ways:
1. with DESI;
2. with no BAO, after which it predicts DESI and SDSS;
3. with SDSS in place of DESI.

All entries in the table are differences from ΛCDM; negative is better.

| Version | Extra parameters | ΔAIC, fit with DESI | Predicting DESI | Predicting SDSS | Fit to SDSS | Locked reading |
|---|---|---|---|---|---|---|
| PURE-TWIST (κ = √(2/3), β_DM = 0) | 0 | −3.37 | −0.89 | −0.41 | −2.67 | PREFERRED |
| KAPPA-ALPHA1 (κ = √(2/3), β_DM fitted) | 1 | −4.30 | −6.72 | +0.90 | −3.04 | not predictive |
| FLAG-1 (κ = 1, β_DM fitted) | 1 | −3.32 | +10.88 | +10.38 | −1.20 | not predictive |
| SPIRAL (κ, β_DM fitted) | 2 | −2.33 | −6.27 | +0.39 | −3.27 | not predictive |
| ON2 (coupling switches on late) | 1 | +0.53 | −1.90 | −0.37 | −0.78 | predicts, not preferred |
| SPIRAL0 (κ = 1, β_DM = 0) | 0 | +1.11 | +0.62 | −0.36 | +1.02 | not predictive |
| w₀w_a (for comparison) | 2 | −2.21 | −3.87 | −0.17 | −3.27 | — |

The DESI-HOLDOUT Test A has its own definition: FLAG-1 is refitted on non-DESI data with its own nuisance settings. Under that definition FLAG-1 predicts DESI worse than ΛCDM by Δχ² = +12.5. The +10.88 in the table comes from the tournament's NOBAO leg.

### 4.3 How much the late-time result is worth

The PREFERRED reading of PURE-TWIST rests on four choices made after data were seen:
1. **The original cliff failed its locked test.** TAIL-F gave Δχ² = +29.2 against ΛCDM. The cliff was then reshaped to the form in (4). That was a choice, not a derivation.
2. **μ = 1 was chosen knowing that it gives the steep tail the data favour.**
3. **The PURE-TWIST rule was written when SPIRAL0 and KAPPA-ALPHA1 were already known.**
4. **The same data were used for six tournament variants, TAIL-F, NS-PURE and two data-swap tests.**

The size of the preference:
- Δχ² = −3.37 with no extra parameter is a likelihood ratio of about 5, or 1.84σ locally (two-sided p = 0.066).
- With 6–12 variants tried, the Šidák-corrected significance is 0.6–1.0σ.
- The held-out improvements (−0.89 and −0.41) are at noise level.
- The likelihood is compressed.
- On the full CMB-SPA + DESI DR2 + Pantheon+ data (the n_s-free leg of NS-SPA), PURE-TWIST fits worse than ΛCDM by Δχ² = +1.45.

The tail is generic thawing quintessence with slope √(2/3). Its supergravity origin plays no role in these fits. The honest reading is that current data give **no evidence** for it. Its scientific value is the prediction locked for new data (Section 6).

DESI DR3 is cumulative with DR2, so it is a weaker out-of-sample test than an independent survey such as Euclid.

### 4.4 Observables at a stated conditioning

At each model's own best fit, with neither refitted, PURE-TWIST relative to ΛCDM:

| z | D_M/r_d | D_H/r_d |
|---|---|---|
| 0.30 | +0.86% | −0.06% |
| 0.51 | +0.40% | −0.55% |
| 0.71 | +0.16% | −0.66% |
| 0.93 | 0.00% | −0.63% |
| 1.32 | −0.12% | −0.45% |
| 2.33 | −0.16% | −0.10% |

At the same best fits, growth relative to ΛCDM:
- σ₈ is 0.781 against 0.801;
- S₈ is 0.793 against 0.798;
- fσ₈ is 3.3% lower at z = 0.5;
- E_G is 4.9% higher at z = 0.5 (0.418 against 0.399).

About four points of that E_G shift come from the different best-fit Ω_m (0.310 against 0.298). At equal Ω_m the β_DM = 0 tail gives E_G within about 1% of ΛCDM, and the growth index stays GR-like (0.557 → 0.548).

The locked growth rule (PREREG_GROWTH) is stated at fixed Ω_m = 0.31 and fixed early amplitude: σ₈ is 1.5% lower and fσ₈ is 3.2% lower at z = 0.3–0.5. At fixed Ω_m and H₀, H(z) is up to 1.9% higher near z = 0.5. That last figure is a theoretical sensitivity, not a forecast of what a survey will see.

Costs relative to ΛCDM:
- The CMB-inferred H₀ falls to ≈ 65.7 km s⁻¹ Mpc⁻¹, a slightly worse Hubble tension.
- The late integrated Sachs–Wolfe signal is 5% stronger (A_ISW ≈ 1.05; measured 0.98 ± 0.35).

## 5. Consistency checks and negative results

The construction of Section 2 survived a sequence of failures:

| Version | Result | What it forced |
|---|---|---|
| Plateau joined smoothly to a √(2/3) tail | ε → 1/3: inflation never ends | a cliff |
| Tail placed before the cliff | the tail inflates on its own (+7 e-folds) | tail after the cliff |
| Plateau at large T (inflaton falling to small T) | the curved space drains the angle's speed by ~e⁻² per e-fold | the mirrored placement |
| A vacuum, F = T − ½ | at the vacuum the angle has the inflaton's mass and oscillates 3–30,000 times per expansion time | no vacuum: the potential runs into a tail (true for any holomorphic F with a simple zero) |
| Original cliff exp(−nT/(T + 1)) | leftover slope dies like 1/x; TAIL-F Δχ² = +29.2 | the e^{−πx/4} cliff (post hoc) |
| A constant superpotential | no angle potential | the stabiliser construction |

### 5.1 The fifth force (the main open problem)

If Re T is today's dark energy, ordinary matter generically feels it:
- Through the Kaplunovsky–Louis anomaly terms [9], the QCD scale moves with x for every matter modular weight except 3/4.
- Sequestered matter gives a coupling β_m ≈ 0.41, about 120 times the Cassini bound (β_m < 3.4×10⁻³).
- Weight-3/4 matter leaves quark masses moving (β_m ~ 0.015).
- No standard screening mechanism applies to an exponential tail.
- The argument that lets the reheating field decay through Planck-suppressed operators also generically gives order-one couplings.

We therefore **assume a shield**: the Standard Model is neutral under both isometries of the T-disk, the scaling T → λT and the shift T → T + ic. The cliff breaks the shift only through q = e^{−πT/4}. Along the thawing solution that instanton part passes the quasar, Oklo, nucleosynthesis, atomic-clock and MICROSCOPE limits by 10¹⁹ or more. Approximate symmetries suppressing quintessence couplings is Carroll's idea [10]. Higgs-dilaton cosmology is a precedent for a spontaneously broken scale symmetry with derivative-only matter couplings [11].

A perturbative leak c_p/x^p must satisfy p ≥ 4 for an order-one coefficient, and clocks require |d ln α_em/dφ| < 1.6×10⁻⁸ today. Any leak has a fixed redshift shape, locked in PREREG_SHIELD:
- about 78% of the change comes after z = 1;
- there is nothing new above z ≈ 3;
- clock drifts are tied to quasar shifts.

Quantum stability of the tail also requires every particle heavier than ~6 meV to have a T-independent mass (the Kolda–Lyth problem [12]). This is assumed.

### 5.2 Gravitino

W = √3 m S T vanishes at S = 0, so the inflaton sector does not set the gravitino mass. Supersymmetry breaking comes from a separate sector that we do not specify. We assume it gives m_3/2 below the inflaton mass, so the plateau is undisturbed.

Two consequences:
- **A stable gravitino is excluded at the Twist's T_RH ≈ 5.6×10¹⁴ GeV.** In the high-scale-supersymmetry scenario of Dudas et al. [13] (all superpartners above the inflaton mass), Ω_{3/2}h² ≈ 0.11 (0.1 EeV/m_3/2)³ (T_RH/2×10¹⁰ GeV)⁷. So the gravitino is not the dark matter (see also [14]). Version 4's statement that a gravitino heavier than T_RH escapes production misread that scenario and is withdrawn.
- **What does work (estimate).** Take superpartners at or below m_3/2, in the bath. The thermal yield is then Y ≈ 1.5×10⁻⁷. For m_3/2 = 10¹¹–10¹⁴ GeV the gravitino decays at T ≈ 4×10⁶–10¹¹ GeV, long before nucleosynthesis, carrying at most 0.4% of the energy. This needs R-parity violation so that the lightest superpartner also decays.

Both assumptions (the separate supersymmetry-breaking sector and R-parity violation) are listed in Section 7.

### 5.3 Field range and initial conditions

The field travels Δφ ≈ 16 M_P from the CMB point to today. Treating T as a volume-type modulus, the tower stays at least 20× above H and at least 76× above T throughout. The far plateau (x ≲ 6×10⁻⁶) lies outside the effective theory.

With ζ = 3×10⁵ the stabiliser is stable down to x = 8×10⁻⁷, so the binding limit is the tower floor. About 2.5–3.8 M_P of plateau beyond the CMB point lies inside the effective theory.
- Homogeneous starts from rest give at least 300 e-folds.
- Fast-moving starts begin where S is unstable and are excluded.
- Inhomogeneous starts fall in the robust plateau class of published numerical-relativity studies. That conclusion is by analogy, not computed.

### 5.4 Cosmic birefringence

The field that rolls today is CP-even. Its CP-odd partner, the angle, is heavy and sits at its minimum. The angle also couples only derivatively to fermion spin, which decouples for heavy fermions [15]. The Twist therefore predicts no isotropic birefringence.

The joint ACT + Planck analysis reports β_CMB = 0.277° ± 0.057° (4.9σ) [16], and an internal test of the Planck detector angles found no calibration inconsistency [17]. This predates our lock and its absolute calibration is open, so it is not scored. A calibrated confirmation would falsify the single-field Twist (Section 6).

## 6. Locked predictions

Every rule below was hashed before the data that will judge it existed. Rules are scored as written.

| Rule | Prediction | Deciding data | Fails if |
|---|---|---|---|
| TWIST-INFLATION | r band 0.0037–0.0040; computed 0.0035–0.0038 | first r measurement with σ(r) ≤ 0.002 (Simons Observatory, LiteBIRD, CMB-S4 class) | r < 0.002 or r > 0.008 at 95% |
| NS-SPA | n_s = 0.964 | — | already scored: INCONSISTENT |
| WATCH-PURE-DR3 | the √(2/3), β_DM = 0 tail at its frozen best fit; BAO offsets as in Section 4.4 | DESI DR3 BAO | Δχ² ≥ +2 against frozen ΛCDM, i.e. DISFAVOURED (SUPPORTED if Δχ² ≤ −2) |
| WA-CEILING | every thawing Twist version has an effective w_a ≥ −0.40 (PURE-TWIST −0.10 in the rule's convention) | DESI DR3 headline w₀w_a | w_a + 3σ < −0.40 |
| PREREG_GROWTH | GR-like growth index; fσ₈ deficit peaking at z ≈ 0.3–0.5 | DESI DR3 full shape, Euclid DR1, Rubin Y1 | growth index off 0.55 by > 0.05 at > 3σ, or an fσ₈ excess at z = 0.3–0.7 at > 3σ |
| BIREF-NULL | isotropic birefringence from this field = 0 | a calibration-independent measurement with error ≤ 0.10° | β_CMB ≥ 5σ |
| LAB-NULLS / GW-FRICTION | no fifth force, no α_em drift, c_gw = c, Ξ₀ = 1 | laboratory and gravitational-wave tests | a confirmed detection |
| SHIELD | any α_em or mass drift follows the locked redshift shape | clocks (thorium-229), quasars, MICROSCOPE successors | a drift with a different shape |

Order of the decisive tests:
- a calibrated birefringence measurement (any year);
- DESI's five-year results and Euclid's first cosmology (2027);
- the Simons Observatory, which can detect r ≈ 0.0036 at 3–5σ (2028–2035);
- thorium nuclear clocks, sensitive to |d ln α_em/dφ| ~ 5×10⁻¹²;
- LiteBIRD (2030s).

## 7. Assumptions and limitations

Assumptions (each is a place the model could fail):
1. **The shield.** The Standard Model is neutral under the T-disk isometries. No string setting we examined realises it (exploratory note).
2. The cliff's form e^{−πx/4} and its depth n ≈ 125 are chosen. Instanton sums we computed give about 10⁻⁴ of the required depth.
3. Masses heavier than ~6 meV are T-independent (tail quantum stability).
4. Supersymmetry is broken in an unspecified sector with m_3/2 below the inflaton mass, and R-parity is violated.
5. The Nieh–Yan current couples to the canonically normalised angle (Section 2.2).
6. The far plateau and fast starts lie outside the effective theory.

Limitations:
- The inflation n_s prediction failed its locked test.
- The late-time preference is not significant after correcting for trials.
- μ and the cliff form were fixed after data were seen.
- The likelihood used for the tournament is compressed.
- The Trans-Planckian Censorship conjecture in its inflationary form would exclude the Twist's inflation scale, and its sharpened late-time form, |V′/V| ≥ √2, would exclude every DESI-fitting exponential tail including this one. We record this as tension, not support.
- The link to loop quantum gravity is motivation only. Today the angle sits at zero, and the self-dual value γ_BI = ±i is a choice [18].

## 8. Methods, data and reproducibility

Code, every rule file with its SHA-256 hash and lock time, the deviation logs and the result files are archived with this Zenodo record (AEGIS repository, branch unify-bg).

Late-time fits use AxiCLASS with a coupled-quintessence extension. It was validated against the unmodified build: background to 10⁻⁷, and P(k) and σ₈ to 2×10⁻⁶. Fits use two Nelder–Mead starts, with a reproduction gate of 0.05 in χ² for stored fits.

Inflation uses two-field background equations on the curved field space, in e-fold time with Christoffel terms, solved by LSODA (rtol 10⁻⁸–10⁻¹⁰). N* follows the standard matching at k* = 0.05 Mpc⁻¹ with ρ_end = 1.5 V_end and g* = 106.75. The supergravity checks evaluate the full two-field potential and mass matrix from (3).

Rules used: TOURNAMENT, KAPPA-ALPHA1, PURE-TWIST, DESI-HOLDOUT, MISSING-PIECE, TAIL-F, TWIST-INFLATION, NS-PURE, NS-SPA, CONSISTENCY, WATCH-PURE-DR3, WA-CEILING, GROWTH, BIREF-NULL, LAB-NULLS, GW-FRICTION and SHIELD.

## 9. Relation to prior work

Every ingredient has been published before:

| Ingredient | Prior work |
|---|---|
| The Immirzi field as a chiral superfield with K = −3 ln(Φ + Φ̄) | Gates, Ketov & Yunes [1] |
| The Immirzi field coupled to fermions via Nieh–Yan | Mercuri [2]; Calcagni & Mercuri [3] |
| Plateau plus dark-energy tail in no-scale supergravity, tail slope 2/√(6α) | Akrami, Kallosh, Linde & Vardanyan [8]; Dimopoulos & Owen [6] |
| The Barbero–Immirzi scalar in inflation and dark energy | Pollari [19]; Gao et al. [20] |
| The Immirzi field as a source of the baryon asymmetry | Mir, Shabir, Tiwari & Faizal [21] |

Mir et al. [21] (read in full) use a different coupling: they couple a pseudoscalar promoted from the Immirzi parameter to the B−L current, with strength set by a Stückelberg mass. Their asymmetry comes from gravity-assisted equilibrium leptogenesis. They include no inflation, dark energy or supergravity embedding, and they predict birefringence and chiral gravitational waves. The Twist predicts no birefringence from its field, which separates the two.

The contribution here is narrow:
1. a stabiliser construction (TWIST-K) that gives the Gates–Ketov–Yunes superfield a plateau → cliff → tail potential with all masses under control;
2. a derived (normalisation-dependent) axial coupling;
3. a falsifiable, locked set of predictions, with negative results reported.

## References

[1] S. J. Gates Jr., S. V. Ketov, N. Yunes, "Seeking the loop quantum gravity Barbero–Immirzi parameter and field in 4D, N = 1 supergravity", Phys. Rev. D 80, 065003 (2009), arXiv:0906.4978.
[2] S. Mercuri, "Peccei–Quinn mechanism in gravity and the nature of the Barbero–Immirzi parameter", Phys. Rev. Lett. 103, 081302 (2009), arXiv:0902.2764.
[3] G. Calcagni, S. Mercuri, "Barbero–Immirzi field in canonical formalism of pure gravity", Phys. Rev. D 79, 084004 (2009), arXiv:0902.0957.
[4] E. G. M. Ferreira, E. McDonough, L. Balkenhol, R. Kallosh, L. Knox, A. Linde, "The BAO–CMB tension and implications for inflation", arXiv:2507.12459 (Phys. Rev. D, 2026).
[5] E. McDonough, E. G. M. Ferreira, "The spectrum of n_s constraints from DESI and CMB data", arXiv:2512.05108.
[6] K. Dimopoulos, C. Owen, "Quintessential inflation with α-attractors", JCAP 06 (2017) 027, arXiv:1703.00305.
[7] A. Bedroya, C. Vafa, "Trans-Planckian censorship and the swampland", JHEP 09 (2020) 123, arXiv:1909.11063; A. Bedroya, R. Brandenberger, M. Loverde, C. Vafa, "Trans-Planckian censorship and inflationary cosmology", Phys. Rev. D 101, 103502 (2020), arXiv:1909.11106.
[8] Y. Akrami, R. Kallosh, A. Linde, V. Vardanyan, "Dark energy, α-attractors, and large-scale structure surveys", JCAP 06 (2018) 041, arXiv:1712.09693.
[9] V. S. Kaplunovsky, J. Louis, "Model-independent analysis of soft terms in effective supergravity and in string theory", Phys. Lett. B 306 (1993) 269, arXiv:hep-th/9303040; "Field-dependent gauge couplings in locally supersymmetric effective quantum field theories", Nucl. Phys. B 422 (1994) 57, arXiv:hep-th/9402005.
[10] S. M. Carroll, "Quintessence and the rest of the world", Phys. Rev. Lett. 81, 3067 (1998), arXiv:astro-ph/9806099.
[11] J. García-Bellido, J. Rubio, M. Shaposhnikov, D. Zenhäusern, "Higgs-dilaton cosmology: from the early to the late universe", Phys. Rev. D 84, 123504 (2011), arXiv:1107.2163; S. Casas, M. Pauly, J. Rubio, "Higgs-dilaton cosmology: an inflation–dark-energy connection and forecasts for future galaxy surveys", arXiv:1712.04956.
[12] C. Kolda, D. H. Lyth, "Quintessential difficulties", Phys. Lett. B 458 (1999) 197, arXiv:hep-ph/9811375.
[13] E. Dudas, T. Gherghetta, Y. Mambrini, K. A. Olive, "Inflation and high-scale supersymmetry with an EeV gravitino", Phys. Rev. D 96, 115032 (2017), arXiv:1710.07341.
[14] E. Dudas, Y. Mambrini, K. A. Olive, "Case for an EeV gravitino", Phys. Rev. Lett. 119, 051801 (2017), arXiv:1704.03008.
[15] J. Quevillon, C. Smith, "Axions are blind to anomalies", Eur. Phys. J. C 79, 822 (2019), arXiv:1903.12559.
[16] ACT and Planck joint cosmic birefringence analysis, arXiv:2608.06480.
[17] Planck detector polarisation-angle internal consistency test, arXiv:2609.09149.
[18] E. Frodden, M. Geiller, K. Noui, A. Perez, "Black hole entropy from complex Ashtekar variables", Europhys. Lett. 107, 10005 (2014), arXiv:1212.4060.
[19] G. Pollari, "Barbero–Immirzi scalar field for inflation and quintom dark energy", arXiv:2308.03145.
[20] Z.-F. Gao, H. Wang, L. C. Garcia de Andrade et al., "Dynamical Barbero–Immirzi field coupled to quintessence", arXiv:2608.09487.
[21] S. A. Mir, A. Shabir, S. K. Tiwari, M. Faizal, "Geometric baryogenesis with chiral-time equivalence", arXiv:2604.03973.
[22] Planck Collaboration, "Planck 2018 results. X. Constraints on inflation", A&A 641, A10 (2020).
[23] DESI Collaboration, DR2 BAO results (2025); D. Scolnic et al., D. Brout et al., Pantheon+ (2022); S. Alam et al., SDSS DR12 (2017) and DR16 (2021) BAO.
[24] B. Bertotti, L. Iess, P. Tortora, "A test of general relativity using radio links with the Cassini spacecraft", Nature 425, 374 (2003).
