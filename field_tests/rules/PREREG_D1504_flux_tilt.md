# PREREG D1504 — tilt plan T3: τ-dependent flux superpotential W(τ) = ∫Ω∧G₃, G₃ = F₃ − τH₃, as the tilt source

Locked 2026-11-19 ~13:37 UTC before computing. Our own file and D-number.
[literature, read this tick] hep-th/0412239 Eq. (2.4) W = ∫Ω∧G₍₃₎, G₍₃₎ ≡ F₍₃₎ − τH₍₃₎; Eq. (2.5) dilaton Kähler term −log(−i(τ − τ̄)); Eq. (3.8) α′³ potential.
Model (complex structure frozen, D_U W = 0 assumed): W(τ) = f − τh (f, h effective complex-structure-weighted flux periods), K = −2 ln(2𝒱̂ + ξ̂) − ln(−i(τ − τ̄)).
Steps (sympy, exact algebra; [derived]): (1) the no-scale-breaking flux term V_τ = e^K K^{ττ̄}|D_τW|² along τ = x + iy at x = ½ (K^{ττ̄} from K, D_τW = ∂_τW + K_τW);
(2) its y-scaling relative to the α′³ plateau term (Eq. 3.8 leading part ∝ ξ̂ e^K|W|²/𝒱̂) — shape exponent in y;
(3) [estimate] the flux ratio h/f needed for that term to supply the needed relative tilt C·g ≈ 2e-4 at horizon exit (C 1.5e-6, g ≈ 126 at the strip centre, D1497/D1485),
 at the D1486 benchmark (|χ| 200, 𝒱 1e3, y* ≈ 6.4e3), and compare with integer-flux naturalness (h/f ≳ 1/N_flux).
Rule: viable only if the shape grows like y^{3/2} (or close) AND the needed h/f is natural; else report which fails. Fixes only via PREREG_D1504_DEVIATIONS.md first.
