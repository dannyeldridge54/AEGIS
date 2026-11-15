---
title: "The Janus Twist: a status report on single-torus modular inflation, its Kairos and Chronos branches, and what it does not explain"
author: "Danny Eldridge (independent researcher), with AI assistance (Claude, Anthropic)"
date: "Draft v2.1, 14 November 2026 — revised after two rounds of independent referee review; not yet published"
---

# Abstract

This is a status and synthesis preprint, not a claim of a new mechanism. "Janus Twist", "SERAPIS", "Kairos" and "Chronos" are naming metaphors for the framework, the model and its two branches.

We collect a series of pre-registered tests (AEGIS D-notes D436–D539) on one idea: the inflaton is the **shape τ of a hidden two-torus**, with a potential built from modular (SL(2,ℤ)) functions. In the model **SERAPIS** (K = −ln 2 Im τ, nilpotent stabiliser), the stretched torus gives a cusp plateau that drives inflation. The torus then relaxes to the square shape τ = i, which is a heavy (m ≈ 4.2–4.5×10¹³ GeV), supersymmetric **Minkowski** minimum; the hexagonal point is a wall. **The cosmological constant is not explained**: an earlier version of this work placed Λ at τ = i, but that relied on a non-holomorphic branch choice and is withdrawn (D537). With a holomorphic superpotential, a heavy de Sitter vacuum at τ = i is excluded in this minimal set-up (D538; cf. Leedom–Righi–Westphal), so Λ is an added, tuned sector, as in other modular-inflation models.

Inflation splits into two branches. **SERAPIS–Kairos** (no fitted tilt) is in effect an α = 1/3 attractor. At its own reheating N* = 52–55.6 it gives n_s = 0.963–0.965 and r = 0.0012–0.0013. That is consistent with CMB-SPA (−1.1σ to −1.8σ) and 2.8–3.7σ from CMB-SPA+DESI. These values hold for the chosen form of H(j) and κ ≲ 2π. **SERAPIS–Chronos** (one fitted tilt, δ = 0.0023) gives n_s = 0.971–0.974 and r ≈ 0.002 over the same N* range, consistent with both data sets. Which branch is right is decided mainly by the CMB-vs-BAO question about n_s.

The contributions are:
- the two-branch prediction and its r range (≈10⁻³, in principle separable from in-class modular hilltops with r ≲ 10⁻⁶);
- an explicit, anomaly-checked assignment of the known modular-centre parity (arXiv:2207.14014) that protects the proton to dimension 6 perturbatively while ⟨W⟩ = 0;
- an audit trail that includes the withdrawn claims.

# 1. The picture

A two-torus has a shape τ in the upper half plane, and tori related by SL(2,ℤ) are the same torus.

* **Stretched torus (Im τ ≫ 1): inflation.** The potential approaches a constant plateau. With K = −ln(2 Im τ) the canonical field gives V ≈ V₀(1 − b e^{−√2 φ}), the α = 1/3 attractor form.
* **Relaxation: reheating.** The shape oscillates about the square torus and reheats gravitationally (T_RH ≈ 2–6×10¹⁰ GeV). Standard cosmology follows.
* **Square torus (τ = i).** This is the fixed point of τ → −1/τ and here a heavy supersymmetric Minkowski minimum with V = 0. Today's Λ comes from elsewhere (§2).
* **Hexagonal torus (τ = ρ = e^{iπ/3}).** The other fixed point; in SERAPIS it is a wall.

These are the only fixed points of SL(2,ℤ), the lattice counterpart of the crystallographic restriction (a 2D lattice admits only 1-, 2-, 3-, 4- and 6-fold rotations).

# 2. The model

**Kähler potential and superpotential.** One torus: K = −ln(2 Im τ). With a nilpotent stabiliser S, W = S·F(τ) and V = e^K|F|². Modular invariance requires F of weight −1, so F = η(τ)⁻² H(j). We take

H = (E₆/η¹²) · j^(−7/12) · [ln(j/1728) + κ]^(1/2),  κ = 1,

where E₆/η¹² ∝ (τ − i) is the holomorphic square root of j − 1728 (D537 corrects the principal-branch form used before).

What each factor does:
- j^(−1/12) cancels |η|⁻⁴ on the cusp, and [ln j]^(1/2) cancels 1/(2 Im τ); together they give the plateau.
- E₆/η¹² makes τ = i a quadratic (stiff) supersymmetric minimum.
- j^(−7/12) makes τ = ρ a wall.

**Status of H.** The plateau factors j^(−7/12) and [ln(j/1728)+κ]^(1/2) lie outside the string-derived Cvetič–Font–Ibáñez–Lüst–Quevedo class, H = (j−1728)^{m/2} j^{n/3} P(j) with integer m, n and polynomial P (D535). In that class no potential has an exactly flat cusp plateau. SERAPIS's plateau is therefore an effective, modular-invariant choice, not a string derivation. The exponents and κ were chosen by hand after earlier variants (D513–D516).

