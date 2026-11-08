# V2 — Light-angle predictions (#3, #6) and the null predictions (#19–24). Scheduled: 9 Nov 09:43 CT

**Depends on:** S8-L scored (noon today) for #3.
**Code ready:** `forward_predictions_cloud.py` handles `spiralL*` (ULA build); P(k) via `axiclass_pk.py`.

## #3 step in the matter power
- Compute P(k, z=0) ratio S8-L / Spiral and S8-L / ΛCDM; record the k where suppression reaches 1%, 5%, and the
  maximum; the mass in eV (approximate, `spiral_l_score.py`), and the "large-misalignment bump" if present.
- Survey targets: Euclid DR1 (mid-2027), Rubin LSST Y1, DESI Lyα (eBOSS/DESI P1D).

## #6 early vs late dark matter
- ω_c inferred at recombination vs today in the coupled Spiral: Δω_c/ω_c = e^(βΔχ) − 1 from the scalar field's roll
  (read φ_scf at z = 1090 and z = 0 from the stored background).

## #19–24 nulls (one rule; values already gathered in the equation-map doc)
| # | Limit | Twist |
|---|---|---|
| 19 | GW170817 \|c_T/c − 1\| ≲ 10⁻¹⁵; LISA/ET Ξ₀ | c_T = c, Ξ₀ = 1 (EC + Nieh–Yan → GR) |
| 20 | GW background circular polarisation | 0 |
| 21 | ESPRESSO Δα/α = 1.3 ± 1.4 ppm (z = 1.15); clocks (1.0 ± 1.1)×10⁻¹⁸/yr | 0 at tree level |
| 22 | Cassini, MICROSCOPE | 0 (baryons blind) |
| 23 | N_eff = 3.044; EDE subdominant at BBN | early field frozen; compute its BBN energy share from the fits |
| 24 | birefringence 0.24° ± 0.06° | ≈ 0° (B4, locked 2 Nov) |
