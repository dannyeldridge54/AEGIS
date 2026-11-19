# PREREG GBTILT — can a dilaton-dependent Gauss–Bonnet coupling ξ(τ) ∝ E(τ,3/2) (from α'³R⁴ on a CY) supply the P3-S tilt, and at what size?

Locked 2026-11-19 (10:55 CT) before computing. 1-min derivation loop, κ research (D1560).
Model: S = ∫√−g[R/2 − (∂φ)²/2 − V − ½ξ(φ)R²_GB] (Guo–Schwarz 1001.1897 convention), V = A·V₀(φ) with V₀ the untilted P3-S shape
(species gradient of E_{3/2}, D1523), A = 3H²/... fixed to 1.68e-11 M_P⁴ (H = 5.8e12 GeV; the A_s normalisation, held fixed — stated),
ξ(φ) = ξ₀·(E(τ,3/2) − E_ρ) along Re τ = ½, φ = ln y/√2.
Formulas [literature, Guo–Schwarz eqs. 42–48, first order]: Q = V'/V + (4/3)ξ'V; ε₁ = (Q/2)V'/V; ε₂ = −Q(V''/V' − V'/V + Q'/Q);
δ₁ = −(4/3)ξ'QV; δ₂ = −Q(ξ''/ξ' + V'/V + Q'/Q); n_s − 1 = −2ε₁ − (2ε₁ε₂ − δ₁δ₂)/(2ε₁ − δ₁); r = 8|2ε₁ − δ₁|; N(φ) = ∫_{φ_end}^{φ} dφ/Q,
φ_end at ε₁ = 1; N* = 50.3 (P3-S value, held fixed — stated).
Grid: ξ₀ = ±10^{k/2}, k = 0 … 20 (dimensionless in M_P⁻² units). Control: ξ₀ = 0 must give first-order P3-S values close to engine F
(0.9601 / 4.0e-4; first-order accuracy ~1e-3 in n_s).
Report: ξ₀ band (n_s 0.969–0.975 with r 4.55–5.7e-4) if any, r and n_s at the band centre; then compare the needed ξ₀ with the string
estimate ξ₀ ~ (ζ(3)/(3·2¹¹))·(∫c₂∧J)·(M_P/M_s)²·g-factors (order of magnitude only).
Expectation stated now: the sign with ξ' > 0 (δ₁ < 0 for Q > 0) raises n_s; a band may exist at |ξ₀|·E'·V ~ 1e-2 ⇒ |ξ₀| ~ 1e5–1e7.
No reruns to chase results; fixes only via PREREG_GBTILT_DEVIATIONS.md written first.
