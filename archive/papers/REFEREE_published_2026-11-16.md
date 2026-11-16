# Referee report on three published Zenodo preprints (cold read, 16 Nov 2026)

Scope: The Twist v5.3 (10.5281/zenodo.24226521), the α no-go paper (10.5281/zenodo.24232382) and Twist-2 v1 (10.5281/zenodo.24235736). I checked each against its D-notes (theory/pending_docs/D72_D75_weak_spots.md), against field_tests/results/, and against the current model (papers/v3/serapis_v3.tex, SERAPIS v3, DOI 10.5281/zenodo.24250733). I used four web searches plus three fetches of the pages they returned. I made no edits except writing this file.

Overall verdict. The α no-go paper is the only one of the three that stands on its own. It needs a v2: the title claims too much, one bound is quoted from the wrong MICROSCOPE paper, and it misses a stronger published bound. The two Twist papers describe a model line the author has dropped; the current model is SERAPIS, a different field with no dark-energy claim. Both Twist papers also contain numbers that later notes contradict. Neither deserves a full rewrite. Each needs a status notice, plus a short corrections addendum for the numbers that are actually wrong.

---

## 1. "The Twist" v5.3 (v5 main text + ERRATA_v5.3)

**Recommendation:** Supersede. Publish v5.4 with a status notice and a one-page addendum that carries the items below which are not yet in the published errata. Do not write a full v6.

### Major issues

**1. The late-time "locked predictions" belong to a variant that existing data already exclude.**
- Quoted (Abstract and §6): "a set of predictions locked before the data that will judge them: r, the tail's w(z), no cosmic birefringence from this field, and the redshift shape of any shield leak". The LAB-NULLS row predicts "no fifth force, no α_em drift".
- What is wrong: The published errata (item 16; D323–D334) shows that the shield fails at one loop: d ln α_em/d ln x ≈ 7×10⁻³. Under the paper's own assumptions (K = −3 ln(T+T̄), x-independent f and Yukawas), the thawing tail therefore predicts an α drift about 10⁵–10⁶ times above the clock bound (D400; the companion paper). So LAB-NULLS and SHIELD are already contradicted by theory plus existing clock data. WATCH-PURE-DR3, WA-CEILING and GROWTH score a variant that is not viable unless an unknown mechanism exists. The "leak" in §5.1 is not a small c_p/x^p term: the paper's own clock limit is |d ln α/dφ| < 1.6×10⁻⁸, against a one-loop value ζ ≈ 5.7×10⁻³.
- Source: ERRATA_v5.3 item 16; D324, D334, D400; ALPHA_NOGO_v1 §4.
- Replacement: "The tail tests (WATCH-PURE-DR3, WA-CEILING, GROWTH, SHIELD, LAB-NULLS) apply only to the thawing-tail variant. At one loop that variant predicts d ln α_em/d ln x ≈ 7×10⁻³, which existing clock and MICROSCOPE bounds exclude unless the Standard Model is decoupled by a mechanism not known in any string construction (D323–D334, D400). Of the locked tests, only those on r, n_s and β remain relevant."

**2. The n_s distances in §3.2 disagree with the source the paper cites.**
- Quoted (§3.2): "It is −1.7σ from CMB-SPA alone (0.9693 ± 0.0029). It is −3.7σ from CMB-SPA + DESI (0.9737 ± 0.0025)."
- What is wrong: Ref. [4] (Ferreira et al., arXiv:2507.12459) gives CMB-SPA n_s = 0.9684 ± 0.003 and CMB-SPA + DESI n_s = 0.9728 ± 0.0027 (verified on the arXiv HTML). For the paper's band 0.9642–0.9654 that means 1.0–1.4σ and 2.7–3.2σ. At the current TWIST-I value 0.9648 (D387) it is 1.2σ and 3.0σ. The errata's own summary (item 3) already uses 1.2σ and 3.0σ, so the main text and the errata disagree. "Planck + ACT + DESI (0.9743 ± 0.0034) … 2.7–3.3σ" should be 2.6–3.0σ for the stated band.
- Source: D385, D387; arXiv:2507.12459.
- Replacement: "Against CMB-SPA (0.9684 ± 0.0030 [4]) the Twist (n_s = 0.9648, N* = 56.7, D387) is 1.2σ low. Against CMB-SPA + DESI DR2 (0.9728 ± 0.0027 [4]) it is 3.0σ low, and against P-ACT-LB (0.9743 ± 0.0034) it is 2.8σ low."

