# Mirror-Loom notes (independent test of a richer Loom method; D1950–D1969 reserved; 21 Nov 2026)
Danny 14:35: "have the other chat agent take it past the 3-point posteriors and look even beyond that and continue the mirror method of SERAPIS itself."
Method: (A) ≥ 5 bearings per data need → a posterior (Gaussian product, Student-t ν = 3, and PRIMARY good-or-bad mixture), with intervals, χ²/Bayes-factor consistency and weights; (B) the SERAPIS mirror for every result (forward ↔ reverse, UV ↔ IR, visible ↔ dark), where a result counts only if both sides pass at the centre.
Script: field_tests/mirror/mirror_posteriors.py (one pass). Output: field_tests/mirror/mirror_posteriors_results.txt.

## D1950 / D1951 — locks
PREREG_D1950_MIRROR_DISPLACEMENT and PREREG_D1951_MIRROR_VOLUME_PPN (+ .sha256) were pushed first (commit c1d7ba9f), before any research. The coordinator's correction (D1894b: need |ε| = 0.0457, not 0.090; D1906a: γ − 1 = −0.40) arrived before the lock and is built into it. No DEVIATIONS file is needed.
**Selection decisions (made after reading and before computing; recorded so they can be checked):**
- (i) Vacua exactly at a knot (King–Wang 𝒜 = 4 at ω, and at i; Knapp-Pérez f_X = 3.49e-8 at i) have log|δτ| = −∞. They cannot be log-Gaussian bearings, so they are listed as context only. For each source the nonzero produced values are used.
- (ii) The ephemerides share data, so I took the latest numeric value per ephemeris family (INPOP, EPM, DE), plus Cassini and the MESSENGER-based INPOP13c.
- (iii) The Yoga-dark-energy source (2111.07286) could not be opened (proxy allowlist). Coupling bearings C2–C5 are therefore analytic model variants (separate code paths), each ×2-inflated as non-Weave models. The LVS "1/√6" coupling is from memory and is not used.
- Web calls: 13 (one failed). That is one over the aim of 12.

## D1952 — Test 1: modulus displacement off ρ, posterior fix + mirror — forward PARTIAL (FRAGILE); mirror PASS (THIN, bimodal); centre balance TENSION ⇒ does NOT count
**Bearings near ρ (all opened)**, given as centre and σ in dex (×2 where the framework is not IIB D7):

| bearing | source | framework | centre | σ (dex) |
|---|---|---|---|---|
| B1 | 2206.04313 | IIB flux landscape | 1e-5 | 0.50 |
| B2 | 2304.14437 | heterotic S + τ + ISS, AdS 0.024 / dS 0.075 | 0.042 | 0.49 |
| B3 | 2310.15604 | CW radiative A₄, 0.024–0.2 | 0.070 | 0.91 |
| B4 | 2310.10369 | King–Wang multi-modulus SUGRA, 0.012 AdS and dS (distance computed from the quoted τ) | 0.012 | 0.40 |
| B5 | 2412.07642 | Fan–Wang–Zhang nilpotent-X SUGRA, Minkowski, ε = 6.8e-6–6.6e-5 (tuned by f₀) | 2.1e-5 | 0.99 |

**Posterior** (need 0.0457):

| combiner | median | 68 % | 95 % | ratio | verdict |
|---|---|---|---|---|---|
| Gaussian | 0.0023 | 0.0013–0.0040 | — | ×20 | FAIL |
| Student-t | 0.014 | 0.006–0.030 | 0.0014–0.064 | ×3.3 | FAIL |
| **mixture (primary)** | **0.020** | **0.008–0.044** | **9e-6–0.10** | **×2.3** | **PARTIAL** |

- Under the mixture, the need lies inside the 95 % interval and just outside the 68 % one.
- **Consistency:** χ² = 39.0 for 4 dof (p = 7e-8), and BF(one common value) = 6e-7. The bearings do NOT share one value. The landscape is **bimodal**: a frozen or tuned cluster at ~1e-5 (B1, B5) and a dynamical cluster at 0.01–0.07 (B2–B4).
- **Weights:** inverse-variance 0.24 / 0.25 / 0.07 / 0.38 / 0.06. Mixture P(good) 0.06 / 0.87 / 0.85 / 0.87 / 0.18. **The only IIB-matched bearing (B1) is the one rejected.**
- The superseded need 0.090 would be ×4.5, a FAIL.
- **3-point fix** (1e-5 / 0.027 / 0.069 → 0.027, ×1.69) is also PARTIAL, so the category agrees. The posterior centre is lower (0.020 vs 0.027) because of B4. The posterior also shows formally that the verdict depends on the combiner, the same lesson as D1908a's extraction-rule dependence.
- **Verdict (locked rule): PARTIAL, FRAGILE.**

**MIRROR (dark / thread modulus off i):**
- Need: |δ_i| < 5.9e-3 (the Z₂ α-protection, d < 4.2e-3 M_P, D1853, n = 1).
- Only 2 near-i bearings exist (THIN): I1 IIB landscape 1e-5, and I2 heterotic 0.010–0.028. 2310.15604 and 2412.07642 give nothing near i, and King–Wang gives exactly i.
- Posterior (mixture) median 3.4e-4 ⇒ PASS by the locked rule. But the two bearings disagree (χ² = 23 for 1 dof, P(good) 0.44 each), so the median sits in the valley between two modes. **The honest reading:** the mirror PASSES only on the IIB-clustering mode and FAILS ×1.7–4.7 on the dynamical mode.

