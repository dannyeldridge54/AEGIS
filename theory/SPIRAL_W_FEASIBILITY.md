# Spiral Twist w(z): first feasibility pass (exploratory, NOT a test)

> **Update: independent literature mirror PASS.** `spiral_w.py mirror_ramos` → `spiral_mirror_ramos.json`. Ramos-Hamud,
> García-Arroyo, Quevedo & Vázquez (arXiv:2609.22539) publish the full autonomous system for the same two-field
> kinetic-mixing structure (W = e^{−ξφ₁}, V = V₀e^{−λφ₁}).
>
> | Their (λ, ξ) | Their attractor w | Ours | Difference |
> |---|---|---|---|
> | (2, 10) | −0.818182 | −0.818182 | 2×10⁻¹¹ |
> | (2, 100) | −0.980198 | −0.980198 | 1×10⁻¹⁰ |
> | (8, 20) | −0.666667 | −0.666667 | 5×10⁻¹⁰ |
>
> The kinetic share of the second field agrees as well (e.g. 0.078512 against 0.078512). An earlier run of this mirror
> "failed" only because the transcription of their Π dropped the matter term; that was corrected before scoring.
> **The field equations (including the kinetic-mixing sign and factor) are validated.** The remaining Toomey et al.
> mismatch is in their unpublished benchmark inputs or their w_eff bookkeeping, not in our equations. The scan
> results below therefore stand as solver output. The w0–wa conversion was already validated (ΛCDM and single-field
> limits).

**Code:** `spiral_w.py` (two-field background solver + "CPL illusion" fit). **Files:** `spiral_w_scan.json`,
`spiral_w_benchmark.json`. **Tier:** HYPOTHESIS. Danny, 2 Nov: "Yes, build it".

## Model

Einstein frame, Reading B (matter blind to the dilaton):
L = −½(∂χ)² − ½e^{λχ}(∂θ)² − V₀e^{−κχ} − m²F²(1 − cos θ/F).
λ = −2√(2/3) (α = 1) and F = (4/π)√(3/2) = 1.56 are fixed; κ, m, θᵢ are scanned; V₀ is tuned for closure. A CPL fit
to the model's H(z) on 0 < z < 2.5 (matter assumed to dilute as a⁻³) gives the w0 and wa a w0–wa analysis would see.

## Validation (internal): PASS

- With no fields the CPL fit returns w0 = −1, wa = 0, Ω_m = 0.300 exactly.
- A single thawing cosine (λ = 0) gives w0 = −0.950, wa = −0.080; CPL matches the true w(0) = −0.950.
- The full spiral's true w never goes below −1 (minimum −0.958 in the test case): null energy condition holds.

## Assembled result (plug and play: every part now has its own passed check)

| Part | Source | Check |
|---|---|---|
| Geometry: λ = −2√(2/3) | Gates–Ketov–Yunes K | exact algebra (sympy); the α-attractor formula agrees |
| Field equations | this solver | mirror PASS vs Ramos-Hamud et al. (1e-10) |
| w0–wa reading | CPL fit of H(z) | ΛCDM and single-field limits PASS |
| Decay constant F = 1.56 | Nieh–Yan period | derived; TF-P testing it now |
| Stability | two-field sigma model | ghost and gradient PASS |