**3. The inflation numbers in the abstract, §2.4, §3.1 and §6 are withdrawn.**
- Quoted: "n_s = 0.9642–0.9654 and r = 0.0035–0.0038"; "N* … 55.7 (instant) to 57.6 (derived f_heat, including kination)"; the table row "derived … 57.6 | 0.9654 | 0.0035".
- What is wrong: The value 57.6 came from a run without the hidden σ sector and is withdrawn. On the full trajectory N* = 56.70, n_s = 0.9648, r = 0.0037 (D387, results/nstar_traj_d387.txt). The running −6.0×10⁻⁴ and n_t −4.4×10⁻⁴ were quoted at N* = 57.6. The errata says this only as an "update". Every 57.6-based number in the main text is still live.
- Source: D387, D391; ERRATA item 19.
- Replacement: "On the full trajectory N* = 56.7, n_s = 0.9648, r = 0.0037 and α_s ≈ −6.2×10⁻⁴ (instant reheating: N* = 55.7, n_s = 0.9642, r = 0.0038)."

**4. The NS-SPA verdict depends on where the n_s band is cut, and the paper does not say so.**
- Quoted (Abstract): "fixing n_s at the Twist value costs Δχ² = 11.7, against a locked threshold of 9."
- What is wrong: The rule fixed n_s = 0.964, the bottom of the band (PREREG_NS_SPA; ns_spa.json: cost 11.734, n_s free 0.9756). A quadratic estimate from the same fit (σ_eff = 0.0034) gives Δχ² ≈ 10.2 at the current value 0.9648 and ≈ 9.1 at 0.9654, essentially at the threshold. The rule was also written with the stored ΛCDM fit (n_s 0.9732) in view (PREREG_NS_SPA line 7). It quantifies a known tension; it is not a blind test. The INCONSISTENT reading stands as scored, but "failed its own pre-registered test" reads as stronger than the margin.
- Source: field_tests/results/ns_spa.json; PREREG_NS_SPA.md; D387; crown D410 (7.95 at 0.9651 with a different data combination).
- Replacement: "Fixing n_s = 0.964 (the low end of the band) costs Δχ² = 11.7 against the locked threshold 9 (INCONSISTENT). At the current n_s = 0.9648 the cost is about 10 (quadratic estimate, not a rescoring). The tension is driven by CMB + BAO jointly and is ~1σ against the CMB alone."

**5. The closest prior paper is not cited.**
- Quoted (§9): "The contribution here is narrow: 1. a stabiliser construction …"
- What is wrong: arXiv:2008.09099 (quintessential inflation in no-scale supergravity, with kination, instant preheating and the residual potential as dark energy) is "structurally the v5 Twist" (D398). It is missing, as are Ellis–Nanopoulos–Olive (arXiv:1307.3537), Choi (hep-ph/9902292) and Dimopoulos (hep-ph/0702018). These fixes are queued in CORRECTIONS_FOR_v6 items 22–23 but are absent from the published v5.3 errata.
- Source: D398, D399; CORRECTIONS_FOR_v6 item 23.
- Replacement (add to §9): "Quintessential inflation in no-scale supergravity with kination and a residual dark-energy potential was constructed in arXiv:2008.09099. The present model differs in the cliff construction and the locked test record, not in the overall structure."

**6. "Derived" is used for quantities that depend on choices.**
- Quoted (Abstract): "a single-field supergravity embedding with a derived axial coupling". §9 says: "a derived (normalisation-dependent) axial coupling".
- What is wrong: c_A = √(3/8) follows only after the author chooses the normalisation (§2.2). The alternative reading changes the matter yield by a factor of 0.44 (ERRATA item 2). The coupling is also used only by the exploratory matter mechanism, which Twist-2 dropped (D395).
- Replacement: "an axial coupling c_A = √(3/8) that follows once the Nieh–Yan current is taken to couple to the canonically normalised angle (a stated choice)".

**7. Items still uncorrected in the published record.**
- §4.4 "CMB-inferred H₀ falls to ≈ 65.7" should read 66.8 (full fit; ΛCDM 68.0; D332, ns_pure.json). The errata summary mentions this but has no itemised correction.
- §5.2 gravitino (m_3/2 = 10¹¹–10¹⁴ GeV, R-parity violation) is superseded by the eV-gravitino sector (ERRATA items 1, 9) and later narrowed to 1.7–4.7 eV (D430, D474).
- §6 "CMB-S4 class" should be removed (CMB-S4 cancelled; D346). "SO can detect r ≈ 0.0036 at 3–5σ (2028–2035)" should read "~3σ by ~2035" (ERRATA item 17).

