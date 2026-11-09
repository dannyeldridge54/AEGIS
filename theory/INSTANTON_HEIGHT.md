# Can Nieh–Yan instantons set the angle's height (and so its mass)? (V5, 9 Nov 2026)

Paper work, not a test. Order-of-magnitude bookkeeping; numbers from `instanton_height.py` → `instanton_height.json`.
Follows `QUANTUM_SIDE_NOTES_2026-11-08.md` §1–2. No locked rule, prediction or fit changes.

## 1. What Kaul & Sengupta show (arXiv:1411.4793, read 9 Nov)
- First-order gravity + a 2-form axion B (H = dB) coupled to torsion, plus β H² with β dimensionless. The torsion is
  fixed by H (contortion K ∝ κH), and the axion charge of a Giddings–Strominger half-wormhole equals its Nieh–Yan index:
  **Q = N_NY ∈ ℤ**.
- Finite action **S = (π/(3√2)) F_a Q**, F_a² = β − 1/8. Dilute gas of these instantons → η-vacua
  |η⟩ = Σ e^(iηN)|N⟩, energy **−2K e^(−S) cos η**, η identified with (the inverse of) the Barbero–Immirzi parameter
  (the paper says "inverse" in the text and "the BI parameter" in the abstract; the identification is taken from
  Date–Kaul–Sengupta 2009 and Mercuri–Randono, arXiv:1005.1291, not derived there).
- **Not in the paper:** any value of β, S or K (K, the fluctuation factor, is "calculable" but not computed); any
  multi-instanton or ℤ_n discussion; explicit units (κ is not tied to G). Our check of their eq. 21 gives S ∝ κF_aQ with
  a different prefactor; the PDF extraction was garbled at that step, so we use their stated result and say so.

So the paper gives the **shape** (a cosine in the BI angle, our plain Nieh–Yan cosine) but **not the height**.

## 2. Our variables
- Late role: V = Λ⁴(1 − cos(d/F)), F = (4/π)√(3/2) M_P = 1.559 M_P (reduced M_P = 2.435×10²⁷ eV), λ = −2√(2/3).
  Mass m² = Λ⁴/F². Identify Λ⁴ = 2K e^(−S).
- To fix units we match K&S to the standard Giddings–Strominger result (Hebecker, Mangat, Theisen, Witkowski 2016,
  arXiv:1607.06814, eq. 4.20, M_P = 1): **S = (π√6/4) n M_P/f ≈ 1.92 n M_P/f**. Matching the two forms gives
  F_a = (3√3/2) M_P/f. That identification of their F_a with our 1/F is our assumption, stated.

## 3. What S the S8-L mass needs
S8-L best-fit masses (approximate, `spiral_l_score.json`): 1.41 / 1.26 / 1.45 × 10⁻²⁵ eV (P+ / Dovekie / Union3)
→ Λ⁴ = 2.9 / 2.3 / 3.0 × 10⁵ eV⁴.

| Prefactor K | S needed |
|---|---|
| M_P⁴ | **240.4 / 240.6 / 240.3** |
| 10⁻⁴ M_P⁴ | 231.2 |
| 10⁻⁸ M_P⁴ | 221.9 |

So S ≈ 220–240 whatever reasonable K is; the window is narrow in S because the height is exponential.

## 4. Is that value natural? No, not with our F
- **At F = 1.559 M_P, one instanton has S ≈ 1.2** (1.92/1.559). e^(−S) ≈ 0.3: no suppression at all, and S ~ 1 is
  outside the regime where a dilute instanton gas can be trusted. The angle would get a Planck-scale height, i.e. a mass
  near M_P, not 10⁻²⁵ eV. This is the familiar statement that super-Planckian decay constants are not protected from
  gravitational instantons (Weak-Gravity-Conjecture territory).
- What S ≈ 240 would need instead (each one alone):
  - **f ≈ 0.008 M_P ≈ 2×10¹⁶ GeV** for n = 1 (a GUT-scale width, 190× narrower than our derived F); or
  - **n ≈ 195** at our F (only charge-195 instantons contribute: no reason for that); or
  - in K&S's own variables, **F_a ≈ 325, β ≈ 1.05 × 10⁵** at Q = 1, against F_a ≈ 1.67, β ≈ 2.9 implied by our F.
    A dimensionless coupling of 10⁵ is not natural.
