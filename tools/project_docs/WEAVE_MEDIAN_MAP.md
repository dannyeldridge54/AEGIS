# The Weave: the median map (21 Nov 2026, 13:15 CT)
Danny 13:12: "skip to the end with every direction pointing somewhere. Map the median."
This takes every tested direction from D1806 to D1887 and records which knot, torus, flux and stack each one points to, then writes down the single configuration they meet at (the median). Each line gives its D-note and status. D1806 to D1887 are not yet independently refereed; D1873 to D1882 are self-refereed (D1878, D1883).

## 1. Where each direction points
| direction | points to | status |
|---|---|---|
| Fold | Z₆-II, twist (1/6, 1/3, −1/2), χ = 48, N = 6 | fixed (D1847, D1871) |
| Two N = 2 planes | plane 2 = the **turnover at ρ**, plane 3 = the **pyramid at i** | literature (D1880, D1881) |
| Strong-force gap Δ₃ | **one Higgs pair, weight 0 on both planes** closes it to −0.02 | conditional (D1881a) |
| Quark charges | can't come from one torus: one weight gives **whole steps only** at both knots | theorem (D1874–D1876) |
| Quark sector | **two stacks one weight apart** (Q₃, u₁, d₁ shifted): natural 18 %, CP 41 % | PASS (D1884) |
| Quark flavour group | consecutive weights ⇒ **level-3 (A₄-type)** | derived (D1886) |
| Charged leptons | **turnover, one weight, three whole rungs** (τ 0, μ 1, e 2) | PASS, modest (D1877) |
| Koide's bend δ | **electron one corner off the Higgs on a flux-6 turnover** (0.177 vs 0.152) | **WITHDRAWN (D1885a)** |
| Neutrinos | **pyramid at i**, flux (4, 4, 8), θ-step n = 3 ⇒ M_N ≈ 1.9e11 GeV | candidate (D1821, D1822) |
| Unification | M₁₂ = 1.06e16 GeV, α⁻¹ = 28, gluino 5.6 TeV | computed (two-loop) |
| Dark sector | dark SU(12) = 2 × 6 on its own cycle, α_D ≈ 0.021 | computed (D1812) |
| Reverse thread | corner hiding is closed (D1873, D1882); **thread on the dark cycle** gives ζ_α ≈ 4e-10, at most 3 crossing units | PASS, estimate (D1887) |
| Outside | **one knob**: the cusp plateau V∞^{1/4} ≈ 0.47 M₁₂ | postulate (U22′) |

## 2. The median: the one configuration every arrow meets at
- **Centre:** the Z₆-II fold. Its two splitting directions are the two knots.
- **ρ, the still point (turnover, Z₃).** Leptons and quarks live here.
  - Leptons: one stack, three whole rungs. ~~flux 6, electron one corner off the Higgs~~ — WITHDRAWN (D1885a); the Koide bend δ and the electron coefficient are inputs.
  - Quarks: two stacks one weight apart, under a level-3 flavour group.
- **i, the hub (pyramid, Z₂).** Neutrinos live here: flux (4, 4, 8), one θ-step down, which fixes the heavy-neutrino scale.
- **Shared between the two:** one Higgs pair with weight 0 on both planes. It is the bridge that closes the strong-force gap at unification.
- **The mirror:** the dark SU(12) cycle carries the dark-energy thread. It touches our side only through at most 3 units of crossing strings, the lock between the two weaves.
- **Outside:** one knob, the cusp plateau.

## 3. The median step (the rung size the sectors ask for)
| sector | step \|u\| |
|---|---|
| up quarks | 0.0031 (the outlier; it sits on the shifted stack) |
| leptons (ladder band, geometric middle) | 0.0169 |
| leptons (slip, D1832) | 0.0253 |
| neutrinos, e^{−9π/8} | 0.0292 |
| Koide equal-weight root | 0.0436 |
| down quarks | 0.0457 |

- Median 0.027; geometric mean 0.021.
- The neutrino θ-step 0.0292 sits on the median.
- Numerology guard: silver⁻⁴ = 0.0294 and φ⁻⁸ = 0.0213 lie close to these numbers. Close matches like this are easy to find by chance, so they carry no evidential weight until a mechanism ties them in.

## 4. What the median predicts (tests the loop runs next)
1. ~~Koide on the flux-6 turnover with the electron one corner off~~ — WITHDRAWN (D1885a).
2. The level-3 flavour group must come from a flux in the magnetised picture (the flux-6 link is void per D1885a).
3. The thread on the dark cycle must still fit DESI w₀/w_a once its mass and slope are re-derived on that cycle.
4. Count the visible–dark crossing strings in the Z₆-II stack set. They must be at most 3.
5. Check that the Higgs pair's weight-0 assignment fits the two-stack quark weights in the full stack picture.
6. Run an independent referee of D1806–D1887 before any of this is written up.

## 5. Still inputs (not derived)
- δ = 2/9 is only partly explained (the corner offset gives its size to 14 %).
- The value of V∞ (the one knob).
- v/m_SUSY (2.7e-7).
- The absolute flux choices (6 for leptons, (4, 4, 8) for neutrinos) are chosen to fit, not derived.

## 6. End run (D1894, 13:20 CT) and corrections
- **Correction (D1885a):** the flux-6 electron result in D1885 was an artefact of a degenerate mode class, so it is withdrawn. Koide's bend δ is an input again, and so is the electron's coefficient (fixed by Koide at c_e = 0.106).
- **End run:** I ran the whole tolerance ladder at once. One shared step, u* = 0.052, passes every data sector down to ±20 % (×1.2), and fails at ±10 %.
- **What that tests:** the run checks one real relation, the muon-to-tau ratio against the down-quark step. They agree to 30 %. The pyramid's step (0.064) also agrees, to about 23 %.
- **Up quarks:** their step is close to u*² (two rungs). I'm reporting that number only, not counting it as evidence.
- **Precision limit:** the single-step picture holds to about 20 %. Going finer needs each torus's own rung law.

## 7. Independent referee (D1897) and corrections
- **Bookkeeping:** every lock came before its result, and every checksum verifies.
- **Δ₃ closure withdrawn (D1881b).** Including the gauge term −C(G) gives R = −0.094, which fails. Δ₃ is OPEN again: α_s is 0.1147 (−3.7 σ) without any threshold, and 0.1167 (−1.5 σ, post-selected) with the Higgs pair.
- **The arrow is one weak test (D1894a).** It checks a single ratio, 1.30, which two unrelated numbers would match by chance about 10 % of the time, before counting how many choices were tried.
- **The knot-charge theorem is sound and already known.** Cite Novichkov–Penedo–Petcov, JHEP 04 (2021) 206.
- **Corrections to the inputs:**
  - the gluino is about 4.9 TeV once α₃ is taken at its own scale;
  - the wino is marginal against the LHC disappearing-track limit;
  - leptogenesis must be non-thermal, since T_R ≪ M_N;
  - g_s > 1 is outside perturbative control.

## 8. Variable error (D1894b): the arrow is withdrawn
The "down-quark step 0.0457" used throughout sections 3–6 was the modulus displacement |ε|, not the step u. The true step is u_d = 0.0259. With that, the one shared step fails (m_μ/m_τ ÷ u_d = 2.30), so sections 3, 4 and 6 are superseded. The real cross-sector relation is D1832's u_ℓ = 0.0253 ≈ u_d = 0.0259, a fit within one lock that conflicts with Koide at ρ. The needed displacement is |ε| ≈ 0.045, which is consistent in scale with matter-F-term and loop shifts and ×4,600 away from the IIB flux-clustering statistic.
