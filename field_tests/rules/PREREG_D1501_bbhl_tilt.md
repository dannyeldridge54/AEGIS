# PREREG D1501 — tilt plan T1: what the exact α′³ (BBHL) potential gives beyond the form-A truncation

Locked 2026-11-19 ~13:30 UTC before computing. Our own file and D-number. Danny 07:21 CT: "Tilt source".
[literature] hep-th/0412239 (Balasubramanian–Berglund) Eq. (3.8): V = 3ξ̂(ξ̂² + 7ξ̂𝒱̂ + 𝒱̂²)/((𝒱̂ − ξ̂)(2𝒱̂ + ξ̂)²)·e^K|W|²,
with K = −2 ln(2𝒱e^{−3φ/2} + ξ(Im τ)^{3/2}) (Eq. 3.1), ξ = −χζ(3)/2 (Eq. 3.2); truncation Eq. (3.9) V_s = (3ξ/4𝒱̂)e^{K⁽⁰⁾}|W|². (Read from the paper this tick.)
SL(2,Z) completion as the P3 chat (D1486): ξ̂(τ) ∝ E(τ,3/2).
Question: at fixed 𝒱̂ and fixed |W| (both as in the P3 chat's form-A frame), write the exact τ-dependence through u = ξ̂/𝒱̂ and compare with the shapes the
P3 runs use — form A (one power of 1/(2𝒱 + ξ)), form B (squared), DILMIX α, and the tilt factor (1 + C·g). Steps (sympy, exact):
 (1) the factor e^K = (2𝒱̂ + ξ̂)^{−2} alone (form-B-like) and the full Eq. 3.8 function G(u) = 3u(u² + 7u + 1)/((1 − u)(2 + u)⁴) (𝒱̂ scaled out);
 (2) series of G(u)/G(u_ρ) in δ = u − u_ρ for small u_ρ, read off the leading power behaviour and the first correction coefficient κ (the would-be tilt per unit δ);
 (3) translate κ to the λ = 1 frame C_model = κ·(something)/a and compare with the needed C ≈ 1–2e-6 at a = 2e3–5e4.
This is an analytic-shape test ([derived] for algebra, [estimate] for the identification with the P3 shapes); no pass/fail. Fixes only via PREREG_D1501_DEVIATIONS.md first.
