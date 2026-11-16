# Referee report: SERAPIS v3.1 (round 7, independent)

Manuscript: `papers/v3/serapis_v3.tex` (16 Nov 2026, v3.1), refs.bib, serapis_v3.pdf.
Sources checked: `theory/pending_docs/D72_D75_weak_spots.md` (D777–D805, D803a), `field_tests/results/*` (D781, D783, D784, D788, D790–D793, D795, D801), `prediction_sheet.md`, `CHANGELOG_v3.1.md`, and the arXiv records of 2504.19364, 2603.08315, 2507.15934, 2212.03876.

**Recommendation: major revision.** The core inflationary results are internally consistent and match their sources. The new ρ-side text, however, has a wrong abstract sentence, stale statements, a mathematical misstatement about the modular subgroup, an overgeneralised theorem citation, and a forecast table that mixes post-hoc rows into "Frozen predictions" while leaving out the frozen SERAPIS-E band.

---

## Major issues

**1. The abstract misstates how baryogenesis works at ρ (it contradicts D788 and the paper's own Limitations).**
Location: abstract, sentence beginning "We follow the history after inflation".
Quoted: "at $\rho$ a residual $\mathbb{Z}_3$ symmetry that makes the inflaton's decay products long-lived, so that the frozen band there requires their decay through string-scale operators and baryogenesis comes from that late decay".
- D788 shows that the late dim-6 decays give ε ≤ 2×10⁻⁸ against the ≥ 2×10⁻⁵ required (results/late_eps_d788.txt). So baryogenesis does **not** come from the late decay.
- In the self-diluted history (D792–D793) the asymmetry comes from the inflaton acting as an Affleck–Dine condensate. The late decays only carry and dilute that asymmetry, and the history lies **outside** the frozen band.
- The Limitations item says exactly this: "choose between the frozen band without a baryogenesis mechanism and this slightly shifted band with one". The abstract says the opposite: frozen band plus baryogenesis.

Fix: "...and at $\rho$ a residual $\mathbb{Z}_3$ that makes the inflaton's decay products long-lived: the frozen band then requires their decay through string-scale operators but leaves no baryogenesis mechanism, while a post-hoc history in which the inflaton acts as an Affleck–Dine condensate gives the observed asymmetry at $n_s=0.967$–$0.970$, $r=(5.1$–$5.6)\times10^{-4}$, just outside the frozen band."

**2. Stale ρ-leptogenesis claims in the Introduction and in the SERAPIS-E section.**
- Intro, point (iv): "leptogenesis from inflaton decay works on both branches, provided the heavy-neutrino couplings carry CP phases". At ρ this route is closed: any early asymmetry is diluted by the late Z₃-charged decays (D782; Limitations). Fix: "...works at $\tau=i$; at $\rho$ the residual $\mathbb{Z}_3$ closes it (Sec. VIII)".
- SERAPIS-E section: "The heavy neutrinos produced by inflaton decay ... can generate the baryon asymmetry (but see Sec.~\ref{sec:limits}: the residual $\mathbb{Z}_3$ at $\rho$ closes this route ...). A full computation of the CP asymmetry ... gives the observed yield for $29$--$70\%$ ... (D775 ...)." The paragraph says the route is closed and then spends about 90 words computing it. Fix: delete the D775/D776 sentence and replace the pair of sentences with: "Leptogenesis from these decays (D775–D776) is superseded: the residual $\mathbb{Z}_3$ makes the decay products long-lived and dilutes any early asymmetry (Sec.~\ref{sec:limits})."

**3. The forecast table mixes frozen and post-hoc rows, omits the frozen SERAPIS-E band, and uses an unsourced falsifier.**
Location: Table `tab:forward` and the paragraph before it ("The following were frozen ... The table restates them.").
- (a) The caption reads "Frozen predictions and the conditions under which each is disfavoured." Rows b, c and d are explicitly not frozen ("Not locked"). This breaks the frozen/post-hoc separation the paper relies on. Fix: either split the table into "Frozen (locks D605, D615, D633, D667, D675–D681, D693)" and "Post hoc / estimates (not frozen; scored only on future data)", or retitle the caption "Frozen predictions (unmarked) and post-hoc or estimated entries (footnotes b–d)".
- (b) The frozen SERAPIS-E band (lock D693: $n_s=0.970$–$0.975$, $r=(4.6$–$5.1)\times10^{-4}$, $\alpha_s=-(9.4$–$10.6)\times10^{-4}$; prediction_sheet.md gives r 4.55–5.12e-4) is **not in the table**. The column "SERAPIS ($\tau=i$; $\rho$)" lists the L-based SERAPIS-ρ variant (0.969–0.972), not SERAPIS-E. As a result, the post-hoc row "SERAPIS-$E$/$\rho$ self-diluted" appears without the frozen band it is meant to be compared against. Fix: add a frozen row "SERAPIS-$E$ (lock D693)" with those three numbers, its falsifier, and its conditions ($T_2\gtrsim10^5$ GeV, full $SL(2,\mathbb Z)$).
- (c) Row d's falsifier "$n_s>0.973$ or $r<4.9\times10^{-4}$ at $3\sigma$" has no source. It does not appear in D792, D793, PREREG_D792/D793, prediction_sheet.md or D805. It also reads ambiguously: does it mean a measured central value above 0.973 at 3σ significance? Fix: use the wording the other rows use ("band excluded at $3\sigma$"), or derive the thresholds in a D-note and cite it.
- (d) Footnotes c and d say "Not locked", but D784, D792 and D793 were each run under a locked PREREG. The intended meaning is "not a frozen forecast". Fix: "Not a frozen forecast (computation pre-registered, PREREG_D784)" and likewise for D792/D793. The same applies to "(post hoc, not locked; D784 ...)" in the SERAPIS-E text.
- (e) The label "SERAPIS-$E$/$\rho$" is easily read as "SERAPIS-E or SERAPIS-ρ". Fix: "SERAPIS-$E$, self-diluted history (post hoc)".

**4. SERAPIS-E opening paragraph: theorem hypotheses misstated and overgeneralised.**
Quoted: "The hexagonal lattice is the unique minimiser of the Epstein zeta function $E(\tau,s)$ for every $s>0$ and of the lattice theta function~\cite{Rankin1953,Montgomery1988}, so any potential built from one-loop lattice sums has its vacuum at $\rho$ ... This holds for sums with positive weights, as in the supersymmetric thresholds used here."
- (a) The paragraph is self-contradictory: it makes an unconditional claim ("any potential built from one-loop lattice sums") and then qualifies it in the next sentence. Put the qualification in the claim itself.
- (b) "Positive weights" is not the right hypothesis. Montgomery's theorem (theta function, every α > 0, at fixed covolume) implies, through Bernstein's theorem, that the hexagonal lattice minimises $\sum' f(|p|^2)$ for every **completely monotone** f, meaning positive mixtures of Gaussians. That class contains $E(\tau,s)$ for all s > 0 (by Mellin transform) and, as the Kronecker limit, $-\ln(y|\eta|^4)$. A lattice sum with positive coefficients but a non-completely-monotone profile is not covered. Fix: "for any sum $\sum' f(|m+n\tau|^2/\mathrm{Im}\,\tau)$ with $f$ completely monotone (a positive mixture of Gaussians), which includes $E(\tau,s)$ and, in the Kronecker limit, $-\ln(\mathrm{Im}\,\tau|\eta|^4)$".
- (c) Attribution: Rankin (1953) did not prove "every s > 0". To my knowledge Rankin covered s ≥ 3/2 in the $|p|^{-2s}$ convention. The extension to all s > 0 is due to Cassels (1959), Ennola (1964) and Diananda (1964), or follows from Montgomery (1988). For E(τ,2) Rankin is sufficient. Fix: cite Cassels/Ennola/Diananda as well, or say "for $s\ge3/2$ [Rankin] and every $s>0$ [Cassels, Ennola, Diananda; Montgomery]". Blanc–Lewin (1504.01153), which D801 used, is a convenient review to cite.
- (d) **The BHK sum used here is itself sign-indefinite.** Each half-period sum $E_2(\varphi_k,U)=\sum' e^{2\pi i\langle p,\varphi_k\rangle}(\ldots)$ carries the characters $(-1)^{m}$, $(-1)^{n}$ or $(-1)^{m+n}$. Each one is invariant only under an index-3 subgroup of Γ₀(2) type, the same structure as a Scherk–Schwarz shift. Only the S₃-symmetric total collapses: $\sum_{k=1}^3 E_2(\varphi_k,U)=4\cdot\tfrac{1}{16}E(U,2)-E(U,2)=-\tfrac34E(U,2)$, as stated in the next paragraph. So what restores full $SL(2,\mathbb Z)$ is the **equal** number of stuck D3s at the three half-periods (S₃ = SL(2,Z)/Γ(2) permutes them), not "positive weights" or supersymmetry. Fix: replace "This holds for sums with positive weights, as in the supersymmetric thresholds used here" with "In the orientifold of Sec. ... this requires equal brane numbers at the three half-periods, which $SL(2,\mathbb Z)/\Gamma(2)\simeq S_3$ permutes; then the position sum collapses to $-\tfrac34E(U,2)$." Add to the Limitations item (issue 6) that an unequal distribution, or the D694 drift of the stacks, reduces the group in the same way as Scherk–Schwarz.
- (e) Quoted: "(of $\Gamma^0(2)$ type, the stabiliser group of $1+i$)". This is mathematically wrong. Γ⁰(2) is not the stabiliser of 1+i. The stabiliser is $\langle TST^{-1}\rangle$, cyclic of order 4 in SL(2,Z), and Γ⁰(2) **contains** it. Fix: "(of $\Gamma^0(2)$ type, i.e. $b$ even, which contains the stabiliser $TST^{-1}$ of $1+i$)". Note: the source's eq. (2.31) names the group Γ₁(2) but imposes "b = 0 mod 2" with a typo "mod 1". The b-even condition is the Γ⁰(2) (=Γ¹(2)) family, so D803a's identification is right. A one-clause footnote recording the source's label would spare readers the same confusion.
- (f) The 2504.19364 minimum is a **metastable AdS** point (Λ ≈ −0.0079 M_s⁴, with unbounded decompactification directions) in a **heterotic free-fermionic** model, with T = U = 1+i. The paper uses it in an argument about a IIB orientifold modulus. State in one clause that it is a heterotic AdS example, offered as an existence proof of a reduced-group minimum at an image of i, and not as part of the SERAPIS setup.
- (g) Notation: this paragraph writes the threshold as $-\ln(\mathrm{Im}\,\tau|\eta|^4)$, while Secs. VI, VIII and the chain use $-\ln(2y|\eta|^4)$. Pick one.

**5. The ρ-history Limitations bullet is stale, overclaims in places, and is far too long.**
Location: Sec. `sec:limits`, "Other caveats", the bullet beginning "At $\rho$ a lepton sector built only from the weight-two doublet ..." (about 650 words in a single bullet).
- (a) Stale: "The wino estimate built on the earlier $T_R$ is being redone." D784 has redone it, and the result is already quoted in the SERAPIS-E section, the abstract and table row c. Delete the sentence.
- (b) Stale: "...which the leptogenesis estimate of Sec.~\ref{sec:serapisE} must still take into account (D779)". Later in the same bullet, that leptogenesis is closed by dilution. Delete.
- (c) Wrong qualifier: "if inflation ends slightly off the CP-symmetric line". The isocurvature bound forces $|\mathrm{Re}\,\tau-\tfrac12|\ge0.15$ (D791), which is 30% of the distance to the next CP-conserving line. "Slightly" is wrong. Also say that this is an initial-condition choice: the axion is light during inflation and the offset persists. D790 itself calls the choice "not natural".
- (d) Overclaim: "This complete $\rho$ history, with spontaneous CP violation and no further ingredient". The history still needs (i) the weight choice $q_{H_u}\neq0$ (R-Z₃, D787), (ii) a dim-6 decay scale Λ ≈ (0.5–2)×10¹⁷ GeV, which is 2–30 times **above** the estimated M_s (D792; the paper does not say this), and (iii) the initial offset ≥ 0.15. Also, $|\eta|\approx2|\Delta x|$ is an extrapolation from two valid read-outs of opposite sign (x₀ = 0.45 → −0.10, x₀ = 0.40 → +0.20; D790), and D792 scans η ∈ {0.3, 0.6, 1} by assumption. Fix: "with no new fields, but with a chosen initial offset and a decay scale $\Lambda\approx2$–$30\,M_s$ (estimates)".
- (e) Small mismatches with the sources: "CP violation in the inflaton's own decays is negligible ($\lesssim10^{-13}$)". D790 gives up to 3.0×10⁻¹³, so write "$\lesssim3\times10^{-13}$". "dimension-four and -five proton decay are forbidden (D787)": D787 says this holds by Z₃ **and** matter parity together, so add "with the matter parity of Sec. VI".
- (f) Misplaced: "The frozen $\sum m_\nu$ assumes normal ordering." This has nothing to do with ρ reheating. Move it to its own bullet or delete it (Sec. VII already says it).
- (g) Too long: the P5 mediator detour (two sentences) leads only to "it is a postulate", and D792 retired P5. Suggested replacement for everything after "...(D741, D777, D778)." and the D779 sentence:

  > More seriously, the inflaton carries the $\mathbb Z_3$ charge, so all its decays produce charged heavy neutrinos with no renormalisable decay (D780). The frozen SERAPIS-$E$ band survives only if they decay through operators suppressed by $\Lambda\lesssim(0.4$–$1)\times10^{16}$~GeV, near the string scale, giving $T_2\gtrsim10^5$–$10^6$~GeV; this needs $q_{H_u}\neq0$, which makes the $\mathbb Z_3$ act as baryon triality (D781–D783, D787). Such late decays cannot themselves make the asymmetry ($\varepsilon\lesssim2\times10^{-8}$, D788), so the frozen band has no baryogenesis mechanism. A post-hoc alternative exists: the inflaton acts as an Affleck–Dine condensate if inflation starts at $|\mathrm{Re}\,\tau-\tfrac12|\ge0.15$ (required by isocurvature, D791), and decays at $\Lambda\approx(0.5$–$2)\times10^{17}$~GeV dilute the result to the observed $Y_B$ at $T_2\approx140$–$1100$~GeV. This moves the predictions to $n_s=0.967$–$0.970$, $r=(5.1$–$5.6)\times10^{-4}$ (D792–D793), just outside the frozen band. The $\tau=i$ branch is unaffected (D785).

  That is roughly 170 words in place of about 650, with no loss of content a reader needs.

**6. Generalised-CP statements are now incomplete because of the self-diluted ρ history.**
- Abstract: "with generalised CP imposed it fails and $\delta_{CP}\in\{0,\pi\}$".
- Sec. VII, CP paragraph: "If generalised CP is imposed, every coupling is real there, the leptogenesis asymmetry vanishes on both branches" and "Within this setup the CP phases must therefore be explicit couplings of the heavy-neutrino sector".
- Limitations: "Leptogenesis on both branches assumes CP phases in the heavy-neutrino couplings".

In D792 the ρ asymmetry comes from **spontaneous** CP violation (the initial offset), and D792 states "P1 is not needed at ρ". That history is compatible with imposed gCP: the couplings are real at the vacuum, so δ_CP ∈ {0, π}, yet baryogenesis works. The statements above are true for *leptogenesis* but read as "gCP ⇒ no baryogenesis on either branch". Fix: in the abstract write "inflaton-decay leptogenesis then fails"; in Sec. VII and the Limitations add "(the post-hoc self-diluted $\rho$ history, Sec. VIII, needs no such phases)".

**7. Covariant-completion wino window conflicts with a reference the paper itself cites.**
- Chain section: "a wino LSP at $0.66$--$2.9$~TeV (all of the dark matter at the upper end, where gamma-ray line searches already constrain wino dark matter)".
- Table row b: "wino $0.66$--$2.9$~TeV", falsifier "no wino $<2.9$".
- Safdi & Xu (2507.15934), cited by the paper for SERAPIS-E, state: "In the subfraction scenario we are able to robustly rule out all wino masses between 1.85 TeV and the thermal mass", and they exclude the thermal wino even for cores up to about 6.7 kpc. So 1.85–2.9 TeV is not "constrained", it is excluded (D713 and prediction_sheet.md already say so).
- The lower end, 0.66 TeV, is the superseded 2201.02472 bound. I verified that 2603.08315 gives 670 GeV for winos ("charginos are excluded for masses up to 670 GeV (770 GeV expected)").

Fix: "wino $0.67$--$1.85$~TeV (Einasto; up to $2.9$~TeV only for cored profiles), a sub-component of the dark matter". Update row b and the $m_{3/2}$ window to match.

---

## Minor issues

1. **Recent CP sentence** (Sec. VII, end of "Where the CP phase comes from").
   - "it depends on $\tau$ only through $|j-1728|\propto|z|^2$" holds only at leading order. Write "$\simeq c|z|^2(1+O(|z|^2))$".
   - "unlike at $\rho$" means SERAPIS-E at ρ, not the L-based SERAPIS-ρ of Sec. VIII. Write "unlike SERAPIS-$E$ at $\rho$".
   - The physics matches D794/D795: the isotropy came from D795, which corrected D794 step 4, and the carrier argument is sound.
   - Suggested tightening: "At $i$ no Affleck–Dine twin exists: the potential is isotropic about $i$ to leading order (D795), so an off-axis orbit carries a charge, but the residual symmetry is only $\mathbb Z_2$ and the Majorana parity eigenstates it decays into cannot store it (D794)."
2. **Notation for ρ.** The Intro and Sec. VIII define $\rho=e^{2\pi i/3}$ (Re = −½), and the Limitations item uses its stabiliser $ST$, which is correct for that point. But the SERAPIS-E inflaton runs along Re τ = +½, ending at the T-image $e^{i\pi/3}$, whose stabiliser is $TS$. Add one clause: "(equivalently its image $e^{i\pi/3}$ on the line $\mathrm{Re}\,\tau=\tfrac12$)".
3. **Limitations item "SERAPIS-E needs the full SL(2,Z)".**
   - Correct as stated. Every index-3 subgroup of PSL(2,Z) lacks order-3 elements: in the action on 3 cosets the order-3 generator must act as a 3-cycle.
   - Add the brane-distribution point from issue 4(d).
   - Clarify "keeps its residual $\mathbb Z_2$ at the image $1+i$": under Γ⁰(2), i and 1+i are no longer equivalent, and only 1+i is elliptic, so the branch's vacuum must sit at 1+i specifically. Under Γ₀(2) the elliptic point is (1+i)/2; under the theta group it is i itself.
4. **"Derived branch".** The section title and the abstract call SERAPIS-E "derived". Its plateau placement is a postulate (P3; D768, D797, D799) and the configuration was chosen after the data (lock D693, "post-hoc" in prediction_sheet.md). Use "a loop-motivated branch" or "a branch with a computed tilt".
5. **Sec. VIII vs Sec. IX on the origin of ρ's tilt.** Sec. VIII says ρ is better motivated because "Its tilt function is the universal $N=2$ threshold". SERAPIS-E says "this tilt, unlike those of the $\tau=i$ and $\rho$ variants, has a loop origin" (D756: in IIB the DKL tilt has no loop origin). Say "heterotic threshold" in Sec. VIII and "in this IIB orientifold" in Sec. IX.
6. **Abstract: "it gives the same $(n_s,r,\alpha_s)$ band".** SERAPIS-E gives r 4.6–5.1 vs Chronos 4.8–5.7, and α_s −(9.4–10.6) vs −(8.8–10.2), all ×10⁻⁴. Write "an overlapping band". Also add "at the same Kähler metric" to "r about 4.5 times below the j-based attractors"; otherwise a reader will compare it with Chronos, whose r is similar.
7. **Table row c falsifier: "no wino $<1.85$~TeV (HL-LHC + lines)".** HL-LHC disappearing tracks reach about 1 TeV (D736, D784), and line searches constrain the upper end. Nothing named covers 1–1.85 TeV. State the reach honestly.
8. **Strip width.** The text says "spans at most $21\%$" (D678) and the table says "width $\le22\%$". Use 21% (the prediction sheet also says 21%).
9. **$\sum m_\nu$.** Sec. VII says 0.0588 eV and Sec. X says 0.0587 eV ("the normal-ordering floor"). D786 gives 0.0586 at m₁ = 0 and 0.0587 at m₁ = 10⁻⁴ eV. Use one value. D786 also gives a τ = i range of 0.059–0.064 eV now that m₁ is free; worth one clause next to the frozen 0.059.
10. **Sec. IX, second paragraph**, about 900 words in one paragraph. It includes a parenthetical inside a parenthetical before the displayed equation: "(D696; 375–488 ...) (in the $\mathcal N=1$ orientifold ... D756)". Split it into four paragraphs (set-up and C; reheating at ρ; numbers; caveats and plateau origin), and move both parentheticals to a footnote.
11. **Reproducibility claims.** The Intro says "every computation was pre-registered", yet D804's group arithmetic was "checked in code, no lock", and it is cited. Table `tab:repro` stops at D639, while the text cites locked computations up to D801, so the table no longer "lists them". Extend the table, or say it is truncated and point to MANIFEST.md.
12. **"The cosmological constant is tuned separately, as in the no-go of Ref. [2212.03876]".** The no-go does not tune anything. Write "is tuned separately; a de Sitter vacuum at the fixed points is excluded in the minimal heterotic setting [2212.03876]". The underlying claim is correct (Corollary 2.1 there).
13. **Sec. VIII text** still says "gamma-ray line searches already constrain" (see major issue 7). Sec. VI's "superseding 660 GeV" is fine.

---

## Checks done

**Modular-group mathematics**
- $TST^{-1}=\begin{pmatrix}1&-2\\1&-1\end{pmatrix}$ is in Γ⁰(2) (b even), fixes 1+i ($\tau^2-2\tau+2=0$), and has order 2 in PSL. It is not in Γ₀(2) (c odd) or in the theta group. Correct as in D804/D803a.
- Γ₁(2) = Γ₀(2) as matrix groups (c even forces a, d odd), with elliptic point of order 2 at (1+i)/2.
- Index 3, ε₂ = 1, ε₃ = 0, two cusps, genus 0 (Riemann–Hurwitz check: 1 + 3/12 − 1/4 − 0 − 1 = 0). Correct.
- No index-3 subgroup of PSL(2,Z) contains an order-3 element. So "has no order-three fixed point" is correct for any index-3 reduction, including the normal Γ³.
- Stabiliser of $e^{2\pi i/3}$ is ST: $\tau\to-1/(\tau+1)$, fixed by $\tau^2+\tau+1=0$. Correct. A Z₃-invariant quadratic form is isotropic. Correct.
- Γ⁰(2)/Γ(2) ≅ Z₂ inside S₃, generated by a transposition; the S₃ doublet then splits as 1 ⊕ 1′. Correct (D804).
- E(τ,2) values reproduced analytically: $E(i,2)=4\zeta(2)\beta(2)=6.027$ and $E(\rho,2)=\tfrac34\cdot6\zeta(2)L(2,\chi_{-3})=5.783$, difference 0.244 (D801: 0.2435). Laplacian check $y^2(f_{xx}+f_{yy})=2E(i)$: −3.427 + 15.480 = 12.05 = 2 × 6.027. Correct.
- For Δ = −ln(y|η|⁴): f_xx + f_yy = 1.000 at i, as harmonicity of ln|η| requires. Correct. Both are saddles, descending along the arc; the arc's tangent at i is the x direction. Correct.
- Character-sum identity $\sum_{k=1}^3E_2(\varphi_k,U)=-\tfrac34E(U,2)$ checked from $\sum_{\varphi}\chi_\varphi(p)=4\cdot[p\in2\Lambda]$. This is what motivates major issue 4(d).

**Numbers in the new text against their sources (all match unless listed in the issues above)**
- D781 (late_reheat_d781.txt): T₂ = 300 GeV gives n_s 0.9669–0.9698 and r 5.20–5.55e-4. The frozen band survives for T₂ ≳ 10⁵–10⁶ GeV. Matches.
- D783 (lambda_window_d783.txt): Λ_max = 3.6e15–1.05e16, M_s = 5.6e15–2.6e16. Paper: (0.4–1)e16 and (0.6–3)e16. Matches.
- D788: ε_max(dim-6) = 3.6e-10–1.7e-8 vs required 1.7e-5–1.2e-3. Paper: "at most 10⁻⁸ ... 10⁻⁵–10⁻³". Matches.
- D790: η ≈ 2|Δx| and required η = 4.3e-6. Matches (but see 5(d)). The inflaton-decay ε bound is 3e-13 (see 5(e)).
- D791 (ad_isocurv_d791.txt): |Δx| ≥ 0.151 and over-production 2.7e4. Matches.
- D792 (self_dilution_d792.txt): T₂ = 142–1097 GeV and Λ = 5.3e16–1.82e17. Matches.
- D793 (selfdil_exact_d793.txt): n_s 0.9667–0.9703 and r 5.127–5.588e-4. Table and text: 0.967–0.970 and 5.1–5.6. Matches. Wino side check T_f = 92.5 GeV < T₂. Matches.
- D784 (wino_late_d784.txt): 0.67–1.85 TeV, f = 0.053–0.407. Paper: 5–41%. Matches.
- D795 (hessian_i_d795.txt): V_xx/V_yy = 0.99999987. Matches.
- D785: τ = i unaffected. Matches.
- D787: q_Hu ≠ 0 gives baryon triality. Matches, apart from the matter-parity omission in 5(e).

**Other cross-checks**
- Frozen τ = i and ρ numbers are consistent across abstract, Secs. IV/V/VIII, table and prediction_sheet.md (n_s, r, α_s with footnote a, β_s, cap).
- D805 data check: no change to the frozen bands is needed. Optional: the post-hoc self-diluted band is 1.5–2.7σ below CMB-SPA+DESI, which would be a useful sentence beside the table.

**References** (four web searches, plus fetches of the arXiv pages)
- 2504.19364 (Antoniadis, Diaz Avalos, Faraggi): Scherk–Schwarz Z₂ deformation; group written Γ₁(2) with b ≡ 0 mod 2 and the "mod 1" typo; minimum at T = U = 1+i, positive-definite Hessian, Λ = −0.00789 M_s⁴, metastable. Correctly cited apart from 4(e) and 4(f).
- 2603.08315 (ATLAS): wino-like charginos excluded up to 670 GeV (770 expected), 137 fb⁻¹. Correct.
- 2507.15934 (Safdi & Xu): sub-fraction winos excluded from 1.85 TeV up to the thermal mass. Correct as used for SERAPIS-E; inconsistent with the covariant window (major issue 7).
- 2212.03876 (Leedom, Righi, Westphal): no dS vacua at the fixed points with a tree-level dilaton Kähler potential (Corollary 2.1); windows open only with Shenker-like corrections. The "minimal heterotic setting" claim is correct.
- 1905.11970: the CP-conserving locus (imaginary axis and the boundary of the fundamental domain) is quoted correctly. Not re-fetched (search budget); consistent with the standard result.
- 2408.05203: not re-fetched; the use is the standard Kallosh–Linde SL(2,Z) attractor framework.
- Rankin 1953 and Montgomery 1988 bibliographic data (journal, volume, pages) are correct. The hypotheses are discussed in 4(b)–(c).
