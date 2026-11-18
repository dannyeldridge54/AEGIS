<!-- AEGIS-FP L2MHITDTBOUD6I22 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Janus String Calculator (v1.3)
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

- **J7b, ASPIC on 17 models (PREREG_J7b):** 32 scored points (power-law p = 2, 4, 2/3, 3, 1; Starobinsky; natural f = 5, 7, 10; ESI q = 1, √2; MHI; RGI; double-well; small-field; logamediate), α_s reference convergence-checked first (R0). Median errors vs exact Mukhanov–Sasaki: n_s 2.0×10⁻⁶ (Janus) vs 7.1×10⁻⁴ (ASPIC), r 8.7×10⁻⁵ vs 2.8×10⁻², α_s 4.1×10⁻⁷ vs 2.0×10⁻⁵; Janus better on n_s at 32/32. (KMII α = 2: ASPIC reports never-ending inflation; listed, not scored.) `validation/results/janus_j7b_*.txt`.
- **J7c2, ASPIC's reheating route (PREREG_J7c2):** same ln R_rad (0, −10) on 16 models; reference = exact Martin–Ringeval matching (arXiv:1004.5525 Eq. 15) with exact-MS amplitude normalisation. Median errors: n_s 2.6×10⁻⁶ vs 6.7×10⁻⁴, r 9.7×10⁻⁵ vs 2.5×10⁻², α_s 5.5×10⁻⁷ vs 2.0×10⁻⁵; ASPIC's pivot is 0.16 e-folds off (median), Janus's 1×10⁻⁴. The first lock (J7c) had a derivation slip in its own matching equation and is kept as VOID with the reason. `validation/results/janus_j7c2_reheat.txt`.

- **J7d + J1d, two-parameter models and PSNI (PREREG_J7d, J7d2, J1c, J1d):** twisted (TI) and small-field (SFI) at two settings each: median n_s error 1.7×10⁻⁶ vs ASPIC 6.1×10⁻⁴ (8/8). PSNI (α = 10⁻³, f = 5): in an exact treatment ε_H = 1 is never reached before the log singularity (ε_H ≈ 0.07 there), so the end of inflation must be a field value; given ASPIC's own end point, Janus n_s error 1–3×10⁻⁷ vs ASPIC 2.6–3.6×10⁻⁴. Two intermediate locks (J7d2 start-finder, J1c stiff fallback) did not fix PSNI and are kept with their diagnosis. New option: `Model(V, dV, phi0, end_y=...)` ends inflation at a field value.
- **Running total vs ASPIC:** 42 scored points at fixed N* (22 model settings) + 32 on the reheating route; Janus has the smaller n_s error at every one.

**New in v1.3 (18 Nov 2026):**
- **Start-condition ripple fixed** in the exact Mukhanov–Sasaki solver (`tools/serapis_calc/ms.py`): starting modes too close to horizon crossing (bd = 200) left a 1e-4-level ripple in exact α_s; the fixed start makes exact α_s stable to 2e-5 (see doi:10.5281/zenodo.24330318).
- **Compiled exact path** (`tools/serapis_calc/ms_jit.py`, optional numba): a 9-k exact spectrum in 0.9–3.8 s instead of ~570 s.
- **SERAPIS tools bundled:** `pipeline.py` (T_R → N* → exact n_s, r, α_s), `emulator.py` (fast SERAPIS-E surrogate; vs exact |Δn_s| ≤ 3.2e-5, r to 1e-6, α_s to 1e-5 over C = 1.0–1.6e-6), `meter.py` (inverse meter n_s → C → Im S·Im ρ), `nstar.py`, `relation.py`.
- **Compiled multi-field helpers** (`janus_calc/core_jit.py`, `mf_jit.py`, `mfms*.py`; optional numba).
- Imports made package-relative so everything runs from this folder.

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
**License:** MIT (free to use, modify and redistribute with attribution). Please cite the Zenodo DOI: https://doi.org/10.5281/zenodo.24298159 (v1.0); v1.1: https://doi.org/10.5281/zenodo.24298903; v1.2: https://doi.org/10.5281/zenodo.24299624; v1.3: new version of the same concept (see the Zenodo record).
