# PREREG SPTILT_TF — the GKP flux potential of the axio-dilaton, with its flux minimum at ρ, as the P3-S tilt

Locked 2026-11-19 (09:40 CT) before computing. DpL cycle 5 (postulation).
Derivation (this cycle, stated before computing): W ⊃ A − τB (G₃ = F₃ − τH₃), K ⊃ −ln(−i(τ − τ̄)) ⇒ D_τW = −(A − τ̄B)/(τ − τ̄) and the no-scale
dilaton F-term potential V_flux = e^{K}K^{ττ̄}|D_τW|² ∝ |A − τ̄B|²/Im τ (times e^{K_cs}/𝒱²). A τ-dependent W₀ therefore does NOT make the
BBHL term y^{5/2}: it switches on V_flux, which is larger than V_α' by ~𝒱³/ξ̂. Taking the flux vacuum at ρ (A/B = ρ̄, D_τW(ρ) = 0):
V_flux ∝ |B|²|τ − ρ|²/Im τ. Along Re τ = ½: X_F = (y − √3/2)²/y — zero at ρ (keeps the P3-S vacuum), ~y at large y (rises like Λ^{−4}).
Postulate (candidate) P3-S-F: V = V₀(1 + C·X_F), V₀ = the P3-S species plateau, i.e. the tilt is the residual flux potential of a
dilaton whose flux minimum coincides with the species desert point ρ.
Run: same script field_tests/scripts/sptilt/run.py with family TF: X = (y − √3/2)²/y, X_ρ = 0, C = f·8e-4/X(55.64), f ∈ {0.5, 1, 1.5, 2, 2.5, 3}.
Rule: band interval in f and C (interpolated), r at n_s 0.969. Expectation stated now: like T2 (band near f ≈ 1.5–1.8, r ≈ 5.4e-4 at n_s 0.969).
No reruns to chase results; fixes only via PREREG_SPTILT_TF_DEVIATIONS.md written first.