**8. Post hoc choices and tests.**
The paper is candid that μ = 1 and the e^{−πx/4} cliff were fixed after the data (§4.3). However, the abstract still lists "the tail's w(z)" under "predictions locked before the data". The tail shape was reshaped after TAIL-F failed (Δχ² = +29.2, tail_f.json). Locking it before DR3 is legitimate, but DR3 is cumulative with DR2, which the paper itself notes. The abstract should say "locked after a failed test, for scoring on DESI DR3/Euclid" rather than imply an a priori prediction.

### Minor issues
- Selective reporting, in the conservative direction. NS-PURE (ns_pure.json, Planck NPIPE + DESI + Pantheon+) gave PURE −3.85 vs ΛCDM with its gate failed (NO VERDICT). The paper reports only the +1.45 from NS-SPA. Report both in one line.
- β_CMB: §5.4 uses 0.277° ± 0.057° (arXiv:2608.06480). Other notes use 0.261 ± 0.061° (D403), 0.215 ± 0.074° and 0.37 ± 0.11° (D386), and ~0.3° at 4.6σ (D404). Pick one source and use it everywhere.
- The TWIST-INFLATION frozen band 0.0037–0.0040 versus the computed 0.0036–0.0037 (D387/D391): state that the rule is scored as frozen.
- "n_s cannot be raised inside the model" is true only for the undeformed W. Route A raises it with ε ≈ 3×10⁻⁷ (D419). Say "without changing W or K".
- DOI bookkeeping: the errata header cites the v5 DOI (24210532). A reader landing on the v5.3 record should see 24226521 on the PDF.

### Status relative to the current model
Superseded twice. First by TWIST-I and Twist-2 (the field is captured and w = −1), and then by SERAPIS. SERAPIS uses a different field (the torus shape τ), has no cliff, no capture and no tail, and its vacuum energy is tuned by hand (serapis_v3.tex §chain: "f² = 3|W₀|² for Λ = 0"). Nothing in v5 carries over to SERAPIS except the method (locked rules) and the lesson that an α = 1 plateau with N* ≈ 57 sits ~3σ below CMB+DESI.

Draft status notice:
> STATUS (16 Nov 2026). This record is superseded and kept for the test record only. Its thawing-tail dark energy is excluded at one loop by gauge-coupling drift (10.5281/zenodo.24232382). Its inflation sector (n_s = 0.9648, N* = 56.7 after D387) is 3.0σ below CMB-SPA + DESI DR2. The author's current model is SERAPIS (10.5281/zenodo.24250733), a different modular-inflation model that makes no dark-energy claim.

### Titles (proposed)
1. "One no-scale field for inflation and dark energy: a pre-registered test record, with a disfavoured n_s and an unsupported tail"
2. "Plateau, cliff and tail in no-scale supergravity: what pre-registered tests kept and what they rejected"

### Checks done
- Δχ² values against tournament.json/pure_twist.json (−3.372, −0.886, −0.406, −2.668), tail_f.json (+29.228), desi_holdout.json (+12.462) and ns_spa.json (11.734, 8.46, +1.452, n_s 0.9756): all match.
- Significance arithmetic: √3.37 = 1.84σ, two-sided p = 0.066; Šidák with 6 and 12 trials gives 0.96σ and 0.58σ. Matches.
- n_s distances recomputed against arXiv:2507.12459 (web-verified): the main text is wrong (item 2).
- N*, n_s and r against D387/D391 and nstar_traj_d387.txt; running and n_t against bridges_d403.txt.
- H₀ against ns_pure.json (66.78 vs 68.00). Cassini ratio 0.41/0.0034 = 120 checks. μ = 1 slope shares 73/74 and 89/90 check.
- Prior art against D398/D399. Errata coverage against CORRECTIONS_FOR_v6 (items 22–23 are missing from the published v5.3).

---

## 2. α no-go: "One-loop gauge-coupling drift rules out modulus quintessence at DESI-preferred dark energy"

**Recommendation:** Issue v2 with corrections. The core result holds, and the bound gets stronger with correct inputs.

### Major issues

