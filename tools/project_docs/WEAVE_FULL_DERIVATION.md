# The Weave: the full derivation chain (forward side + reverse thread), 21 Nov 2026
Danny 13:33: "get it fully derived … then we're going to test it … then a full paper … linking all the tests after it's been refereed."
This file is the chain from the postulates to the observables. Every link names the D-note that holds it (theory/pending_docs/D72_D75_weak_spots.md) and its lock (field_tests/rules/PREREG_*). Status labels:
- **DER**: derived, computed in code from earlier links
- **LIT**: taken from the literature
- **FIT**: one number fixed by data
- **INPUT**: not derived
- **CONS**: consistency only (no test content)
- **OPEN**: unresolved
- **WD**: withdrawn

Refereeing: self-refereed D1878, D1883, D1892; **independently refereed D1897** (corrections D1881b, D1886a, D1894a; rerun D1898: 13 PASS, 3 FAIL). Where this file and D1897/D1898 differ, D1897/D1898 win.

---
## 0. Postulates and the one outside input
| # | postulate | role |
|---|---|---|
| U22 | The edge is the SL(2,Z) Farey edge. Ladders are parabolic (cusp) orbits ending on elliptic knots. | sets the stage |
| U22′ | The only thing outside is the cusp, with one knob V∞. Inside are the knots ρ (order 3, still point) and i (order 2, hub), plus the golden, silver and Markov loops, all of which pass through i (D1818). | inside/outside |
| U24 | One source unfolds in stages, and each stage is a lock-and-key selection rule. | organising |
| U26 | Shape ladder: torus → pyramid (T²/Z₂) → turnover (T²/Z₃) → cube → 6D fold. The corners are the splitting points. | geometry |
| U28 | The arrow: one shared rung step with only geometric coefficients (D1889). | test hypothesis |

**The only INPUT outside:** V∞^{1/4} = 4.9e15 GeV = 0.47 M₁₂. It is not tied to any knot quantity (D1839, D1844).

## 1. Geometry: the fold, the knots, the corners
1. **Fold (DER/LIT):** Z₆-II with twist (1/6, 1/3, −1/2). χ = 48 on every lattice (hep-th/0609014; D1847, D1871).
2. **Rank (DER):** the KKLT condition |W₀| = A e^{−x}(1 + 2x/3), with x = 2πσ/N, selects N = 6 for the hidden sector. The dark SU(12) = 2 × 6 sits on its own cycle with σ_d = 40.3 and α_D ≈ 0.021 (D1811, D1812).
3. **Moduli (DER):** 𝒱 ≈ 4.0e4, W₀ ≈ 5.5e-9, A ≈ 0.54 (D1871); m₃/₂ ≈ 2.6e5 GeV.
4. **Where the tori sit (DER/LIT):**
   - Tori 1 and 2 (Z₃-twisted) have U = ρ. These are the turnovers, with 3 corners each.
   - Torus 3 (Z₂-twisted) has U = i. This is the pyramid, with 4 corners.
   - In Z₆-II, θ³ fixes the ρ torus and θ² fixes the i torus. Both are N = 2 planes (D1880, LIT hep-ph/9405420).
5. **Corners (DER):** on the turnover each Z₃ sector sits on its own corner (D1849). On the pyramid the odd mode vanishes at all 4 corners (D1870).

## 2. The knot-charge theorem (DER, D1874–D1876, refereed in D1878)
- At a knot, the stabiliser γ (S at i, ST at ρ) acts on the zero modes of weight k.
- Because γ² (or γ³) is a scalar, all modes of one weight carry residual charges that differ by **whole numbers**. The fractional part is fixed by the weight: n ≡ k/2 · (½ at i, ¼ at ρ for k = ½).
- On the pyramid the even and odd parity sectors carry integer and half-integer charges respectively, and they never mix. A product of Z₂-graded tori cannot mix them either (D1875).
- ⇒ **A half-step gap inside one generation triplet requires generations with different weights (Δk = 1).**
- This is the known residual-symmetry structure (Novichkov–Penedo–Petcov, JHEP 04 (2021) 206, arXiv:2102.07488); D1874–D1876 apply it to the Weave's knots.

