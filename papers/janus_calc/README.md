# Janus String Calculator (v1.0)
**Author:** Danny Eldridge (dannyeldridge54@gmail.com) · AEGIS / SERAPIS project · built with Claude (Anthropic)

A fast calculator for inflationary observables (n_s, r, α_s) of single-field plateau models, including the modular-invariant SERAPIS family (SL(2,ℤ) Eisenstein / j-invariant plateaus: SERAPIS-E, SERAPIS-ρ, Chronos, Kairos).

**Method (standard, stated plainly):** one background integration in e-folds; Hubble-flow parameters ε₁, ε₂, ε₃ at horizon crossing; second-order slow-roll spectra (Stewart–Gong / Schwarz–Terrero-Escalante); α_s by differentiating the second-order n_s along the background. The method is the established slow-roll expansion; what this package adds is its application to modular-invariant plateaus, validated against an exact Mukhanov–Sasaki solver.

**Validation (pre-registered, locked before running; files included):**
- Battery A (PREREG_D990): 24/24 SERAPIS-family points pass; |Δn_s| ≤ 2.4×10⁻⁵ (median 1.7×10⁻⁵), |Δr/r| ≤ 0.013%; 8 textbook stress models (m²φ², φ⁴, Starobinsky, natural) also within 3.1×10⁻⁵ / 0.031%. ~1 ms per point vs ~40–70 s for the exact solver (median speed-up ≈ 4×10⁴). Result file: janus_battery_a_d990.txt.
- Battery B (PREREG_D989): α_s against the exact solver on 8 points — results to be added in v1.1.

**Use:** `from janus_calc import models, core; m = models.serapis_E(1.15e-6); m.spectra(50.0); core.alpha_dn(m, 50.0)` (needs numpy, scipy, mpmath; run from this folder: the modular functions the SERAPIS models need are bundled in tools/serapis_calc).
**Integrity:** every file is listed with its SHA-256 in SHA256SUMS.txt. Pre-registrations were committed (with their own .sha256) before the runs they govern.
**License:** MIT (free to use, modify and redistribute with attribution). Please cite the Zenodo DOI.