**1. The title and abstract claim more than the paper shows.**
- Quoted (title): "… rules out modulus quintessence …". Quoted (§7): "A modulus with a logarithmic Kähler potential cannot be the evolving dark energy that DESI prefers unless …".
- What is wrong: The result is a one-loop estimate under stated assumptions. These are: a visible MSSM-like sector in the same supergravity, whose e^K contains the rolling field; X-independent holomorphic f_a; universal (Yukawa-fixed) matter metrics; and α_em only. §5 itself lists open escapes: sequestering, per-factor GS, axions, screening. Choi (1999) already made the qualitative exclusion, and the project's own notes call D323 "a refinement of a known result, not a new no-go" (D399). "Rules out modulus quintessence" reads as model-independent.
- Source: D399, D401 ("framed as a quantitative sharpening"), §5–6 of the paper.
- Replacement title: see below. Replacement abstract sentence: "Under these assumptions a Kähler modulus that rolls as fast as the DESI-preferred fits require violates clock and equivalence-principle bounds by factors of 10³–10⁷, so such a modulus needs its one-loop coupling to the visible sector suppressed by at least ~10³ in ζ, and by ~10⁵ using the combined bound of arXiv:2105.09746."

**2. The MICROSCOPE value does not match the citation, and the bound is out of date.**
- Quoted (§4): "the MICROSCOPE equivalence-principle result η = (−0.1 ± 1.3)×10⁻¹⁴ [16]", where [16] = Touboul et al., PRL 129, 121102 (2022).
- What is wrong: (−0.1 ± 1.3)×10⁻¹⁴ is the 2017 first result: [−1 ± 9(stat) ± 9(syst)]×10⁻¹⁵, PRL 119, 231101. The cited 2022 final result is η(Ti,Pt) = [−1.5 ± 2.3(stat) ± 1.5(syst)]×10⁻¹⁵ (verified on arXiv:2209.15487), about 5× tighter. With it the 1σ bound is ζ ≲ 1.7×10⁻⁶ (not 3.6×10⁻⁶), the required suppression is 2.0–3.4×10³, and the predicted η exceeds the bound by 3.9×10⁶–1.2×10⁷σ. The same input error appears in PREREG_D400 and desi_alpha_d400.txt. The conclusion is unchanged; only the numbers grow.
- Source: arXiv:2209.15487; PREREG_D400_DESI_ALPHA.md line 11.
- Replacement: "MICROSCOPE's final result η(Ti,Pt) = (−1.5 ± 2.3_stat ± 1.5_syst)×10⁻¹⁵ [16] gives, with η ≈ 10⁻³ζ² [17], ζ ≲ 1.7×10⁻⁶ at 1σ." Then recompute the η column and note that the locked run used the 2017 value (record it as a deviation, not a silent edit).

**3. A combined published bound that is ~60× stronger is missing.**
- What is wrong: Martins et al. (arXiv:2105.09746) combine quasars, clocks and MICROSCOPE and get ζ = (−3.6 ± 5.9)×10⁻⁸. That makes the required suppression ~5×10⁴–10⁵ rather than ~10³. D421 found this after publication and queued it for v2.
- Source: D421.
- Replacement (§4): "The combined quasar + clock + MICROSCOPE analysis of [Martins et al., arXiv:2105.09746] gives ζ = (−3.6 ± 5.9)×10⁻⁸, so the one-loop value ζ = (3.3–5.7)×10⁻³ must be suppressed by ~10⁵."

**4. Significance language: "~10⁶σ" is not a meaningful statistic.**
- Quoted (Abstract): "These exceed the ESPRESSO, optical-clock and MICROSCOPE bounds by ~10²–10³σ, ~10⁶σ and ~10⁶σ."
- What is wrong: A pull of 10⁶ standard deviations comes from Gaussian tails extrapolated far beyond their validity. It also mixes metrics: η scales as ζ², so the "10⁶σ" in η is a factor 10³ in ζ. Twist-2 §1 repeats this as "violates … by ~10⁶". State ratios.
- Replacement: "The predicted values exceed the ESPRESSO, clock and MICROSCOPE 1σ uncertainties by factors of ~10²–10³, ~10⁶ and ~10⁷ respectively; in terms of the coupling ζ, the excess is ≳ 10³ (MICROSCOPE) and ~10⁵ (combined bound [2105.09746])."

