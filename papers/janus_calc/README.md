# Janus String Calculator (v1.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24298159.svg)](https://doi.org/10.5281/zenodo.24298159)
**Author:** Danny Eldridge (dannyeldridge54@gmail.com) · AEGIS / SERAPIS project · built with Claude (Anthropic)

A fast, pre-registered and validated calculator for inflationary observables: n_s, r, α_s, β_s for any single-field potential (third-order slow roll on the exact background), reheating → N* in one call, and two-field n_s, r and f_NL^local (δN). Includes the modular-invariant SERAPIS family (SL(2,ℤ) Eisenstein / j-invariant plateaus: SERAPIS-E, SERAPIS-ρ, Chronos, Kairos).

**Method (standard, stated plainly):** one background integration in e-folds; Hubble-flow parameters ε₁…ε₄ at horizon crossing on the exact background; slow-roll spectra to second order (Stewart–Gong / Schwarz–Terrero-Escalante) and third order (Ballardini–Davoli–Sirletti 2024, arXiv:2408.05210 eqs. 47–52); α_s by differentiating n_s along the background; reheating matching for N*; δN for several fields (Vernizzi–Wands astro-ph/0603799; next-to-leading-order field spectra from Byrnes–Wands astro-ph/0605679). An exact Mukhanov–Sasaki solver is bundled (tools/serapis_calc/ms.py) for checking any result. The method is the established slow-roll expansion; what this package adds is its application to modular-invariant plateaus, validated against an exact Mukhanov–Sasaki solver.

**Validation (pre-registered: each test was locked with a SHA-256 before it ran; locks, scripts and results are in this repo):**
- **Battery A (PREREG_D990), n_s and r:** 24/24 SERAPIS-family points pass; |Δn_s| ≤ 2.4×10⁻⁵, |Δr/r| ≤ 0.013% vs the exact solver; 8 textbook models within 3.1×10⁻⁵. ~1 ms per point vs ~40–70 s exact (≈4×10⁴ faster). `janus_battery_a_d990.txt`.
- **Battery B (PREREG_D989), α_s:** 8/8 pass; |Δα_s/α_s| ≤ 0.30% (median 0.10%) vs the exact solver at 305–718 s per point; Janus 3–7 ms (≈1.5×10⁵ faster). The exact α_s reference was itself convergence-tested twice independently (PREREG_D981; runs D990 and D981c agree to 2×10⁻⁶). `validation/results/janus_validate_d989.txt`, `alpha_wide_d981*.txt`.
- **J3, third order (PREREG_J3):** n_s median error 1.6×10⁻⁶, about 10× better than second order. `validation/results/janus_j3_check.txt`.
- **J4, reheating (PREREG_J4):** self-consistent N* from (T_R, w) reproduces an independent exact solution to |ΔN*| < 5×10⁻⁴; n_s within its stated error bar. `janus_j4_check.txt`.
- **J6, two fields (PREREG_J6, J6b, J6c, J6d):** f_NL vs the Vernizzi–Wands analytic result to 0.6%; next-to-leading-order r vs the single-field calculator to 9×10⁻⁵; large non-Gaussianity (|f_NL| up to 81, Byrnes–Choi–Hall Example A) to 0.4–6% on uniform-density slices. Two locks did NOT pass as written and are kept, with the reasons: J6 (r compared at the wrong slow-roll order; fixed by J6b) and J6c (analytic formula compared at ε = 1 where it does not apply; J6d compares where it does).
- **J7a, head-to-head with ASPIC (PREREG_J7a):** ASPIC (github.com/cosmicinflation/aspic, commit 75400d2) built from source and run through its documented route; both codes scored against the exact Mukhanov–Sasaki solver on 14 points (power-law p = 2, 4, 2/3; Starobinsky; natural f = 5, 10; ESI; N* = 50, 60). Median |Δn_s|: Janus 3.8×10⁻⁶, ASPIC 7.7×10⁻⁴ (Janus better on all 14); median |Δr/r|: 7.5×10⁻⁵ vs 2.5×10⁻². ASPIC is faster per point (closed forms, ~0.1 µs, one hand-coded module per model); Janus takes any V(φ) at ~1 ms. The α_s part of J7a was uninformative (reference too coarse) and is being redone in J7b. `validation/results/janus_j7a_*.txt`.

**Use:**
```python
from janus_calc import models, core, anyV, observe, twofield
m = models.serapis_E(1.15e-6); core.spectra3(m, 50.0)            # n_s, alpha_s, beta_s (3rd order), r
s = anyV.from_formula('(1-exp(-sqrt(2/3)*phi))**2'); core.spectra3(s, 55.0)   # any potential
observe.observe(s, TR=1e9)                                        # reheating -> N* -> observables with error bars
twofield.observe_multi(V, grad, hess, [phi1, phi2])               # two-field n_s, r (NLO), f_NL
```
Needs numpy, scipy, sympy, mpmath; run from this folder (the modular functions, multi-field background and exact solver are bundled in tools/serapis_calc). Validation scripts in `validation/scripts` were run inside the AEGIS research repository and are included as provenance.
**Integrity:** every file is listed with its SHA-256 in SHA256SUMS.txt.
**License:** MIT (free to use, modify and redistribute with attribution). Please cite the Zenodo DOI: https://doi.org/10.5281/zenodo.24298159 (v1.0).
