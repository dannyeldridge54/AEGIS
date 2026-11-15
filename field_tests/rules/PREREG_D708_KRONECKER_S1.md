# PREREG D708: the s = 1 (Kronecker / species-scale) rung of the Epstein plateau ladder
Locked 2026-11-15 before computing. Motivation: D707 found the species scale naturally carries the s = 1 object −log(Im τ |η(τ)|⁴) (Kronecker limit of E(τ,s) at s → 1), not E(τ,2).
Script theory/modular/kronecker_s1_d708.py (D702 script with the plateau swapped).
Model: F(τ) = −log(y|η(τ)|⁴) + κ, η by q-product; V/V0 = [1 − F(ρ)/F(τ)]·(1 + CÊ2), same BHK tilt, same canonical map y = e^{√2φ} on x = ½, same H.
κ is scheme-dependent (the regularised E(τ,1) constant) → pre-registered κ ∈ {0, 2}, both reported, no tuning.
Checks: η(i) vs Γ(1/4)/(2π^{3/4}) to 1e-10; F minimal at ρ (vs ρ+0.05, ρ+0.05i, i).
Grid: C ∈ {0, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5}, N* ∈ {48.4, 49.9}; interpolate n_s = 0.970.
Expectation (D701 index rule, e = 1, before running): r ~ 1e-3 or more, i.e. above the SERAPIS cap r ≤ 8.3e-4.
Viability rule as D700: n_s = 0.970 reachable, y* ≤ 25, |α_s| ≲ 2e-3, r ≤ 8.3e-4. Fails any → NOT VIABLE.
