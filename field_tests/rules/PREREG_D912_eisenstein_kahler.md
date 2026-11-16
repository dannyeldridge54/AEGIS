# PREREG D912 (P3.K1): plateau from an Eisenstein term in the Kähler potential (D911 lead)
Locked before computing, 2026-11-16.
Model (post hoc, not a frozen prediction): K = −k ln(2y) − c ln E(τ,2), W = W₀ η(τ)^{−2k}, so G = K + ln|W|² = −k ln(2y|η|⁴) − c ln E(τ,2) + const is modular invariant; E(τ,2) normalised as Σ'_{(m,n)} y²/|mτ+n|⁴ = 2ζ(4)y² + πζ(3)/y + … (same function as Ese in antiD3_serapis_e_d835.py). V = |W₀|² e^G (G^{ττ̄}|G_τ|² − 3) + V₀ with G_{ττ̄} = (G_xx + G_yy)/4, |G_τ|² = (G_x² + G_y²)/4; V₀ = 3|W₀|²e^{G(ρ)} so V(ρ) = 0. Optional SERAPIS-E-type tilt: V → V·(1 + C·(E − E(ρ))) with C = 1e-6 (as D835).
Grid: cusp weight w = k + 2c ∈ {2.0, 2.5, 2.9, 3.5}, with k = 0.75w, c = 0.125w (so k > 2c, needed for a positive metric at ρ by D911).
Checks:
(1) Positivity: G_xx + G_yy > 0 on a grid over the fundamental domain (|x| ≤ 1/2, |τ| ≥ 1, y ≤ 6) and along x = 1/2 up to y = 40.
(2) Vacuum: along x = 1/2, V(ρ) = 0, V > 0 nearby (m² > 0 at ρ in the canonical field).
(3) Plateau: sign of V − V₀ at large y (from below = plateau; from above = no plateau descending to ρ).
(4) Spectra (only where (1)–(3) pass): canonical φ from dφ = √(2G_ττ̄) dy along x = 1/2; exact Mukhanov–Sasaki with the D632 solver (running_d632.py lines 12–41, reused verbatim, start at y = 25), N* = 48.4 and 49.9; n_s, r with C = 0 and C = 1e-6.
Verdict rule: REPRODUCES the frozen SERAPIS-E band if some grid point passes (1)–(3) and gives n_s ∈ [0.970, 0.975] and r ∈ [4.55, 5.12]e-4; otherwise FAILS for the band (report the nearest n_s, r).
Prediction (pre-stated, from D911): positivity holds for all grid points; plateau from below only for w < 3 (w = 3.5 fails check 3); the canonical approach exponent is p = √(2w) < √6 < 2√2, so r ≈ 4.75e-4 × 8/(2w): about 9.5e-4 (w = 2), 7.6e-4 (2.5), 6.6e-4 (2.9). Verdict FAILS for the frozen band.
Output: theory/modular/eisenstein_kahler_d912.py → field_tests/results/eisenstein_kahler_d912.txt.
