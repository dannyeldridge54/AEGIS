# PREREG D835 (K.4): the anti-D3 term added to SERAPIS-E; exact MS
Locked before computing, 2026-11-16.
Potential on the inflaton line x = ½: V/V0 = P_E(1 + CÊ) + 4k[Δ(U) − Δ(ρ)], with Δ(U) = −ln(y|η(U)|⁴) and k = κ/V0.
(Derivation: for z_a = 0 with stacks (5, 2) and O3 weight 4, B = −2Δ + S, S = −2 ln 2 (D829, D831); V_add = −2κB; shifted so V(ρ) = 0. Check: B(i) = −3.4957 (D831).)
Code: D692 script and MS solver (running_d632 lines 12–41, start y = 25) with V replaced as above; ln|η|⁴ = −πy/3 + 4Σ_{n≤30} ln|1 − q^n|, q = e^{2πiU}.
Runs: C = 1.0e-6 (D692 band row); k = 0, 0.5e-4, 1e-4, 2.07e-4; N* = 48.4, 49.9. Report y*, n_s, r, α_s.
Checks: (i) k = 0 reproduces D692 (n_s 0.9701 / 0.9715, r 4.754e-4 / 4.551e-4) to 1e-4; (ii) (a) ratio V_add/(V0·CÊ) at y* and y = 25: is the anti-D3 wall smaller than the BHK rise; (iii) sign of ∂²_x V_add at x = ½, y = y* (stable iff > 0).
Verdict rule: "harmless" iff |Δn_s| ≤ 0.001 and |Δr/r| ≤ 10% at k = 2.07e-4 for both N*.
Prediction (pre-stated): at k = 2.07e-4 the anti-D3 term adds a slope ≈ 4k·(π/3)·√2 ≈ 1.2e-3 to V'/V at y*, comparable to the BHK slope; Δn_s ≈ +0.003–0.006 (redder→bluer), i.e. NOT harmless at the maximum, harmless at k ≲ 0.5e-4. (D831's bound was an order-of-magnitude slope criterion.)