## 3. Quarks
1. **Residual-charge lock (FIT + natural):** q_Q = (3/2, 1, 0) and q_u = q_d = (½, 0, 0) form the unique fit out of 117,649 assignments. Their matrix model is natural: 18 % of O(1) draws fit 7 observables, and 31 % of those also fit J (D1828, D1829).
2. **Geometric home (DER):** by §2, Q₃, u₁ and d₁ sit on a second stack one weight unit away. With the Kähler factor (√3)^{∓1/2} the fit stays natural: f7 = 10.7 % / 17.9 %, fJ = 23.5 % / 40.5 %, with Δk = −1 preferred (D1884).
3. **Flavour group (DER):** the Yukawa weights then span three consecutive integers. At level 1 either the odd-weight entries vanish (Y block-diagonal, V_ub = V_cb = 0) or the even ones do, so the model needs level ≥ 3 (A₄-type, Γ(3)) (D1886, corrected D1886a).
4. **Step sizes (FIT):** u_d = 0.0457 and u_u = 0.00311. The up quarks sit at about u*^{1.95}, two rungs of the shared step (reported only, D1894).

## 4. Charged leptons
1. **Ladder (DER, modest):** one turnover with one weight and three whole rungs (τ 0, μ 1, e 2). It is natural for |u| between 0.0066 and 0.0435, at 5.3 %, and most of that comes from the ordering (D1877).
2. **Koide (INPUT):** picture A, Koide exact at ρ, is favoured by the odds (D1837).
   - An equal-weight ladder cannot be Koide-exact (D1879, FAIL).
   - The corner-offset explanation of the bend (D1885) is **WD** (D1885a: a degenerate-class artefact).
   - **δ = 2/9 and the electron coefficient (c_e = 0.106 from Koide) are INPUT.**

## 5. Neutrinos (i, the pyramid; **U = i is a choice, not fixed by the Z₂ action — D1907**)
1. **Ratio (DER):** m₂/m₃ is natural from magnetised Z₂ overlaps at i with flux (4, 4, 8) (1.3 %, D1821).
2. **Scale (CONS):** the θ-step e^{−πn²/8}, with n = 3 the only value inside the leptogenesis window, gives M_N ≈ 1.84e11 GeV (D1822). Since T_R = 3.7e8 GeV ≪ M_N, leptogenesis must be non-thermal (D1897).
3. **Rung ratio (CONS):** the 3→4 step e^{−7π/8} = 0.064 matches the shared turnover step to 23 % (D1891, D1894).

## 6. Forces and unification
1. **Two-loop running (DER):** with the split spectrum, M₁₂ = 1.06e16 GeV and α⁻¹ = 28.0. The AMSB gluino at 5.6 TeV gives α_s(unif) = 0.1147, against 0.1180 measured, which leaves Δ₃ = −0.237 (D1816).
2. **Threshold (DER + LIT):** the two Z₆-II N = 2 planes (ρ, i) have per-unit shifts 0.0823 and 0.0839.
   - The duality-anomaly normalisation applies (D1881).
   - ~~One Higgs pair with modular weight 0 on both planes gives Δ₃ → −0.023~~ — corrected (D1881b): with the gauge term −C(G) included, Δ₃ → −0.094, which fails. Matter weights are not counted, and the U-only case is assumed. **Δ₃ is OPEN**; α_s = 0.1147 is −3.7 σ without a threshold. The brane-picture restoration (U29, D1900–D1904) was WITHDRAWN by the independent referee (D1907). Reasons: the Z₂-twisted aa term is unavoidable on the ρ plane, the Higgs counting was heterotic, U = i is not fixed by the orbifold, and the dropped 2π V constant outweighs the knot term.
   - The step from the field content to b′ coefficients still has to be redone for IIB/D7.
3. **Proton:** the G-branch gives τ ≈ 1.6e35 yr at two loops, or the proton is stable.

## 7. Spectrum (DER from the master relation and AMSB)
| state | mass |
|---|---|
| gravitino | 2.6e5 GeV |
| winos | 0.69 TeV (marginal against the 0.66 TeV LHC limit; O(1) higgsino threshold) |
| gluino | 4.9 TeV (α₃ at its own scale, D1898) |
| bino | ≈ 2.3 TeV |
| scalars and higgsinos | 0.25–0.7 PeV |

tan β is between 1 and 4. v/m_SUSY ≈ 2.7e-7 is **INPUT** (tuned).