**Vacuum.** At the model's own N*, m = 4.2–4.5×10¹³ GeV ≈ 4.9 H_inf (D539). So there is no fifth force and no cosmological-moduli problem.

**Λ (withdrawn claim).** The earlier statement that "a constant c sets V(i) = Λ, with c ≈ e^{−121.6} instanton-sized" is withdrawn. A constant term has the opposite S-character to E₆/η¹² and breaks modular invariance. In the holomorphic model the vacuum at i has V = 0. An S-even, non-vanishing H makes τ = i a saddle unless the vacuum is light (D538). A positive Λ therefore needs a separate uplift, for example hidden matter as in Knapp-Pérez et al. (arXiv:2304.14437). It is tuned exactly as in arXiv:2405.06497.

# 3. The branches and the data

| Branch | N* | n_s | r | α_s | fitted tilt | vs CMB-SPA | vs SPA+DESI |
|---|---|---|---|---|---|---|---|
| **SERAPIS–Kairos** (own reheating, D519; grid D526) | 52–55.6 | 0.963–0.965 | 0.0012–0.0013 | ≈ −6.6×10⁻⁴ | none | −1.1σ … −1.8σ | −2.8σ … −3.7σ |
| **SERAPIS–Chronos** (plateau power ½+δ, δ = 0.0023, D525; grid D526) | 52–55.6 | 0.971–0.974 | 0.0020–0.0022 | ≈ −5.9×10⁻⁴ | one | +0.9σ … +1.7σ | −0.6σ … +0.3σ |

Comparisons use CMB-SPA n_s = 0.9684 ± 0.0030 and CMB-SPA+DESI 0.9728 ± 0.0027.

- **Reheating (D518–D520, D534).** The heavy shape decays gravitationally and reheating is matter-dominated. A stiff, kination-like phase is impossible here: even at the minimum mass needed to reheat, the oscillations stay quadratic (D534). So Kairos cannot reach the DESI-including value by changing reheating.
- **Parameter sensitivity.** κ moves n_s by < 0.003 for κ ≲ 6. κ = 7 shifts it; κ = 8 breaks the plateau (D526). Other functional forms of H would give other numbers.
- **Interpretation.** The DESI pull on n_s is tied to the BAO–CMB tension and can be mimicked by a shift in the optical depth τ_reio (McDonough & Ferreira, arXiv:2512.05108). Kairos's numbers are those of a standard α-attractor: arXiv:2510.18656 finds 0.958–0.963 for that class.

**Late universe.** The field sits at the minimum, so dark energy is a cosmological constant (w₀ = −1, w_a = 0), supplied by the separate Λ sector of §2.

# 4. Matter and the extra dimensions

* **Where the torus lives (D530, D532).** Exact SL(2,ℤ) on one torus needs a factorised lattice T² ⊕ T⁴, with the SERAPIS torus as the N = 2 fixed plane. Non-factorisable orbifolds reduce the symmetry to congruence subgroups (Mayr–Stieberger, hep-th/9303017). In type IIB, flux on that T² breaks SL(2,ℤ) unless the fluxes also transform, and it favours τ = ω (Ishiguro–Kobayashi–Otsuka, arXiv:2011.09154). So the SERAPIS T² must carry no flux. A concrete compactification is not constructed here.
* **Proton protection (D527–D529, D533).** The centre of SL(2,ℤ) leaves τ fixed, so matter fields of weight n/M carry a Z₂M that survives at every τ (Kobayashi et al., arXiv:2207.14014).
  - In the supergravity convention required here (W of weight −1), family-independent Z₄^R and Z₈^R assignments allow the Yukawa, μ and Weinberg terms. They forbid all dimension-4 and dimension-5 proton-decay operators and the dimension-6 Kähler operators QQU†E† and QLU†D†.
  - Some of these pass the Ibáñez–Ross condition A₃ ≡ A₂ (mod N/2): 8 of 16 for Z₄^R and 16 of 96 for Z₈^R. Green–Schwarz-induced breaking is safe for δ_GS ≲ 6 (D533; order-of-magnitude bounds).
  - Caveats: a non-zero ⟨W⟩ (gravitino mass) breaks this R-symmetry. Hypercharge and gravitational anomalies were not checked. Compare the known Z₄^R of Lee–Raby–Ratz–Ross et al. (arXiv:1102.3595), which forbids μ perturbatively.