**5. The result is stronger and less DESI-dependent than the title suggests.**
- What is wrong: The paper's own clock relation (§4, "null test") gives 1 + w₀ ≲ 2–6×10⁻¹³ today for k = 1–3. This is an estimate from R with the 1σ clock error, Ω_DE = 0.69. So any measurable thawing of a rolling modulus is excluded, not only the DESI-preferred CPL fits. Because the title ties the result to DESI, a reader may think it weakens if DESI's preference fades. It does not.
- Replacement (add to §4): "Applying R today with the clock bound requires 1 + w₀ ≲ 10⁻¹² for k = 1–3. The exclusion therefore does not depend on the DESI preference: any observable thawing of such a modulus is excluded, under the assumptions of §6."

**6. One assumption is unstated.**
- What is wrong: The no-go needs X-independent holomorphic gauge kinetic functions f_a (beyond a universal GS term). §2 says only that "the point is not a tree-level coupling, which can be tuned away". The precise statement is in ERRATA v5.3 item 16 and D334 ("x-independent holomorphic f and y"). For k ≠ 3 the "locality" weights n_r = k/3 are a requirement (x-independent Yukawas), not a derived locality result. D401 asked for an independent check for k ≠ 3, and D402 checked only the volume case.
- Replacement (§2): "We assume that the holomorphic gauge kinetic functions and Yukawa couplings do not depend on X (a shift symmetry of Im X forbids non-linear dependence; linear dependence is a tree-level coupling, which is far more constrained). For k ≠ 3 we impose n_r = k/3 by requiring X-independent Yukawas; we have not derived it from a string locality argument."

### Minor issues
- "prefer a time-dependent dark-energy equation of state, at 2.3σ to 4.2σ": DESI DR2's own abstract gives 3.1σ (DESI+CMB) and 2.8–4.2σ with supernovae (web-verified). Quote that, or say which analysis gives 2.3σ.
- Table "vs ESPRESSO" uses σ = 1.4 ppm (stat ⊕ sys). Say so in the text.
- Only 4 of the 9 fit/k combinations are tabulated, and the abstract range 3.5–10×10⁻⁴ covers all 9. Fine, but state "all nine in [11]" next to the abstract range.
- Ref [2] and ref [3] have no author names. Ref [18] has no authors.
- "This sharpens the qualitative argument of Choi (1999)": good. Also cite hep-ph/0402075 (moduli quintessence and varying α), as D399 recommends.

### Status relative to the current model
This paper stands on its own. Its result does not depend on the Twist, and SERAPIS does not touch it: SERAPIS has w = −1 and a heavy inflaton at the vacuum. It is the most durable of the three records. It should no longer be framed as "arising from" a model the author has dropped (Acknowledgements); a neutral line is enough.

Draft status notice:
> STATUS (16 Nov 2026). The central result, a one-loop drift d ln α_em/d ln x = 7.0×10⁻³ (k/3) for a rolling Kähler modulus, stands. v2 corrects the MICROSCOPE input (the final 2022 value strengthens the bound about fivefold), adds the combined bound of arXiv:2105.09746 (required suppression ~10⁵ in ζ), states the assumptions explicitly, and replaces "rules out" with a conditional statement.

### Titles (proposed)
1. "Rolling moduli move α: a one-loop obstruction to Kähler-modulus quintessence from clocks and MICROSCOPE"
2. "Anomaly-fixed gauge-coupling drift versus a thawing modulus: why dark energy from a Kähler modulus needs a 10⁵ suppression"

### Checks done
- Coefficient: kl_coeff.txt reproduces −b_a, d ln α_em/d ln x = 6.968×10⁻³, an empty solution set with μ, and n_Hu + n_Hd = 12 without it. Hand check: d(1/α_em) = −(1 + 5/3·33/5)/4π = −0.955.
- Canonical map d ln x/dφ = √(2/k), from K_XX̄ = k/(X+X̄)².
- Table against desi_alpha_d400.txt: all nine rows match. R bridge: 1.8×10⁻¹⁹/(6.89×10⁻¹¹ × √(3·0.69·0.167)) = 4.4×10⁻⁹, with ±6.2×10⁻⁹. Matches.
- MICROSCOPE final value (web, arXiv:2209.15487): mismatch with the paper (item 2).
- DESI DR2 significance (web, DESI DR2 abstract): 3.1σ; 2.8–4.2σ with SNe.
- ESPRESSO (1.3 ± 1.3 ± 0.4 ppm) and Filzinger clock (1.8 ± 2.5)×10⁻¹⁹ yr⁻¹ agree with the locked rule. Not independently re-verified online (search budget).
- Later notes: D421 (missed combined bound) and D399 (novelty). No later note contradicts the coefficient.