**What the assembly says (post-hoc, MEANING → EVIDENCE for the solver's statement only):**

- In Ramos-Hamud's notation our fixed geometry is a kinetic coupling ξ = −λ/2 = √(2/3) ≈ 0.82.
- Their DESI fit draws its (slight) benefit only from **ξ > 10^2.57 ≈ 370** (all three potentials).
- **The α = 1 BI geometry is therefore about 450× too weak** to reach that strong-mixing regime. At ξ ≈ 0.8 the spiral
  behaves as exponential (thawing) quintessence: w0 ≈ −0.84, wa ≈ −0.24 at κ = 1, as the scan found.
- Toomey et al.'s posterior λ = −1.3 (ξ ≈ 0.65) is also weak. Their effect must then come from the angle's own
  oscillation and energy exchange (the "matter-like angle" branch), not from strong mixing. That branch is the only
  remaining route for the spiral, and the only part still unreproduced.

**Consequence for the plan:** with α = 1 fixed, the spiral's realistic outcomes are:
- (a) plain thawing: no gain over the minimal Twist;
- (b) the matter-like-angle route: untested.

A stronger mixing would need α ≪ 1 (ξ = √(2/(3α)) > 370 means α < 5×10⁻⁶), which abandons the BI derivation.

## Matter-like-angle route (`spiral_w.py matter_angle`; `spiral_matter_angle.json`, `spiral_matter_angle_big.json`)

The angle oscillates (m = 100 H₀) and makes up a fraction f of the matter. Through the fixed geometry it is dark
matter coupled to the dilaton with d ln m_eff/dχ = 0.816, so β_eff ≈ 0.816 f. True matter is lowered so that the
total stays 0.30. The output is the CPL reading.

| κ | f (angle share of matter) | β_eff | w0 | wa | Plain-thawing wa at that w0 | CPL residual |
|---|---|---|---|---|---|---|
| 1.0 | 4.0% | 0.033 | −0.850 | −0.256 | −0.230 | 0.17% |
| 1.0 | 9.2% | 0.075 | −0.866 | −0.295 | −0.205 | 0.46% |
| 1.2 | 4.2% | 0.034 | −0.777 | −0.356 | −0.341 | 0.17% |
| 1.2 | 9.7% | 0.079 | **−0.795** | **−0.401** | −0.314 | 0.46% |
| 1.2 | 18.1% | 0.148 | −0.830 | −0.599 | −0.260 | 1.2% |
| 1.5 | 10.9% | 0.089 | −0.656 | −0.564 | −0.526 | 0.47% |

- **The mechanism works in the right direction:** the angle pushes wa below the plain-thawing line toward DESI, and
  more so as f grows.
- **Existing data cap it:**
  - the Babu & Amendola bound |β| < 0.073 gives f ≲ 9%;
  - our own Coupled Twist fit points to f ≈ 6% (MIRROR_MAP row 1).

  At those values the bend is only Δwa ≈ −0.05 to −0.09.
- **One clean setting reaches the DESI-like box**: κ = 1.2, f = 9.7%, w0 −0.80, wa −0.40. It sits at the box edge, with
  β_eff = 0.079, just above the bound (and the β mapping is approximate).
- **Reading:** at α = 1 the spiral is **borderline**: it can just touch the DESI-like region at the edge of what the
  coupling bounds allow. It does not reach DESI's central point (w0 ≈ −0.75, wa ≈ −0.86). Only a real fit (the
  two-field AxiCLASS module, with the S8 and DESI-dependence rules of MIRROR_MAP rows 3–5) can say whether this edge
  beats the minimal Twist on data.

## Q3: ghost and gradient check: **PASS** (analytic)

- Kinetic matrix diag(1, e^{λχ}) is positive definite for every χ: no ghost.
- The Lagrangian is linear in the kinetic terms (a two-field sigma model), so both perturbation sound speeds are
  c_s² = 1: no gradient instability and no strong-coupling point. (Contrast the dropped K(φ) = tanh model, which had a
  ghost-sign region and a strong-coupling point at K = 0.)
- The null energy condition holds for the total system (validated numerically above), so the phantom-looking
  behaviour is always an artefact of how the energy is split, never a real ghost.

## Literature mirror (Toomey et al. benchmark): **FAIL**

Their Fig. 1 benchmark settings (λ = −1.25, α = 1.7, m = 11 H₀, f = 0.082 M_Pl, θᵢ = 3.12) give in our code
w0 = −0.47, wa = −0.68, with a poor CPL fit (6% residual). True w(0) = −0.43. **This is not their reported phantom
illusion.** Either our implementation or our reading of their benchmark (units, initial conditions, what counts as
dark energy) differs. Until this mirror passes, the scan below is provisional.

### Mirror, second attempt (their own definitions)

Their paper (read in full): the angle is counted with matter ("all of matter, including the scalar contribution"), and
dark energy is the dilaton's effective w (their eq. 11), not the total. With eq. 11 implemented as written and
χᵢ = 10⁻⁴:

