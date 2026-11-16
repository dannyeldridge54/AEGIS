# Referee report: "The Shape of the Torus Sets the Sky" (SERAPIS v3.2 draft)

## 1. Summary

The paper proposes an SL(2,Z)-invariant plateau for the torus modulus τ, with its vacuum at τ=i (built from |j−1728|) or at ρ. One extra term, ε I₁, gives the vacuum at i a mass and tilts the spectrum. This produces an untilted face ("Kairos", n_s≈0.96) and a tilted face ("Chronos", n_s≈0.970–0.975, r≈5×10⁻⁴). A closed-form consistency relation predicts α_s from (n_s, r) to about 2%, and the paper adds a cap and a narrow (n_s, r) strip. A loop-motivated branch, SERAPIS-E, builds the plateau and the tilt from E(τ,2) using a BHK one-loop Kähler term. A long consistency chain covers reheating, supersymmetry breaking, protons, leptogenesis and Affleck–Dine, and the predictions are frozen with hashes. The analytic core (Secs. II–V) is sound. I checked the slow-roll algebra, the consistency relation, the general (p, κ) relation, β_s at x=0, the N_* integral, the values c=1.1865 and E₄(i), and the wino/gluino mass arithmetic. The problems are mainly that later corrections have not been carried through the paper, and that some framing claims more than the body supports.

## 2. Major issues

**M1. The reheating correction is not carried into the headline numbers.** Line 171 says: "With this channel T_R≈(0.8–3)×10⁶ GeV … the stiff-phase rows describe the actual history" and "the corrected τ=i prediction therefore meets the frozen band only for ε≈(1.40–1.45)×10⁻⁴ … n_s≈0.9745–0.9750". Several places still use the old T_R=10³–10⁵ GeV bracket (N_*=46–49) and the full window ε=1.3–1.6:
- the abstract (line 10), which quotes T_R∼10⁶ GeV and the old band in the same paragraph;
- Sec. IV (lines 75–77);
- line 173 ("which is the range used");
- the Fig. 2 caption;
- line 196 ("restoring T_R∼10⁵ GeV", "ΔM/M≈0.08–0.5"), which line 201 contradicts ("0.6–11, not the 0.08–0.5 estimated earlier");
- the Affleck–Dine m_ν1 range at line 207 (computed for T_R=10³–10⁵).

*Fix:* in the abstract, after the Chronos band, add: "with the corrected reheating (T_R∼10⁶ GeV) the τ=i model meets this frozen band only for ε≈(1.40–1.45)×10⁻⁴, at n_s≈0.975, r≈4.9×10⁻⁴." Mark line 196 and the Fig. 2 caption as superseded by D727/D738.

**M2. The leptogenesis heading contradicts the abstract.** Line 201 is headed "Leptogenesis from inflaton decay fails." The abstract (line 10) and line 23 say it works at i. The positive result also rests on a chain of assumptions: a maximal phase, no washout, a leading-order radiative estimate (D744–745), and a postulated CP-odd racetrack axion on two cycle classes (D854). *Fix:* rename the heading to "Leptogenesis from inflaton decay at τ=i". In the abstract, write "leptogenesis from inflaton decay at i (a leading-order estimate, conditional on spontaneous CP violation on two cycle classes)".

**M3. The "strip" and "cap" are stated for "any ε, both vacua", but the paper's own post-hoc ρ history lies off the strip.** Line 133 says "the allowed r at fixed n_s … e.g. r=(4.4–5.3)×10⁻⁴ at n_s=0.970". The self-diluted SERAPIS-E band (line 261, Table I) is n_s=0.966–0.970 with r=(5.2–5.7)×10⁻⁴, which sits at or above the strip's upper edge. Locks D679/D681 say such a point "excludes the family". The cap and strip assume N_*=46–49, and they were computed for SERAPIS and SERAPIS-ρ (κ=½), not for SERAPIS-E (κ=1). The 2% relation of Eq. (consistency2) uses the j-offset c, so it does not apply to SERAPIS-E either (line 237 gives 3.5–5% there). *Fix:* write "within the reheating bracket N_*=46–49, for the j/I_ρ plateaus" in the abstract, line 133 and Table I. State explicitly that the self-diluted history leaves the strip.

**M4. SERAPIS-E is called "derived" and "natural" more strongly than the body allows.** Line 240 says "Sec. VIII gives a derived alternative". In fact:
- C=(1.0–1.3)×10⁻⁶ corresponds to choosing Im S·Im ρ≈750–975 after the data (line 237: "built after the data");
- the plateau is placed by hand (line 259);
- the "unique flux-free tadpole-consistent placement" with N−N₀=4 (line 232) is not the relevant one once the uplift anti-D3 is present, where (N,N₀)=(5,2) gives N−N₀=3 (line 237).