**CENTRE BALANCE (the locked tension clause): TENSION.**
- No single mechanism class passes both ladders.
- The dynamical F-term/uplift class (2304.14437, the same paper on both sides) gives the forward side its PARTIAL (0.024–0.075 at ω), but moves i by 0.010–0.028, which fails the mirror.
- The IIB-clustering class passes the mirror (1e-5) but fails forward by ×4,600.
- **Test 1 therefore does NOT count.** Escape routes, each a postulate for the main Loom:
  - (a) the ρ-torus and the dark i-torus are stabilised by different sources (an uplift localised on the flavour torus);
  - (b) the dark modulus sits exactly at i by tuning (exact-i vacua exist in 2304.14437 and 2310.10369);
  - (c) U = i is dropped (it is already a choice, D1907).

**New finding for the main Loom:** the forward PARTIAL relies on non-IIB frameworks, and the SAME mechanism breaks the dark-side α protection.

## D1953 — Test 2: volume-direction thread vs PPN γ, posterior fix + mirror — FAIL (robust), mirror FAIL ⇒ excluded on both ladders
**Part (a), the bound on γ − 1.** Bearings, γ − 1 in units of 1e-5:

| bearing | measurement | value |
|---|---|---|
| G1 | Cassini | 2.1 ± 2.3 |
| G2 | INPOP13c + MESSENGER | −0.3 ± 2.5 |
| G3 | EPM2011 | 4 ± 6 |
| G4 | INPOP20a | 2.64 ± 3.44 |
| G5 | DE405 | 40 ± 10 |

Sources: G1 is Bertotti 2003 via Genova+ 2018 (Nature Comms 9:289, Table 1); G2–G5 are from Fienga & Minazzoli, arXiv:2303.01821, Table 5.
- **Posterior (mixture):** 1.6e-5, with 68 % [0.13, 3.1]e-5 and 95 % [−1.3, 4.6]e-5. **B95 = 4.6e-5**, tighter than Cassini alone (6.7e-5).
- χ² = 15.4 for 4 dof (p = 0.004), driven by G5 (P(good) 0.18; the others ≈ 1.00). BF(common) = 2e5.
- Weights: 0.40 / 0.34 / 0.06 / 0.18 / 0.02.

**Part (b), the coupling α (DEF convention):**

| bearing | model | α |
|---|---|---|
| C1 | Weave n = 1, m ∝ M_s (D1906a) | 0.50 ± 0.10 |
| C2 | Weave n = 1, m_e ∝ m₃/₂ | 1.00 ± 0.20 |
| C3 | no-scale n = 3, m ∝ M_s | 0.87 ± 0.35 |
| C4 | n = 3, m ∝ m₃/₂ | 1.73 ± 0.69 |
| C5 | n = 2 | 0.71 ± 0.28 |

- **Posterior (mixture):** α = 0.68, with 95 % [0.43, 1.18].
- Consistency is ambiguous: p = 0.09, BF 0.65. The C1/C2 split is species-dependent, an equivalence-principle (MICROSCOPE) channel, as D1906a noted.
- **Predicted |γ − 1| = 0.64**, with a 95 % lower bound of 0.31. That is **×1.4e4 over B95 ⇒ FAIL in all three combiners.**
- Cassini requires α < 4.8e-3.
- 3-point / D1906a gave FAIL ×6,000 (α = 0.5 against 6.7e-5). This posterior gives ×8,700 for α = 0.5 against B95. Same verdict, slightly stronger.

**MIRROR (the visible-sector volume modulus in the early universe):**
- Since BBN (the thread is frozen until late, Δφ = 0.64 M_P, D1853), Δ ln(G m²) = 2|β|Δφ = 0.45 (C1), up to 0.62 at the posterior median. That is effectively G_BBN/G₀ ≈ 1.6–1.9.
- The bound is 0.99 (+0.06, −0.05) at 95 % (Alvey+ 2019, arXiv:1910.10730, BBN + Ω_b h²). The prediction is **×9–16 over it ⇒ FAIL** (THIN: one BBN source).
- Late-ladder cross-check: the G m² drift of 3.6e-11 /yr is ×480 over EPM2021's (0.85 ± 3.75)e-14 /yr (2303.01821, Table 6). This replaces D1906's LLR value, which was from memory.
- **The mirror adds something the 3-point fix did not have:** BBN is cosmological and unscreened, so a chameleon/screening rescue of the Solar-System bound cannot save a volume thread.
- **CENTRE:** both sides FAIL ⇒ the volume direction is **excluded on both ladders**, independent of screening.

## D1954 — METHOD verdict (Mirror-Loom vs 3-point Loom)
- **Test 2:** the conclusion is unchanged (FAIL at every level). The posterior adds a tighter bound and an outlier flag (DE405). The mirror adds a screening-proof second kill (BBN) and replaces a from-memory LLR number with an opened source.
- **Test 1:** the category is unchanged (PARTIAL). But the method caught three things the 3-point fix missed:
  1. the bearings are formally inconsistent (BF 6e-7: a bimodal landscape, so "the" median is a modelling choice);
  2. the verdict is combiner-fragile (Gaussian FAIL), and the only IIB-matched bearing is the outlier;
  3. the mirror exposed a centre-balance TENSION, which demotes the result from "PARTIAL" to "does not count".
- **Cost:** about 3–4× the web calls per data need. There is also a new hazard: a median of a bimodal posterior can sit in a valley (as in mirror 1). When BF < 1, report the modes, not the median.
- **Recommendation:** adopt it for **data ticks only**, meaning a data need that feeds a verdict near a bar, or any quantity shared by both ladders. Use the mixture combiner as primary, require the FRAGILE label and a mode report when BF < 1, and make the mirror mandatory. Keep 3-point fixes for routine ticks.
