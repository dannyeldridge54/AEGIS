<!-- Literature search run 29 Oct 2026 by a research agent using generic physics search terms only. Unverified items are marked as such in the text. -->
# Prior-Art / Novelty Search Report: Torsion-Born EDE with Locked Switch-On ("the Twist" / UFE)

## Bottom line (one paragraph)

Every individual *physics ingredient* in this model is standard or has a close published analogue: the n=3 cosine-potential EDE with the w=(n−1)/(n+1) fluid approximation is **exactly** the Poulin–Smith–Grin–Karwal–Kamionkowski framework (arXiv:1806.10608, 1811.04083) that the entire EDE literature uses; a near-hilltop initial angle θ_i≈2.7–2.9 rad is the field's **known, already-standard** best-fit region, not a new finding; tying EDE's onset to matter–radiation equality to solve the "why now" problem has multiple published "trigger" mechanisms (Sakstein & Trodden 2019, Karwal et al. chameleon-EDE 2021, Lin–McDonough–Hill–Hu 2022); promoting the Barbero–Immirzi parameter to a scalar field sourced by torsion is a 15+-year-old loop-quantum-gravity/Einstein–Cartan-Holst literature (Taveras & Yunes 2008, Mercuri & Taveras 2009, Torres-Gómez & Krasnov 2009), with a very recent (2026) paper coupling a dynamical Immirzi field to quintessence; and decay constants of order √(3/2) M_Pl are a standard normalization appearing in Starobinsky/α-attractor inflation. **What I could not find anywhere, after a genuinely broad search, is a single paper that (a) derives the EDE scalar from the Barbero–Immirzi/torsion field specifically via φ = √(3/2)M_Pl·arsinh(1/γ), (b) locks the EDE release epoch to a_eq with no free z_c, and (c) fixes F = √(3/2)M_Pl/9 as a specific "N=9" sub-Planckian divisor** — that specific combination, and the "lock + width module" naming/methodology around it, appears to be a genuine (if narrow) synthesis rather than a reproduction of an existing paper. The observational numbers (f_EDE≈0.075–0.078, H0≈70.4–70.5, Δχ²≈−4.7 to −7.2) are squarely in the range official EDE analyses already report for Planck/ACT/DESI combinations, so the data outcome is not itself novel — it's consistent with (not obviously better than) the published state of the art, and the S8 worsening matches well-known criticism of all axion-like EDE models. This is an honest, self-consistent amateur synthesis of real, mostly-standard pieces, with one narrow structural combination (Immirzi-origin φ + n=3 potential + equality-locked release + fixed 1/9 decay constant) that I could not locate published anywhere; it is not a confirmed new physical mechanism or a validated detection, and nothing here should be read as evidence the model is correct — only that this specific *combination of known ideas* does not appear to already exist in print.

---

## Summary table