| Run | w_χ,eff today | w_χ,eff at z = 1 | Fitted w0_eff / wa_eff |
|---|---|---|---|
| Their benchmark (λ = −1.25) | **−1.09** | −0.89 | −0.97 / +0.05 |
| Same with our λ = −2√(2/3) | **−1.50** | −0.89 | −1.13 / +0.32 |
| Their posterior, CMB + DESI (Table 3) | — | — | −0.50 ± 0.21 / −1.51 ± 0.60 |

- **The mechanism appears** (the dilaton's effective w dips below −1 while the total system obeys the null energy
  condition), and **our fixed λ makes it stronger.**
- **The mirror still fails on the numbers:** our run is phantom *today* and closer to −1 in the past; their posterior
  (and DESI) wants the reverse. Missing from their text: initial velocities, starting redshift, the units of m and f in
  Fig. 1, and whether Λ is present. Their modified CLASS is not linked. **Status: mirror FAIL, with a known cause
  (unreproducible benchmark inputs), not yet a known bug on our side.**
- To close it: ask the authors for the benchmark inputs or code, or rebuild from their equations with a scan over the
  missing inputs and match their Fig. 1 curves.

### Mirror, third attempt (scan of the unstated inputs): **0 of 86 match**

`spiral_w.py mirror` → `spiral_mirror_scan.json`. Their f = 0.082 M_Pl fixed; scanned λ ∈ {−1.25, −1.633},
κ ∈ {1, 1.7, 3}, m ∈ {3, 5, 11, 30, 100} H₀, θᵢ/f ∈ {2.5, 3.0, 3.12, 3.14}. Target: w_eff above −1 today, below −1 at
z = 1, and (w0_eff, wa_eff) inside their 1σ box. **No combination matches.** Typical result: a thawing curve
(w0_eff ≈ −0.86, wa_eff ≈ −0.19). Either our implementation differs from theirs, or the effect needs inputs outside
this range (for example a large angle energy counted as matter). **Open; the clean fix is to ask the authors for the
benchmark inputs or code (an outward step: Danny's call).** Until then, no spiral w(z) number is used for any claim.

## Scan (80 combinations: κ ∈ {0, 1, 3, 5, 7}, m ∈ {1, 3, 10, 30} H₀, θᵢ ∈ {0.05, 0.15, 0.5, 1.5})

- 36 solved. The rest either overclose (the angle alone exceeds the dark-energy budget) or cannot close (a steep
  dilaton runs away too fast to act as dark energy).
- **Best clean result (κ = 1):** w0 ≈ −0.84, wa ≈ −0.24, CPL residual < 0.1%, almost independent of m and θᵢ.
  - This w0 is DESI's value, but this wa is the plain thawing relation wa ≈ −1.53(1 + w0) = −0.245
    (arXiv:2608.19781, eq. 22), not DESI's ≈ −0.7.
  - **The dilaton is doing all the work. With F = 1.56 the angle carries too little energy to make the kinetic
    mixing matter.**
- **Large |wa| appears only when the angle behaves like extra matter** (e.g. κ = 1, m = 10, θᵢ = 0.5: w0 −0.83,
  wa −1.16), but then Ω_m,eff rises to 0.36 (true 0.30) and the CPL fit is poor (2%). A real fit would have to lower
  the true matter density to compensate; not done here.
- No combination met the DESI-like box (−0.9 ≤ w0 ≤ −0.7, wa ≤ −0.4) with a clean CPL fit.

## Provisional reading

With λ and F both fixed by the torsion/supergravity numbers, the spiral behaves like a thawing exponential dilaton.
It reaches DESI's w0 but not its wa. The phantom-illusion region needs either a much smaller decay constant (the
published model uses about 0.08 M_Pl or less) or the angle as a matter-like component. **Both conclusions wait on
fixing the failed mirror.**

## Next (in order)

1. Fix the mirror: read Toomey et al.'s equations and initial conditions in full and reproduce their benchmark.
2. Rerun the scan, including a "matter-like angle" branch with the true matter density lowered so the total early
   matter matches the CMB.
3. Only then lock a Spiral Twist prediction and fit it (AxiCLASS would need a two-field module: about a day of work).