---

## 3. Twist-2 v1: "one no-scale field for inflation and the vacuum energy …"

**Recommendation:** Add a status notice plus a v1.1 corrections addendum, covering the queued items D422/D427/D428/D430 and the issues below. Do not write a full v2: the capture mechanism the paper describes (the λ(T − T_E)χχ̄ condensate) was itself replaced by the FI-term picture (D436–D486), and the line was then dropped for SERAPIS.

### Major issues

**1. "Every data block fits better than ΛCDM" describes a background Twist-2 does not have.**
- Quoted (Abstract): "One tiny holomorphic deformation … fits n_s = 0.9736, after which every data block fits better than ΛCDM". §5: "With the deformation (n_s = 0.9736) every block fits better than ΛCDM (CMB −2.77, BAO −0.41, SNe −2.48)."
- What is wrong: Those numbers are the THAW_FREE fit: thawing dark energy with w₀ = −0.956 on the line w_a = −1.58(1+w₀), with n_s free (crown_d410.json; D419). The Twist-2 baseline is w = −1 (§1, §4: "w −1 (baseline)"), and the paper's own companion work excludes a thawing modulus. With w = −1 and n_s = 0.9736, the fit is ΛCDM with n_s free (0.9737): Δχ² ≈ 0 against ΛCDM, not better. The thawing improvement (−2.15 in total) also costs one extra parameter (ΔAIC ≈ −0.15) and belongs only to the single-axion variant. The paper itself says that variant fails DESY5 (D393) and needs f ≈ M_P. Finally, the agreement exists only because ε was fitted to n_s after the crown failed (D410 scored, then D419 locked).
- Source: crown_d410.json; D410, D419, D393.
- Replacement: "With ε fitted to n_s = 0.9736, the baseline (w = −1) fits as well as ΛCDM with free n_s, by construction. A thawing background lowers χ² by a further 2.2 at the cost of one parameter. That background would need the separate single-axion variant, not the baseline."

**2. The claim that "every computation was pre-registered" is false.**
- Quoted (Abstract): "Every computation was pre-registered (rule and hash committed before running)." §3 header: "all numbers from locked runs". §7: "Every number above comes from a short script whose rule … was written and hashed before it ran."
- What is wrong: The leptogenesis row is cited to D394 ("estimate in code; not locked") and D411 ("no new locked computation"). The α-after-capture row cites D417 ("consistency arithmetic … no new locked computation"). The dark-matter row relies on D112/D415, and the Λ-sensitivity reading on D413. The paper's own sources label several entries as unlocked estimates.
- Source: D394, D411, D417.
- Replacement: "Numbers marked [L] come from pre-registered runs; leptogenesis (D394, D411) and the post-capture α estimate (D417) are unlocked estimates."

**3. "Residual potential sets the vacuum energy" and "needs no tuning" overclaim (D427, D456).**
- Quoted (Abstract): "captured at a point x_E ≈ 29.6 where its residual potential sets the vacuum energy". §3 table: "Λ ∝ x_E^(−0.97): pinning point needs no tuning".
- What is wrong: The χ condensate carries a soft vacuum energy of ~10²⁶–10³² GeV⁴, which is 10⁷²–10⁷⁹ ρ_Λ. That energy must be cancelled by the same one-off cosmological-constant tuning that already cancels the SUSY-breaking energy (D427). Only after that cancellation is the leftover the cliff value. The depth n ≈ 124.1 is itself chosen to match ρ_Λ (v5 §2.4), and in the string toy the O(1) factor is selected by flux integers (D456). The model accounts for an order of magnitude given two tunings; it does not explain Λ. "Needs no tuning" refers only to the insensitivity to x_E.
- Replacement: "After the usual one-off cancellation of the vacuum energy (which must also absorb the χ-condensate energy, ~10⁷² ρ_Λ), the leftover x-dependent piece is the cliff value e^{−2n} at x_E. The depth n ≈ 124.1 is chosen to match ρ_Λ. Λ is insensitive to the exact capture point (Λ ∝ x_E^{−0.97})."