- **Verdict (paper level): the S8-L mass is not derived.** With our F, Nieh–Yan wormhole instantons give a height that
  is far too large; the observed tiny mass needs either a much smaller width (which breaks the F = 1.559 M_P result
  the late fits use) or a large, unexplained coupling. Unless K is extraordinarily small (it would need
  e^(−239) ~ 10⁻¹⁰⁴ by itself, i.e. the whole hierarchy moved into K), this route does not explain the mass.
- Caveats: the GS match (§2) is an assumption; wormhole instantons in Einstein–Cartan with a dynamical dilaton
  (our χ) change S by the dilaton coupling (Hebecker et al. eq. 4.19: S = (2/α)(n/f) sin(απ√(3/2)/4); if their α maps
  to our |λ| = 2√(2/3), the factor is 0.64, i.e. S *drops* to ≈ 0.8), which makes the gap to 240 larger, not smaller.

## 5. Could the same height set the early switch-on? No
- The Locked Twist's early field (n = 3, stored `edelockP`: f_EDE 0.078 at z_c ≈ 3554, θ_i 2.77) has
  Λ⁴_early ≈ 0.013 eV⁴ → S_early ≈ 257 (K = M_P⁴). Late: S ≈ 240. They differ by ΔS ≈ 17 (heights differ by ~10⁷).
- The widths differ too (early F ≈ 0.14 M_P vs late 1.559 M_P; `COUPLING_CHOICE_NIEH_YAN.md`), and S ∝ 1/F would make
  the early instantons *less* suppressed (S_early ≈ 11× S_late at fixed n), the opposite of what is needed.
- So one instanton height cannot set both roles. This adds to the misalignment conflict already noted (θ_i ≈ 0.03 late
  vs 2.4–2.8 early): the early boost and the late angle look like different fields.

## 6. Could a three-fold symmetry give n = 3? Not by cancelling terms
- (1 − cos x)³ = 5/2 − (15/4) cos x + (3/2) cos 2x − (1/4) cos 3x. It is **not** ℤ₃-invariant (it is not periodic under
  x → x + 2π/3). A ℤ₃ that forbids the 1- and 2-instanton terms leaves only cos 3x: that is **1 − cos 3x, an n = 1
  cosine with a third of the period**, not the flat-bottomed n = 3 shape.
- The n = 3 shape needs the 1-, 2- and 3-instanton amplitudes in the fixed ratio 15/4 : 3/2 : 1/4 (with alternating
  signs from the η phase). A dilute gas gives e^(−S) : e^(−2S) : e^(−3S); the ratio 3/2 ÷ 15/4 = 0.4 would need
  S ≈ 0.9 and then the third ratio fails (e^(−2S) ≈ 0.16 vs 1/15 ≈ 0.07), and S ≈ 0.9 is not a dilute gas anyway.
- **So instantons do not give n = 3**, with or without ℤ₃. The options left from the 8 Nov notes: the early boost is
  another field, or the n = 3 shape is effective (dilaton and angle moving together). The deferred n = 1 test
  (DRAFT_POWER_N1_AXICLASS.md) would say how much n = 3 is really required.

## Bottom line
- Nieh–Yan instantons explain **why the potential is a cosine in the BI angle** (supports the Nieh–Yan choice).
- They do **not** explain the **height**: with F = 1.559 M_P the predicted height is ~10¹⁰⁰ times too large; S ≈ 240
  needs β ~ 10⁵ or a GUT-scale width.
- They do **not** link the early and late roles, and they do **not** produce n = 3.
- Nothing here is a fitted number; no rule is proposed. The mass stays a free parameter of S8-L.

## Sources
Kaul & Sengupta, arXiv:1411.4793; Hebecker, Mangat, Theisen, Witkowski, arXiv:1607.06814; Mercuri & Randono,
arXiv:1005.1291.