*Fix (line 240):* "Sec. VIII gives an alternative whose tilt has a computed loop form; its size is set by the moduli values Im S·Im ρ, chosen to fit." In line 232, drop "unique" or add "absent the uplift anti-D3".

**M5. The "4.5 times below the j-based attractors" claim is misleading.** The abstract (line 10) and line 237 say "puts r about 4.5 times below those attractors". The paper's own j-based plateau with p=2 (Kairos) already gives r=3.3–3.7×10⁻⁴, the same as untilted SERAPIS-E (3.6×10⁻⁴). The suppression comes from the y⁻² approach (α_eff=1/12, line 105), which SERAPIS shares. *Fix:* "…about 4.5 times below the p=1 j-based attractors of Ref. [2408.05203] at the same Kähler metric (the same as our p=2 j-plateau)."

**M6. The Σm_ν row is presented as a frozen prediction, but the body makes it conditional and inconsistent.**
- Table I lists "≃0.059 eV (if NO)" in an unmarked (frozen) row, disfavoured above 0.07 eV.
- Line 209 says the floor applies only if Affleck–Dine is the source, "with the inflaton-decay routes above this is no longer required", and that it "tests that class rather than SERAPIS specifically".
- Line 272 says inverted ordering "would falsify that input rather than the model", yet IO gives ≈0.10 eV and would trigger the >0.07 eV falsifier.
- Two different DESI bounds are quoted: <0.0592 eV (line 209, "alive by 0.0005") and <0.064 eV (line 307, "passes").

*Fix:* mark the row "conditional on Affleck–Dine baryogenesis; not specific to the model", and quote one bound consistently in both places.

**M7. Two superpartner rows contradict each other.** Line 287 has a frozen row "none below ∼3×10⁸ GeV" from the constant-W₀ embedding, which line 274 retracts ("The no-scale claim is retracted"). Line 289 predicts a TeV wino in the adopted completion. The thresholds also differ: 3×10⁸ GeV in the table versus 10⁸ GeV at line 274. *Fix:* move the D605 row into a footnote labelled "retracted embedding; not applicable to the adopted covariant completion".

**M8. The pre-registration claim is too broad.** Line 26 says: "All predictions are frozen … and every computation was pre-registered with a hash before it was run." This conflicts with:
- line 316 ("group-theory checks excepted");
- line 325 (22 non-registered notes, and an "unregistered numerical diagnostic" in D608);
- the post-hoc rows in Table I.

*Fix:* "The inflationary predictions in Table I (unmarked rows) are frozen; numerical computations, except group-theory checks and one disclosed diagnostic (D608), were pre-registered."

**M9. The paper does not say which model is primary, and the Z₃ problem is not stated for SERAPIS-ρ.** The title, abstract and Secs. III–V lead with τ=i. Line 218 calls ρ "the better-motivated vacuum". Line 263 demotes τ=i to "a conditional variant", and line 261 calls the ρ history "its most fragile part". The residual-Z₃ argument (the inflaton carries the charge, its decay products are long-lived, and there is no baryogenesis in the frozen band) applies to any vacuum at ρ. The paper, however, discusses it only for SERAPIS-E. The SERAPIS-ρ row in Table I (n_s 0.969–0.972) carries no such caveat, and Sec. VII still says "the rest of the chain carries over". *Fix:* state in Sec. VII whether the Z₃ issue applies to SERAPIS-ρ, add the condition to its table row, and give one sentence in the introduction on the hierarchy of branches.

**M10. The exact ρ spectra do not match the frozen band as stated.** Line 218 says: "the same band to rounding except that the largest r lies 1.2% above the frozen upper edge". The exact α_s=−(8.7–9.9)×10⁻⁴ also exceeds the frozen −(8.5–9.5)×10⁻⁴ by about 4%. *Fix:* "…except that the largest r lies 1.2% and the most negative α_s 4% beyond the frozen edges."

## 3. Minor issues

