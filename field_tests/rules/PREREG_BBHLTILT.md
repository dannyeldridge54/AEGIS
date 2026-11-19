# PREREG BBHLTILT — pin the normalisation of the α'³ (BBHL) tilt on the P3-S plateau: required volume and the resulting M_s, M_KK

Locked 2026-11-19 (11:05 CT) before computing. 1-min derivation loop; corrects the sign/normalisation guess of D1565.
Inputs [literature]: BBHL (hep-th/0204254) K = −2 ln(𝒱 + ξ̂/2), ξ̂ = ξ·(Im τ)^{3/2} → SL(2,Z)-completed ξ·E(τ,3/2)/(2ζ(3)),
ξ = −χ(X)ζ(3)/(2(2π)³) (X the IIB CY; ξ > 0 ⇔ χ < 0). Frame guide (2301.05178): M_s = g_s M_P/√(4π𝒱), M_KK ≈ g_s M_P/𝒱^{2/3} (order of magnitude).
Derivation (stated before computing): at fixed 𝒱 the τ-dependence enters only through ξ̂(τ):
  (P1) F-term-type prefactor e^{K} ∝ (𝒱 + ξ̂/2)^{−2} ⇒ V ∝ 1 − ξ̂/𝒱 ⇒ relative tilt −ξ E/(2ζ(3)𝒱);
  (P2) D7 D-term prefactor (D1549) ∝ (∂_T K)²/Re f ∝ (𝒱 + ξ̂/2)^{−4/3}·… ⇒ relative tilt −(2/3)ξ E/(2ζ(3)𝒱).
  In the T3 convention V₀(1 + C(E − E_ρ)): C = −ξ/(2ζ(3)𝒱)·w, w = 1 (P1) or 2/3 (P2). Blue (C > 0) ⇔ ξ < 0 ⇔ χ(X) > 0 (h¹¹ > h²¹).
  ⇒ 𝒱 = |χ|·w/(4(2π)³C).
Compute for χ ∈ {+20, +50, +100, +200}, w ∈ {1, 2/3}, C ∈ {6.8e-7, 8.0e-7, 9.37e-7} (the T3 band, D1529/D1532), g_s* = 1/55.64:
  𝒱, M_s, M_KK (GeV and in units of H = 5.765e12 GeV), ξ̂(y*)/𝒱 (perturbativity), 𝒱/y*^{3/2} (2504.01268 control).
Rule ("tilt closes at estimate level"): for some natural χ ≤ 200 and both w: M_s > M_KK > H with M_KK/H ≥ 1.5, ξ̂/𝒱 < 0.1, 𝒱 ≫ y*^{3/2}.
Expectation stated now: 𝒱 ≈ 600–1300·|χ|; M_KK ≈ 1.5–6 H for χ 20–200 ⇒ closes, with the sign condition χ(X) > 0 (incompatible with LVS's
ξ > 0, compatible with KKLT/KL — stated). The species plateau itself remains postulate P3-L.
No reruns to chase results; fixes only via PREREG_BBHLTILT_DEVIATIONS.md written first.
