# PREREG — axio-dilaton route, step 1 (Danny 03:29 "Djl" after the route review): does a plateau built on E(τ,3/2) land in band?

Locked 2026-11-19 before computing.
Motivation: IIB α′³ correction K = −2 log(𝒱 + ξ/2), ξ ∝ χ·E(τ,3/2) after the SL(2,Z) completion (Green–Gutperle) — the Eisenstein
series of the axio-dilaton τ sits inside the overall e^K factor; SL(2,Z) is exact S-duality. Kinetic K = −log Im τ ⇒ n = 1 (the
pipeline's serapis_e path: Re τ = ½, n = 1). Check done before locking: E(ρ,3/2) = 8.8927 < E(i,3/2) = 9.0336 (vacuum at ρ).
Shape forms (Ẽ = E(τ,3/2) − E(ρ,3/2), x = λẼ, λ = 1 frame as for the SERAPIS point):
  A: V ∝ x/(1 + x)·(1 + C·Ẽ)          (one power of the overall factor, as in D1371);
  B: V ∝ [1 − 1/(1 + x)²]·(1 + C·Ẽ′)  (the BBHL square, e^K ∝ (𝒱 + ξ/2)⁻²), via the pipeline mapping g = (1+x)² − 1
     (so g/(1+g) = B's plateau exactly; the tilt then reads C·g/λ — declared approximation).
Runs (pipeline.predict, T_R = 8.94e8, start at the deepest grid point — the D1398 DEVIATIONS D1 rule, adopted here up front):
  A0: C = 0; A1: C = 1.25e-6; A2: C = 1e-5; B0: C = 0.
Report n_s, r, α_s (D1417 estimator), N*. Rule: "E(τ,3/2) plateau viable (fixed-point scan)" if ≥ 1 run lands in the frozen band
(n_s 0.969–0.975, r 4.55–5.7e-4); "near" if within 0.003 in n_s and 30% in r; else "not viable on this scan". Expectation stated
now: approach ~ y^{−3/2} sits between α = 1/3 (y^{−1}, D1398: r 1.6e-3) and SERAPIS (y^{−2}, r 4.8e-4) ⇒ r ≈ 8e-4–1e-3 at C = 0.
No reruns to chase results; fixes only via PREREG_DILATON32_DEVIATIONS.md written first.