**4. ΔN_eff, the dark-radiation products and the gravitino window are wrong per later notes (D422, D430, D463, D474).**
- Quoted (Abstract, §4): "extra radiation ΔN_eff ≈ 0.05–0.10 (hidden pair 0.034 + gravitino 0.047)"; "a light gravitino ≤ 4.7 eV"; §3: "The decay products, a hidden vector-like pair, are dark radiation."
- What is wrong: The decay products are heavy (m_ψ ≈ 5×10⁵–10⁹ GeV) and must decay to the SM through an L-conserving lepton portal, so the hidden-pair 0.034 is withdrawn. The capture-sector ΔN_eff is then 0.02–0.06 from the gravitino alone (D422, D430), or 0.065–0.081 in the later FI picture (D463). The gravitino is bounded below as well: 1 eV ≲ m_3/2 ≤ 4.7 eV (D430), narrowed to 1.7–4.7 eV (D474).
- Replacement: "ΔN_eff ≈ 0.02–0.06 (gravitino only; the x decay products are heavy and decay to leptons) and m_3/2 ≈ 1.7–4.7 eV (√F ≈ 85–140 TeV)."

**5. The birefringence discriminator threshold is wrong (D428).**
- Quoted (§4 table): "β_reio/β_rec < 1 if m_a ≳ 20 H₀ (LiteBIRD)".
- What is wrong: At 20 H₀ the ratio is 0.85–0.94, which cannot be told apart from miscalibration (ρ ≈ 1). A useful difference |1 − ρ_β| ≥ 0.2 needs m ≳ 30–40 H₀, and ρ_β ≈ 0 for m ≥ 100 H₀.
- Replacement: "ρ_β = β_reio/β_rec ≲ 0.8 for m_a ≳ 30–40 H₀ and ≈ 0 for m_a ≥ 100 H₀; for m_a ≲ 20 H₀ it is indistinguishable from a calibration error."

**6. The Route A "genuine tests" do not single out Twist-2 (D464, D475), and the ε window is out of date (D434).**
- Quoted (§5): "the genuine tests move to r, α_s and B1". "The ε window for n_s within ±0.003 is (1.8–3.7)×10⁻⁷." Abstract: "r about twice the plain-Starobinsky value at the same n_s".
- What is wrong: Route A's (n_s, r) = (0.9736, 0.0046) lies on the fibre-inflation / α ≈ 2 line (r = 0.0042 there; α_eff = 2.2, D464), and α_s does not separate the two either (0.2σ, D475). So r, α_s and B1 test Route A against Starobinsky, not Twist-2 against known α ≈ 2 models. The computed ε window is 2.0–4.0×10⁻⁷ (D434). "Tiny" is also misleading: the relevant ratio is ε/x* ≈ 2.5×10⁻³ at the CMB point (D419).
- Replacement: "Route A's band (n_s 0.9706–0.9766, r 0.0042–0.0050, ε 2.0–4.0×10⁻⁷; D434) separates it from plain Starobinsky but not from fibre inflation or α ≈ 2 attractors (D464, D475). What is specific to Twist-2 lies in its post-inflation predictions (ΔN_eff, gravitino window, ρ_β)."

**7. String-control weak point understated (D450–D453).**
- Quoted (§6): "the KK and string towers stay ≥ 2.4×10⁴ times above the temperature after inflation, but at x ≲ 1 … the volume reading is outside geometric control."
- What is wrong: With the natural normalisation, the whole inflationary phase sits at sub-string volume (𝒱 ≈ 4×10⁻⁶, D450). Rescaling the modulus to restore 𝒱 ≳ 1 at the CMB point drops the KK margin to m_KK/T ≈ 3–6, and only a narrow band a ≈ 3.8–7.9×10³ satisfies both conditions (D452–D453). The 2.4×10⁴ margin and geometric control cannot hold together.
- Replacement: "Read as a volume modulus, the field is at sub-string volume throughout inflation (D450). A rescaling restores 𝒱 ≈ 1–3 at the CMB point only by reducing the KK margin after inflation to m_KK/T ≈ 3–6 (D452–D453): control is marginal at best."

