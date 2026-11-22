# Who got this far, what they did, where they stopped, and how we break through (22 Nov 2026, 08:30; Danny 08:19)
One research pass. Each row lists the best result in that line of work, its method, and its **endpoint** (where it stopped).

| line of work | best achievement | method | endpoint (where it stopped) |
|---|---|---|---|
| **D3 quivers at singularities in a compact CY** (Cicoli et al. 1312.0014; SM quiver 2106.11964) | a chiral left-right SM quiver (dP₅) embedded in a compact CY with h¹¹ = 4; LVS moduli; T-brane dS | local quiver, then global embedding, then E3 instantons, then a T-brane FI term | ~264 vector-like/exotic states **not shown massive**; hypercharge only sketched; F-flatness argued; **flux vs D3 tadpole unresolved**; dS hedged |
| **Explicit small W₀ + dS** (McAllister et al. 2406.13751) | candidate dS vacua with tiny W₀ on explicit CYs | perturbatively flat vacua plus KKLT, computed | **no Standard Model sector** |
| **Heterotic Z₆-II MiniLandscape** (0812.2120, 1003.0084) | exact MSSM spectrum; **an approximate R-symmetry gives W₀ ~ ⟨φ⟩^N = 10^{−O(10)} AND μ ~ ⟨W⟩ ~ m₃/₂** | discrete R-symmetries of the orbifold, broken only at order N = 9–26 | **T-moduli fixing and uplift "studied elsewhere"**, never closed |
| **IIA T⁶/(Z₂×Z₂) global** (2511.05006) | MSSM-like spectrum, STU stabilisation, anti-D6 uplift | wrapping numbers, fluxes, ΔW shift | adjoints and light exotics; flavour put in by hand; **η_B off by 10⁴**; needs a CY |
| **F-theory SU(5)** (review 2401.01939) | large scans of **exotic-free** chiral spectra; non-perturbative rank-up of Yukawas | spectral covers, G₄ flux | moduli + flavour together; doublet–triplet splitting |
| **μ from D-instantons** (hep-th/0609191, 1502.03582) | μ ~ M_s e^{−S_E2}, which can be hierarchical | rigid E2/E3 instantons with the right zero modes | instanton zero-mode/rigidity conditions are model-specific |
| **Tadpole problem** (2010.10519, 2112.00013) | conjecture: flux stabilisation of n moduli costs a tadpole ∝ n | flux counting | a large tadpole for many moduli. **Mild for rigid, few-moduli orbifolds** |
| **Review: what is known** (Marchesano–Shiu–Weigand 2401.01939) | — | — | open: moduli with chirality, the μ-term, flavour, dS, unification |

**The common wall:** nobody has the **chiral SM + all moduli fixed + tadpole + small W₀ + μ** at the same time. Each line gets two or three of these and stalls on the rest.

## Where v4 can break through (each to be locked and tested)
- **B1 (biggest): an R-symmetry at ρ gives small W₀ and μ ~ m₃/₂ in ONE mechanism.**
  - The MiniLandscape result lives on **the same Z₆-II orbifold as v4**.
  - At τ = ρ the residual modular Z₃ acts as an **R-symmetry**, and modular-invariant superpotentials vanish at ρ for generic weights. v4 already found Minkowski vacua at the knots (FRONTIER).
  - So W₀ is small because ρ is an R-symmetric point, and slight breaking gives W₀ ~ ε^k.
  - **Numerology hint (no credit):** W₀ = 2e-9 needs ε ≈ 4.5e-5 at k = 2. The flux landscape's typical displacement from fixed points is |δτ| ≃ 1e-5 (2206.04313).
  - μ ~ ⟨W⟩ then follows from the same breaking, so **the D2100 knob μ_W/μ could become derived**.
  - **This targets two FAILs at once: W₀ and the μ knob.**
- **B2: families from intersections, not from |M| = 9 flux. This removes the tadpole FAIL's main cost.**
  - The tadpole FAIL comes from the |M| = 9 three-family magnetic flux (D3 charge 46).
  - The Seed models (D2095) get **3 + 3 families purely from intersection numbers**, and their charge closes exactly with hidden rings. No D3 flux is needed for chirality.
  - Test: rebuild v4's family mechanism in the intersecting (or T-dual magnetised-without-extra-D3) language and recompute the D3 ledger.
- **B3: exotics.** Use the D2097 size rule (mirror rings ≲ ½ the visible size) plus an F-theory-style scan for exotic-free spectra. Seed v5 needs other χ and tilts.
- **B4: the μ-term from a D(−1)/E3 instanton.** At ρ a D(−1) weighs 4.3e-3 (D2073). A μ_W = 0.25μ ≈ 22 TeV needs S_inst ≈ ln(M_s/22 TeV) ≈ 27. Check whether a rigid E3 on a cycle of volume ~27/2π ≈ 4.3 exists in Z₆-II.
- **Not a route for v4:** the D3-at-singularity quivers. They fix mirage by sequestering, but give α_G ≈ g_s = 1.155 at ρ, which is far too strong (D2054). This is exactly the wall they did not face, because they work at weak g_s.

## Read
v4's assets line up with the walls others hit:
- **the Z₆-II orbifold and the R-symmetric knot ρ** address small W₀ and the μ-term (the heterotic wall);
- **rigid, few moduli** keep the tadpole conjecture mild;
- **intersection families** keep chirality cheap in charge.

The order to test them: **B1, then B2, then B4, then B3.**