1. **D-labels.** There are more than 150 "D###" labels and they are opaque. Table II covers only notes up to D639, while the text cites up to D855. The note file name `D72_D75_weak_spots.md` (line 325) does not look like a container for D528–D855. Keep labels only for locks and key computations, and give a complete index.
2. **Symbol overloading.** ε is both the tilt and the CP asymmetry (lines 201, 261). κ is used four ways (lines 60, 171/201, 141, 259). ρ is the fixed point, the Kähler modulus Im ρ (line 223) and an energy density ρ_x. Rename the secondary uses.
3. **Fig. 1 caption.** "the perturbative bound Im τ≈25" conflicts with line 43, where the bound is ≈29 and 25 is the imposed cut. Fix to "the imposed cut Im τ=25".
4. **Line 207 typo.** "(LH_u)²/M_P, With" should read "…/M_P. With".
5. **Line 105.** "(Sec. V, last paragraph)" is a reference to the section it appears in. Write "(see 'Removing the bias' below)".
6. **Line 133.** "home-safe family" is undefined jargon. Use "the SERAPIS family with y_*≤25".
7. **Line 78.** ρ_x′ is undefined.
8. **Pass fractions.** Lines 201 and 203 give 34–86% and 68–71% for apparently the same Casas–Ibarra grid. Say how the two grids differ.
9. **T_R range.** It is (0.8–3)×10⁶ GeV at line 171 but (1–3)×10⁶ GeV at line 201. Use one range.
10. **Table I, upper falsifier for r.** Two different values appear: r>1.1×10⁻³ (line 283) and r>8.3×10⁻⁴ (line 294). Reconcile them.
11. **Table I, covariant falsifier.** "no wino <1.85 TeV" ignores the cored-halo extension to 2.9 TeV (line 190).
12. **Line 218.** Constant-W₀ numbers (m_3/2≳3.6×10¹⁰ GeV) and covariant numbers are mixed in one paragraph without labels.
13. **Abstract wording on testing α_s.** "testing it needs σ(α_s)≈2×10⁻⁴" only separates the Janus value from the attractor value. Testing the 2% relation itself needs σ of order 10⁻⁵. Reword.
14. **Abstract length.** At about 400 words with nested clauses, it is hard to read. Move the Affleck–Dine and wino details to the body.
15. **Repository link.** Line 272 cites "the public repository" without a URL or commit hash; only a Zenodo DOI is given. Add both. (All citation keys resolve; 12 bib entries are unused, which is harmless.)

## 4. Verdict

**Not yet.** The core inflationary analysis is sound and honestly caveated. However, the abstract, Sec. IV and Table I still state the pre-correction τ=i band, the Σm_ν and superpartner rows, and the family-wide strip in ways that the paper's own later sections contradict. These are mostly wording and table fixes (M1–M10), so the paper should be ready after one careful consistency pass.

---
## Response (D858, 16 Nov 2026)
Applied: M1 (abstract, Sec. IV results line, e-fold paragraph note the corrected-reheating ε window 1.40–1.45e-4), M2 (heading "Leptogenesis from inflaton decay at τ = i"; abstract states the result is a leading-order estimate conditional on spontaneous CP violation on two cycle classes), M3 (strip and cap qualified to the j / I_ρ plateaus with N* = 46–49; the self-diluted ρ history noted as outside), M4 ("derived alternative" → computed one-loop form with fitted moduli; "unique" placement qualified), M5 (4.5× compared with the p = 1 attractors of 2408.05203, as for our p = 2 plateau), M6 (Σm_ν row footnoted as Affleck–Dine-only class test; both DESI bounds quoted), M7 (D605 superpartner row footnoted as retracted embedding), M8 (pre-registration claim narrowed), M9 (residual Z₃ stated for SERAPIS-ρ), M10 (α_s 4% beyond frozen edge stated). Minor: 3 (Fig. 1 caption), 4 (typo), 6 (home-safe jargon).
Deferred (judgement or larger edits; listed for Danny): minor 1 (D-label index), 2 (symbol overloading), 5, 7, 8 (pass-fraction grids), 9 (T_R range), 10 (two r falsifiers), 11 (cored-halo extension), 12, 13 (α_s testing wording), 14 (abstract length), 15 (repository URL/commit hash). Also: line 196 ("restoring T_R ∼ 10⁵ GeV", ΔM/M 0.08–0.5) is older text superseded later in the same section; left as historical with the later correction in place.
Batch 1 of deferred minors applied (D871): #5 self-reference, #7 ρ_x′ defined, #9 one T_R range (0.8–3)×10⁶ GeV, #10 r falsifiers reconciled (footnote h), #11 cored-halo 2.9 TeV added, #13 α_s testing wording (abstract and body).
Batch 2 (D872): #15 repository URL and branch added; #2 CP asymmetry renamed ε_CP (κ overloading left: each use is local and defined); #12 constant-W₀ label added in the ρ paragraph; #14 abstract shortened (wino clause moved to body reference); #1 already covered by the existing D-label paragraph and Table II caption (later notes in MANIFEST.md).