### Minor issues
- Abstract: "drives Starobinsky-class inflation". True only undeformed. Route A has α_eff ≈ 2.2 (D464).
- §1: "violates clock and equivalence-principle bounds by ~10⁶". See α-paper item 4; also "That is excluded" should be conditional on the α paper's assumptions.
- §3 "x ≈ 3 at matter freeze-out" refers to the v5 angle-driven matter genesis, which Twist-2 dropped (D395). Remove it or explain it.
- Leptogenesis window [10⁹, 2.5×10¹³] GeV: trimmed to ~7×10⁸–10¹³ GeV in the rescaled geometry (D454). Dark matter "or decaying with ξ ≲ 0.6": with M_s ~ 10¹⁴ GeV, gauged stability is mandatory (D473).
- §4: "SO / CMB-S4 σ ≈ 0.03". CMB-S4 is cancelled (D346, known before v1).
- §4 B1 column: correct, but say that B1 is now a fit-conditional consistency test, not a prediction of the undeformed model.
- Prior art: add fibre inflation (0808.0691, 1603.06789), arXiv:1110.3333 and 1310.4751 (D-term fixing / trapping), and 2107.09064/09065 (exponentially small Λ), per the Zenodo v2 list.

### Status relative to the current model
Superseded. SERAPIS (10.5281/zenodo.24250733) replaces the inflaton (τ, not T), drops the capture and the cliff, and tunes Λ = 0 by hand. The Janus Twist status record (10.5281/zenodo.24239090) already names SERAPIS as the reference model. Twist-2's surviving content is negative: the crown failure of an undeformed α = 1 plateau (Δχ² = 7.95) and the observation that a thawing single field does not lower n_s (0.9736 vs 0.9737). Both are worth keeping on the record.

Draft status notice:
> STATUS (16 Nov 2026). This model is no longer the author's working model; see SERAPIS (10.5281/zenodo.24250733). The joint-fit failure of the undeformed n_s (Δχ² = 7.95) stands. Corrections in v1.1: ΔN_eff is 0.02–0.06 (not 0.05–0.10), the gravitino window is 1.7–4.7 eV, "Λ from the cliff" holds only after a one-off cancellation that must also absorb the χ-condensate energy, the birefringence-ratio threshold is m_a ≳ 30–40 H₀, and the "better than ΛCDM in every block" statement applies to a thawing background, not to the w = −1 baseline.

### Titles (proposed)
1. "Capturing a no-scale inflaton: thermal trapping, a cliff-sized vacuum energy, and a spectral index that must be fitted"
2. "Twist-2: a pre-registered joint-fit failure of an α = 1 plateau and a one-parameter repair with a testable tensor ratio"

### Checks done
- Crown χ² against crown_d410.json: 2408.06 − 2400.11 = 7.95 (√ = 2.82σ); blocks +5.803/+4.216/−2.254; thawing −2.15 vs ΛCDM; w₀w_a −9.96. Match. Issue 1 comes from the w₀ = −0.956 of THAW_FREE.
- Route A against D419/D434 (ε 3.04×10⁻⁷, r 0.0046, α_s −7.7×10⁻⁴, B1 +2.5×10⁻³; window corrected to 2.0–4.0×10⁻⁷). 3(1−0.9736)² = 0.0021, so 2.2×. Matches.
- N*, n_s and r against D391/nstar_nosigma_d391.txt (57.2, 0.9651, 0.0036). Capture, pinning, Λ and ΔN_eff against D396, D407, D412, D413, D416, then D422, D427, D428, D430, D463, D474.
- Pre-registration claim checked against the D-note labels of D394, D411 and D417 (unlocked).
- String flags against D408, D409 and D450–D453. Prior art against D464 and the Zenodo v2 list.

---

## Cross-paper notes
- One recurring pattern: "derived", "rules out", "every computation pre-registered" and "~10⁶σ" each say more than their own source notes support. A one-line style rule for future records: state ratios, not σ beyond ~10, and mark every unlocked estimate.
- Twist-2 §1 propagates the α paper's "~10⁶" and unconditional "excluded" wording. Fix both in the same pass.
- The project's n_s reference values are inconsistent across documents: CMB-SPA 0.9693 vs 0.9684 vs 0.9682; +DESI 0.9737 vs 0.9728. Use arXiv:2507.12459 / 2512.10613 values consistently and cite which.

## Web sources used
- MICROSCOPE final results: https://arxiv.org/abs/2209.15487v1
- Ferreira et al., BAO–CMB tension and inflation (n_s values): https://arxiv.org/html/2507.12459v1
- DESI DR2 Results II abstract: https://huggingface.co/papers/2503.14738
- Search hits consulted: https://arxiv.org/pdf/2506.20707 (SPT-3G D1), https://iac.es/en/science-and-technology/publications/desi-dr2-results-ii-measurements-baryon-acoustic-oscillations-and-cosmological