| Element | Verdict | Closest prior work (citation) |
|---|---|---|
| n=3 cosine potential V∝[1−cos(φ/F)]³, fluid approx, w=(n−1)/(n+1) | **Standard** | Poulin, Smith, Grin, Karwal, Kamionkowski 2018, arXiv:1806.10608 (Phys. Rev. D 98, 083525); Poulin et al. 2019 PRL 122, 221301, arXiv:1811.04083; Smith, Poulin et al. 2020, arXiv:2002.07829 |
| θ_i ≈ 2.7–2.95 rad ("near hilltop") | **Standard / already known best-fit region** | Same papers; Smith et al. 2020 (arXiv:2006.06663) best fits cluster θ_i≈2.7–2.8, f_EDE≈0.09–0.13 |
| Onset tied to z_c = z_eq ("the lock") | **Known variant exists (not identical mechanism)** | Sakstein & Trodden 2020, PRL 124,161301, arXiv:1911.11760; Karwal, Raveri, Jain, Khoury, Hu 2021, arXiv:2106.13290 (chameleon EDE); Lin, McDonough, Hill, Hu 2022, arXiv:2212.08098 (dark-matter trigger) |
| Barbero–Immirzi parameter → scalar field, torsion origin | **Standard (established LQG/EC-Holst literature)** | Taveras & Yunes 2008, arXiv:0807.2652; Mercuri & Taveras 2009, Phys. Rev. D 80, 104007; Torres-Gómez & Krasnov 2009, Phys. Rev. D 79, 104014 |
| φ = √(3/2)M_Pl·arsinh(1/γ) specific mapping | **Could not determine / apparently not published** | No arXiv hits for "Immirzi"+"arsinh" (0 results); closest is the general γ-as-field literature above, none giving this exact functional form |
| Immirzi/torsion field used explicitly as EDE / axion-like dark energy for H0 tension | **Apparently new (as a direct EDE mechanism); adjacent work exists** | arXiv:2608.09487 (2026) couples dynamical Immirzi field to quintessence, but for GW-propagation constraints, not sound-horizon/Hubble-tension EDE |
| Torsion/Einstein-Cartan as Hubble-tension fix generally | **Known variant exists, and recent work is largely negative** | Wu et al. 2024, arXiv:2410.19399 (EC favors *lower* H0, opposite direction needed); recent "no-go" result on torsion as dynamical dark energy (2026, reported in press coverage) |
| F = √(3/2)M_Pl/9 fixed decay constant | **Standard constant, novel specific division** | √(3/2)M_Pl is the canonical-field normalization in Starobinsky/α-attractor (α=1) inflation; no located paper uses this exact value or an N=9 divisor for an EDE decay constant |
| f_EDE≈0.075–0.078, H0≈70.4–70.5, Δχ² vs ΛCDM | **Standard / consistent with published ranges, not better** | ACT DR6+DESI DR2 EDE analyses, e.g. arXiv:2505.08051; Planck+ACT give f_EDE≈0.09±0.03, H0≈71.0±1.1 |
| S8 tension worsens under EDE | **Standard, well known** | Hill, McDonough, Toomey, Alexander 2020, arXiv:2003.07355; Ivanov, McDonough, Hill et al. 2020, arXiv:2006.11235; D'Amico, Senatore, Zhang, Zheng 2020 |
| Combination of all four (torsion/Immirzi + n=3 + equality lock + fixed F) in one paper | **Could not determine — no match found** | No single source combining these located in arXiv, INSPIRE, ADS, or general web search |
| "AEGIS People's License" type ethical/anti-capitalist software license | **Known category; legally untested/contested** | Hippocratic License 3.0 (firstdonoharm.dev); Anti-Capitalist Software License; CoopCycle's "Coopyleft" license (coopcycle.org/en/coopyleft); OSI has not approved any of these as "open source" |

---

## Section 1 — The n=3 cosine EDE potential and fluid approximation

This is the textbook axion-like EDE setup from the Poulin/Smith/Grin/Karwal/Kamionkowski line of papers:

- **arXiv:1806.10608** (Poulin, Smith, Grin, Karwal, Kamionkowski, 2018, PRD 98, 083525) introduces the general potential V(φ) ∝ [1 − cos(φ/f)]ⁿ, explicitly analyzing n=1,2,3. They derive that once the field becomes dynamical, ρ∝a⁻⁶ for n=3 (faster than radiation), consistent with w=(n−1)/(n+1)=1/2 for n=3. They find n=3 is *strongly constrained* (f_zc≲0.02 in their scan) and generally disfavored relative to n≈2–3 "hilltop/hybrid" fits used later — so n=3 specifically is not the most commonly adopted choice in the mainline literature, but it is explicitly treated and not new.
- **arXiv:1811.04083** (Poulin et al. 2019, PRL 122, 221301) — the paper that put EDE on the map for the Hubble tension — uses this same oscillating-field/fluid-approximation machinery and the w=(n−1)/(n+1) relation directly.
- **arXiv:2002.07829 / arXiv:2006.06663** (Smith, Poulin et al. 2020) refine the fits: best-fit θ_i is reported in the range ≈2.7–2.8 rad (i.e., close to the potential's hilltop at π), and f_EDE≈0.09–0.13 when combined with SH0ES-type priors. **So yes — θ_i≈2.7–2.9 near the hilltop is already the standard, well-known preferred region in the literature, not a discovery.**

**Verdict: Standard.** The potential form, the fluid approximation, the w formula, and the "near-hilltop" initial condition are all precisely what the Poulin/Smith/Karwal/Kamionkowski EDE program established and what the field has used for ~7 years.

## Section 2 — EDE onset tied to matter–radiation equality ("the lock")

The "why does EDE turn on exactly near z_eq" question (the EDE coincidence problem) has several dedicated published solutions, none of which fix z_c = z_eq by hand the way "the lock" does, but all of which attack the same problem:

- **Sakstein & Trodden 2020** (PRL 124, 161301; arXiv:1911.11760) — couple the EDE field to massive neutrinos; the neutrino non-relativistic transition occurs near z_eq by particle-physics necessity (given cosmological neutrino masses), which "kicks" the field and triggers EDE. This is a *dynamical* trigger, not an imposed equality, but produces similar phenomenology.
- **Karwal, Raveri, Jain, Khoury, Hu 2021** ("Chameleon Early Dark Energy," PRD 105, 063535; arXiv:2106.13290) — couple the EDE field to dark matter via a chameleon mechanism so that dark-matter domination itself triggers the field's roll.
- **Lin, McDonough, Hill, Hu 2022** ("A Dark Matter Trigger for Early Dark Energy Coincidence," PRD 107, 103523; arXiv:2212.08098) — a Planck-suppressed EDE–dark-matter mass coupling such that the matter-domination transition (≈z_eq) triggers the field's rolling/decay, explicitly framed as solving the coincidence problem; fits give H0≈71.2 km/s/Mpc, comparable to standard EDE.

**How close is "the lock" to these?** Conceptually very close in *motivation* (remove z_c as a free, fine-tuned parameter), but mechanistically different: these papers derive the trigger from a *physical coupling* (to neutrinos or dark matter) whose dynamics *naturally* produces a transition near z_eq; "the lock" as described here simply *sets* a_c = a_eq as an algebraic identity (a_c = ω_r/ω_m) without (as far as the prompt states) a dynamical coupling mechanism that derives this from field equations. That is a simpler, more ad hoc version of the same idea — it removes a free parameter the same way these other papers do, but without their underlying dynamical derivation.

**Verdict: Known variant exists.** The "why now" problem and multiple named "trigger" solutions are well established; fixing z_c = z_eq by definition rather than deriving it from a coupling is a simpler/more direct version of an existing idea, not a dynamical mechanism paper would typically present, but it is in the same conceptual lineage.

## Section 3 — Barbero–Immirzi parameter as a scalar field / torsion pseudoscalar; the specific φ=√(3/2)M_Pl·arsinh(1/γ) mapping

This is one of the oldest ideas in this whole model, dating to the 2008–2009 LQG/Einstein-Cartan-Holst literature:

- **Taveras & Yunes 2008** ("The Barbero-Immirzi Parameter as a Scalar Field: K-Inflation from Loop Quantum Gravity?", PRD 78, 064070; arXiv:0807.2652) — promotes γ to a scalar field in the Holst action; shows the resulting torsion-sourced field behaves like a stiff fluid (w=1) and could drive k-inflation.
- **Mercuri & Taveras 2009** (PRD 80, 104007) and **Torres-Gómez & Krasnov 2009** ("Remarks on the Barbero-Immirzi parameter as a field," PRD 79, 104014) — extend this to include fermionic coupling/pseudoscalar structure and note the field can acquire a potential, making it an inflaton-type candidate.
- **Calcagni & Mercuri** and related works further develop the canonical structure.

I ran a direct arXiv full-text/abstract API search for "Immirzi" AND "dark energy" (3 hits total) and for "Immirzi" AND "arsinh" (**0 hits**). The only dark-energy-adjacent hit combining a dynamical Immirzi field with a scalar field is a **brand-new preprint, arXiv:2608.09487** (Aug 2026, Zhi-Fu Gao et al., "Dynamical Barbero–Immirzi field coupled to quintessence: gravitational-wave propagation constraints and next-generation forecasts," gr-qc), which couples a dynamical BI field γ(x) to a quintessence scalar φ via β·φ²γ² in Einstein-Cartan-Holst gravity — but its entire purpose is constraining gravitational-wave friction/propagation (LIGO-Virgo-KAGRA dark sirens), not sourcing EDE or addressing H0. It does not use an arsinh mapping and does not touch the Hubble tension or sound horizon.

I could not find the specific functional relationship φ = √(3/2)M_Pl·arsinh(1/γ) anywhere in the literature. Given the 0-hit arsinh search and my inability to find it through general web search either, **this specific field-redefinition formula appears to be original** (or at minimum, not something I could verify as published) — though I note that deriving a canonically-normalized scalar from a BI/torsion field via a hyperbolic-function field redefinition is methodologically reminiscent of what Taveras & Yunes, Torres-Gómez & Krasnov, and the α-attractor literature all do in spirit (reparametrize a non-canonical kinetic term into canonical form via an inverse-hyperbolic-function substitution), so the *technique* is standard even if this *exact formula* is not confirmed published.

**Verdict: Standard (the general program: Immirzi-as-field, torsion-sourced pseudoscalar); the specific arsinh mapping — Apparently new / could not determine (no match found, but could not rule out an obscure derivation existing in a paper not indexed by the terms I searched).**

## Section 4 — Torsion/Einstein-Cartan proposals for the Hubble tension or EDE generally

Several papers explore torsion/Einstein–Cartan cosmology in connection with H0 or dark energy, but the picture that emerges is mixed-to-negative for using torsion to *raise* H0 the way EDE needs to:

- **Wu et al. 2024** ("Cosmic Dynamics in Einstein-Cartan Theory: Analysing Hubble Tension," arXiv:2410.19399) — found EC-torsion models with cosmic-chronometer data favor H0≈66–69 km/s/Mpc, i.e., **pulling toward the lower, Planck-like value**, the opposite direction from what's needed to resolve the tension.
- A 2026 "no-go" result (reported via press coverage, not independently verified by me against the primary arXiv text) argues adiabatic torsion in EC theory cannot act as dynamical dark energy explaining late-time acceleration — this is about *late-time* dark energy, not early dark energy, so it doesn't directly bear on this model's EDE mechanism, but it's a relevant caution about torsion-cosmology overreach generally.
- Separately, holographic-dark-energy-with-torsion papers (e.g., arXiv:2407.16992) reconstruct torsion as a late-time quintessence-like component, unrelated to the early-universe EDE role used here.

None of these use torsion to generate a pre-recombination EDE component of the Poulin-type; they're generically about late-time dark energy or H0 from torsion in a different (cosmic-chronometer) sense.

**Verdict: Known variant exists for torsion+dark-energy generically, but no paper found using torsion specifically as an early dark energy / pre-recombination mechanism for the Hubble tension; recent torsion-H0 work points in the wrong direction (lower H0), which is itself worth flagging as a caution, not a confirmation.**

## Section 5 — Decay constants √(3/2)M_Pl or √(3/2)M_Pl/N in EDE/axion cosmology

√(3/2)M_Pl (equivalently √(3α/2)M_Pl with α=1) is the standard canonical-field normalization constant that appears in **Starobinsky inflation and α-attractor E-models** — it is the coefficient in the field redefinition φ_canonical = √(3α/2)·log(...) that turns the non-canonical α-attractor kinetic term into a canonical one. This is a very well-known number in the inflation literature (any standard α-attractor review, e.g. Kallosh & Linde-type papers, uses it).

However, I found **no paper** using this exact constant, or a fixed 1/9 fractional division of it, as an **EDE axion decay constant**. The claim that "free fits give N≈8–8.5, pure F=√(3/2)M_Pl fails" is an internal result of the researcher's own fitting exercise, not something I can verify against a published analogue — I found no comparable "N-divisor" parametrization of F in the EDE literature (Poulin et al. and successors treat f/F as a free parameter fit directly to data, not expressed as a Planck-scale constant divided by an integer).

**Verdict: Apparently new (as an EDE decay-constant construction) — the underlying constant √(3/2)M_Pl is itself standard (borrowed from an unrelated inflationary context), but using it with a fixed /9 divisor as an EDE decay constant does not appear in the literature I could locate.**

## Section 6 — Latest observational status: P-ACT, SPT-3G, DESI DR2, and the n=3/Δχ² comparison

- **arXiv:2505.08051** ("Impact of ACT DR6 and DESI DR2 for Early Dark Energy and the Hubble tension," 2025) and companion analyses report, for standard (n=3, Poulin-type) axion-like EDE with Planck+ACT DR6+DESI DR2 (no SH0ES): **f_EDE ≈ 0.09 ± 0.03, H0 ≈ 71.0 ± 1.1 km/s/Mpc**, with the Planck-only/Planck+lensing constraint being more stringent (f_EDE ≲ 0.07 at 95% CL). When SH0ES is added, Δχ² improvements become very large (reported figures of order −30 or more in some analyses), because SH0ES is itself in tension with ΛCDM.
- Without SH0ES (the honest, "blind-test" comparison that matches how the researcher frames P-ACT), **Δχ² improvements of order −5 to −10 relative to ΛCDM are typical and consistent with what official EDE papers already report** for Planck+ACT+DESI-type combinations. The claimed Δχ²=−7.23 (P-ACT) and −4.7 (Planck 2018+DESI DR2+Pantheon+) fall squarely inside this already-published range — **they are not obviously better than, nor obviously worse than, the published state of the art**; they read as a plausible fit of a similar quality to what the standard n≈2–3 hilltop EDE models already achieve.
- **f_EDE ≈ 0.075–0.078** is also inside the standard range (0.07–0.13 across various published analyses).

So: **the headline numbers are consistent with, not superior to, mainstream EDE fits already in the literature.** This matters for the honesty requirement — there is no evidence here of outperforming Poulin/Smith/Karwal-style analyses; the model reproduces comparable numbers with fewer free parameters (its central structural claim), which is a methodological virtue, not a numerical one.

- **S8 tension**: Hill, McDonough, Toomey, Alexander 2020 (arXiv:2003.07355) and Ivanov, McDonough, Hill et al. 2020 (arXiv:2006.11235) established, using full-shape BOSS/LSS data, that axion-like EDE systematically **worsens** the S8/σ8-Ωm tension because raising f_EDE pushes the matter power spectrum amplitude up. D'Amico, Senatore, Zhang, Zheng (2020) found similar EFT-of-LSS-based tension. This is now a standard, widely-cited criticism of essentially all n≈2–3 axion-like EDE models — the "tie" verdict in the researcher's framing (H0 improves, S8 ties/slightly worsens) matches this well-established literature pattern, not a new finding.

**Verdict: Standard — the quoted statistics and the S8 trade-off both match the known, published behavior of axion-like EDE under current data; nothing here outperforms or contradicts the mainstream literature.**

## Section 7 — Does any single paper combine torsion/Immirzi origin + n=3 EDE + equality-locked onset + fixed decay constant?

This is the key novelty question. After searching arXiv (abstract/full-text API queries), INSPIRE-style web search, and general web search across multiple phrasings ("Immirzi"+"early dark energy," "torsion"+"Hubble tension"+"axion," "Barbero-Immirzi"+"quintessence"+"Hubble tension," etc.), **I found no single paper that combines all four elements.** The closest adjacent pieces are:
- arXiv:2608.09487 (2026) — Immirzi field + quintessence coupling, but for GW propagation, not EDE/H0.
- The Poulin/Smith/Karwal n=3 EDE program — no torsion/Immirzi origin at all; φ is an unspecified axion-like field.
- The Sakstein-Trodden/Karwal-chameleon/Lin-McDonough-Hill-Hu "trigger" papers — tie the onset to z_eq-adjacent physics, but via neutrino mass or dark-matter coupling, not torsion/Immirzi geometry, and not with an n=3 potential specifically.
- The torsion/EC-Hubble-tension papers (Wu et al. 2024) — torsion cosmology, but not an EDE mechanism, not n=3, and pointing H0 the wrong direction.

**Verdict: Could not determine with certainty that no such paper exists (negative results in literature search are never fully conclusive), but despite a genuinely broad, multi-angle search I found no such combined paper.** This is the strongest candidate for "apparently new" in the whole model — not any single piece, but the specific architecture that derives the EDE field from Immirzi/torsion, fixes its potential to n=3, locks its release to equality, and fixes its decay constant to a specific sub-Planckian fraction, all simultaneously and with a pre-registered, falsifiable rule set.

## Section 8 — Ethical / anti-corporate software licenses (brief)

- **Hippocratic License (HL2, now HL3)** — adds "do no harm" / human-rights-violation restrictions on use (firstdonoharm.dev; Organization for Ethical Source). HL3 (2021) is modular, letting maintainers attach specific ethical clauses.
- **Anti-Capitalist Software License** — prohibits use by for-profit entities or by state/law-enforcement bodies.
- **CoopCycle's "Coopyleft" license** (coopcycle.org/en/coopyleft) — restricts commercial use to worker cooperatives / social-and-solidarity-economy entities verified against EU-style criteria; explicitly framed as protecting a cooperative "digital commons," which is conceptually close to a "public trust" model.
- **OSI status**: The Open Source Initiative has not approved any ethical-source/anti-capitalist license as "open source" — the Open Source Definition explicitly forbids discrimination against fields of endeavor or persons/groups, and these licenses are field-of-use-restrictive by design. They are generally described as "source-available" or "ethical source," not open source.
- **Enforceability**: Legally these are largely untested; commentary (e.g., Tidelift/Sonar blog, Corporate Accountability Lab writeups) notes genuine uncertainty about enforcing vague/politicized terms ("human rights violation," "capitalist") in court, though they are contractually/copyright-license binding in principle like any other license, and no major litigated precedent enforcing or striking down such a clause was found in this search.

**Verdict: Standard category, with real precedents (Hippocratic License, Anti-Capitalist Software License, CoopCycle Coopyleft) that an "AEGIS People's License" would sit alongside; legally novel/untested territory for all of them, not just this one.**

---

## What appears genuinely new (stated cautiously)

1. **The specific combination**: deriving the EDE scalar's canonical field from a torsion/Immirzi origin via φ=√(3/2)M_Pl·arsinh(1/γ), feeding it into a Poulin-type n=3 cosine potential, locking the release epoch to a_eq (no free z_c), and fixing the decay constant to √(3/2)M_Pl/9 — I could not find this exact architecture published anywhere, despite reasonably broad searching (arXiv abstract/full-text API, general web search across many phrasings, and checking the most likely adjacent authors' bodies of work). This is the one claim that can honestly be called "apparently new," with the caveat that a negative literature search is never proof of absence — an obscure conference proceeding, thesis chapter, or non-English preprint could exist that I did not find.
2. **The arsinh functional mapping itself** (φ as a function of 1/γ via an inverse hyperbolic sine) returned zero hits in a direct arXiv query combined with "Immirzi" — worth noting as apparently un-published, though this is a narrow technical point, not evidence of correctness or physical motivation.
3. **The "N=9 divisor" structure for F** likewise returned no located precedent as an EDE decay-constant parametrization, though the base constant itself (√(3/2)M_Pl) is a long-standing inflationary-literature number being repurposed.