* **Earlier realisation (Twist-2, D436–D489).** A rolling Kähler modulus captured by a stringy Fayet–Iliopoulos term on a magnetised D7-brane. Capture works for string scales 3×10⁻⁵–0.3 M_P and soft masses 1 eV–100 TeV (D446, D452, D460, D483). It requires:
  - hidden-sector annihilation of the remnant (D447, D455, D468);
  - baryon-number protection (D469);
  - gauged DM stability (D473);
  - a fibred Calabi–Yau (D462).

  SERAPIS replaces capture with a symmetry-fixed heavy minimum.

# 5. Predictions and tests

1. **n_s** to ±0.002 (Simons Observatory and CMB-S4-class experiments): Kairos 0.963–0.965 vs Chronos 0.971–0.974.
2. **r**: both branches give r ≈ 1–2×10⁻³, separated from each other only at ≈1σ by LiteBIRD/CMB-S4-class σ(r) ≈ 10⁻³. With σ(r) ≲ 4×10⁻⁴ (delensed CMB-S4-class sensitivity), r ≈ 10⁻³ would be distinguishable from in-class modular hilltops (r ≲ 10⁻⁶; arXiv:2405.06497, 2405.08924), D536; at LiteBIRD's σ(r) ≈ 10⁻³ the difference is ≈1σ. A firm limit r < 5×10⁻⁴ would exclude both SERAPIS branches.
3. **w₀ = −1, w_a = 0** (DESI DR3+, Euclid). A confirmed w₀ > −1 disfavours the model, whose Λ is a constant.
4. **ΔN_eff ≈ 0.05–0.08** in the realisations with a light gravitino (D463, D511): a 2σ-level hint at CMB-S4-class sensitivity (Twist-2/Twist-M-L realisations; a non-zero gravitino mass breaks the §4 R-parity, so the two are not yet shown compatible).

# 6. Prior art (credited)

- **Modular-invariant superpotentials from gaugino condensation:** Cvetič, Font, Ibáñez, Lüst, Quevedo (1991); Font, Ibáñez, Lüst, Quevedo (1990); Gonzalo, Ibáñez, Uranga, arXiv:1812.06520; Leedom, Righi, Westphal, arXiv:2212.03876 (no dS at fixed points); Knapp-Pérez et al., arXiv:2304.14437.
- **Modular-invariant inflation:** arXiv:2405.06497, 2407.12081 (log-type plateau; also species-scale control), 2405.08924, 2411.18603, 1604.02995, 2403.02125, 2503.13682.
- **α-attractors:** Kallosh, Linde and collaborators; arXiv:2510.18656 (n_s for attractors with reheating).
- **Fixed points and trapping:** attraction of moduli to fixed points, arXiv:2211.00659; trapping at enhanced-symmetry points, hep-th/0403001.
- **Moduli fixing and orbifold structure:** D-term moduli fixing, arXiv:1110.3333; threshold duality groups in orbifolds, hep-th/9303017; flux statistics, arXiv:2011.09154.
- **Matter parities:** arXiv:2207.14014, 1812.11072, 1102.3595; Ibáñez–Ross (1991); Dreiner, Luhn, Thormeier, hep-ph/0512163.
- **Other:** quintessential inflation (Peebles–Vilenkin; arXiv:2311.02730); exponentially small Λ from flux vacua, arXiv:2107.09064/09065; fibre inflation, arXiv:0808.0691; Planckian interacting dark matter, arXiv:1709.09688; light-gravitino bounds, arXiv:1601.07386, 1608.01610; modular quintessence, arXiv:2506.02731; n_s and the BAO–CMB tension, arXiv:2512.05108.

# 7. Open problems

- A string origin of the plateau factors (outside the CFILQ class, D535).
- The Λ sector (separate uplift, tuned; D537, D538).
- A concrete factorised, flux-free compactification with the SERAPIS T² as N = 2 plane, and the Standard Model on branes that do not wrap it.
- The embedding of the Z₄^R/Z₈^R parity in that compactification, with its full anomaly check, and its fate once the gravitino mass is non-zero.
- The full Twist-2 capture runs J1–J3 (D500 etc., running).

# Method and data

Every scored test was pre-registered: a PREREG file with its SHA-256 was committed and pushed before running. Most locks precede their results by tens of seconds to minutes. That prevents changing verdicts afterwards, but not exploratory work before a lock.

Several notes are reasoning or literature only, marked as such in the log; examples are D520, D521, D527, D530, D532, D535, D536 and D538. Fixes were written as DEVIATIONS files; in one case (D525) the deviation was committed together with its rerun result. Failed, superseded and withdrawn results are kept, including D517's Λ claim, withdrawn in D537 after an independent referee check.

Code, locks and results are in the AEGIS repository (branch unify-bg): theory/modular/, field_tests/rules/, field_tests/results/. AI assistance (Claude, Anthropic) was used for literature search, code, drafting and the referee review. All numbers are from code.