## 8. The single arrow (U28): the predictive statement
- **End run (D1894):** one step, u* = 0.052, threads every data sector to ±20 % and fails at ±10 %.
- **Data content:** one fitted u* against m_μ/m_τ (data) and u_d (a FIT from the D1828 scan). That is one effective test, at about a 10 % chance level before trials (D1894a). Δ₃ and the thread do not depend on u*.
- **Precision limit (D1895):** the per-torus steps cannot be derived from generic modulus displacement. The step needs |δτ| ≈ 0.09, while the IIB flux landscape prefers |δτ| ≈ 1e-5 (arXiv:2206.04313). **This tension is OPEN and ranked first.**

## 9. Cosmology (forward)
- **Inflation:** plateau E(S, 3/2) with A = 7.30 = (8/3)·2ζ(2)/ζ(3).
- **Predictions:** n_s = 0.9706, r = 5.4e-4, α_s = −9.9e-4, T_R = 3.7e8 GeV, ΔN_eff = 0, 12.8 GeV collisionless dark matter from one asymmetry, no domain walls.

## 10. Reverse weave (dark energy)
1. **Closed routes:**
   - An axion thread (excluded by m = 282 H₀).
   - Corner shielding: U27 fails with s = 0.53 (D1873), and the best high-flux odd mode gives only s = 0.17 against the 4.3e-3 needed (D1882).
   - The dark-dimension route is in hard conflict.
2. **Viable route (DER, estimate):** the thread lives on the dark SU(12) cycle and reaches α only through loops.
   - With no crossing states, ζ_α ≈ 3.8e-10, far below the 1.66e-6 bound.
   - Up to 3 units of crossing (bifundamental) states are allowed (D1887).
3. **OPEN:**
   - The thread's slope: a volume-direction thread (λ = 0.943 from the warped uplift, D1902) is EXCLUDED by Cassini (γ − 1 = −0.22, D1906). The thread must be orthogonal to 𝒱 and have its own slope source — OPEN.
   - The actual crossing count.
   - A′ = 4.45 (locked as RW10 for DR3).

## 11. Final list of INPUTS (plus: g_s = 2/√3 > 1 is outside perturbative control, D1897)
1. V∞ (the one outside knob).
2. δ = 2/9 and the electron coefficient (Koide).
3. The per-torus rung steps (u_d, u_ℓ, u_u), against a landscape tension of about 10⁴ (D1895).
4. v/m_SUSY.
5. The flux choices: (4, 4, 8) on the pyramid, and the turnover fluxes.
6. The dark-thread potential parameters.

## 12. Withdrawn or failed (kept for the record)
- D1757a (U1)
- D1795 (computed Λ)
- D1842 (gauge artefact)
- D1873 and D1882 (corner shielding)
- D1879 (equal-weight Koide)
- D1885 → D1885a (flux-6 electron offset)
- D1893 (crash, reverted)

## 13. Tests, linked
Each test has a lock (`field_tests/rules/PREREG_<name>.md` + `.sha256`) and a result (`field_tests/results/`). The suite `field_tests/weave_suite.py` re-runs the headline numbers (task 3). The list below covers this segment's chain. The locks A2 through D6 and B1/B3/B4/B8/B9/B10/C1/C2/C4/C6/C7/D2/D4/D6 are forecasts against future data.

| claim | lock | result |
|---|---|---|
| exact KKLT, N = 6 | D1811, D1812 | d1811/d1812 scripts in theory/tests |
| threshold at the knot | D1816, D1820 | d1816_threshold.py, d1820_neq2.py |
| quark lock, CP | D1828, D1829 | d1828_chargescan.py, d1829_cp.json |
| Koide odds | D1837 | d1837_koideodds.py |
| corners | D1849, D1870 | d1849_corners.py |
| pyramid thread | D1873, D1882 | d1873_oddthread.txt, d1882_highflux_odd.txt |
| knot-charge theorem | D1874, D1875, D1876 | d1874/d1875/d1876 txt |
| lepton ladder | D1877, D1879 | d1877/d1879 txt |
| Z₆-II threshold | D1880 | d1880_z6_threshold.txt |
| two-stack quarks | D1884 | d1884_mixedweight.txt |
| dark-cycle thread | D1887 | d1887_darkcycle.txt |
| arrow and end run | D1889–D1891, D1894 | theory/median/engine.py, end_run.py, d1889–d1894 txt |