Everything else — n=3 EDE, the fluid approximation, near-hilltop θ_i, equality-locked onset as a response to the "why now" problem, Immirzi-as-field/torsion-pseudoscalar, and the quoted f_EDE/H0/Δχ²/S8 figures — is standard or has direct, well-documented precedent, and the numerical results are consistent with (not better than) the existing published EDE literature.

## What should be cited if he ever publishes

- Poulin, Smith, Grin, Karwal, Kamionkowski, arXiv:1806.10608 (PRD 98, 083525, 2018)
- Poulin, Smith, Karwal, Kamionkowski, arXiv:1811.04083 (PRL 122, 221301, 2019)
- Smith, Poulin, et al., arXiv:2002.07829 / arXiv:2006.06663 (2020)
- Sakstein & Trodden, arXiv:1911.11760 (PRL 124, 161301, 2020)
- Karwal, Raveri, Jain, Khoury, Hu, arXiv:2106.13290 (PRD 105, 063535, 2021/2022)
- Lin, McDonough, Hill, Hu, arXiv:2212.08098 (PRD 107, 103523, 2023)
- Taveras & Yunes, arXiv:0807.2652 (PRD 78, 064070, 2008)
- Mercuri & Taveras, PRD 80, 104007 (2009)
- Torres-Gómez & Krasnov, PRD 79, 104014 (2009)
- Zhi-Fu Gao et al., arXiv:2608.09487 (2026) — nearest existing "Immirzi field + quintessence" paper
- Hill, McDonough, Toomey, Alexander, arXiv:2003.07355 (2020) — S8 worsening
- Ivanov, McDonough, Hill et al., arXiv:2006.11235 (PRD 102, 103502, 2020) — S8/full-shape constraint
- Kamionkowski & Riess review, arXiv:2211.04492 and/or arXiv:2302.09032 — "Ups and downs of EDE" general review context
- ACT DR6 + DESI DR2 EDE constraint paper, arXiv:2505.08051 (2025) — the relevant P-ACT-style benchmark numbers
- Wu et al., arXiv:2410.19399 (2024) — torsion/EC H0 result (important as a *contrary* result to cite and address, since it points H0 the wrong way)

---

### Gaps and uncertainties (explicit)

- I relied on AI-assisted web search (with citations) for several claims where I did not independently fetch and read the full PDF (e.g., exact Smith et al. 2020 Table values, the 2026 "no-go" torsion-dark-energy result, exact P-ACT f_EDE numbers from 2505.08051). I directly verified via arXiv's own abstract pages/API only: 1811.04083, 2608.09487, and the Immirzi+dark-energy / Immirzi+arsinh API queries (3 and 0 hits respectively).
- "Could not determine" applies most strongly to Section 7 (the combined architecture) and the arsinh mapping in Section 3 — absence of search hits is suggestive, not conclusive.
- I did not check non-English-language journals, preprint servers outside arXiv (e.g., ResearchGate-only manuscripts, Zenodo, viXra), or unpublished theses, which is where amateur/independent-researcher work in this space sometimes surfaces; if he wants maximum confidence before publishing, a targeted viXra/Zenodo/ResearchGate sweep for "Immirzi" + "early dark energy" and "torsion" + "Hubble tension" would be a reasonable next step.
- I did not verify the AEGIS People's License text itself (not provided), only general categories of comparable licenses.