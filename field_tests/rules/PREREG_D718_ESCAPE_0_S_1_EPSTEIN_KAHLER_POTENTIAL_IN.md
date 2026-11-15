# PREREG D718: Escape 0<s<1: Epstein Kahler potential in the critical strip
Locked 2026-11-15 before computing. Script: theory/modular/strip_kahler_d718.py. Output: field_tests/results/strip_kahler_d718.txt.

## Question
D717's escape: for 0 < s < 1 the Laplace eigenvalue s(s−1) is negative, so K = −c ln E(τ,s) has a positive metric at the fixed points. Is E(τ,s) (analytically continued, Σ′ normalisation) positive on Re τ = ½ with its minimum at ρ, and does the constant-W0 supergravity potential V = e^K|W0|²(K^{ττ̄}|K_τ|² − 3) + V_up give a viable plateau?

## Inputs (fixed now)
- E(τ,s) = 2ζ(2s)y^s + 2√π Γ(s−½)ζ(2s−1)/Γ(s) y^{1−s} + (4π^s/Γ(s))√y Σ n^{s−½}σ_{1−2s}(n)K_{s−½}(2πny)cos(2πnx) (continuation; check against the lattice sum at s = 2 and s = 1.5 where it converges). s ∈ {0.6, 0.75, 0.9}. K = −(3α/s) ln E(τ,s) so e^K → y^{−3α} at the cusp; α ∈ {1/2, 2/3, 0.8}; V_up tunes V(ρ) = 0; D691 tilt C·Ê(τ,2) multiplying V, C ∈ {0, 1e-7, 1e-6, 1e-5, 3e-5}; N* ∈ {48.4, 49.9}. Expected before running: plateau exponent p = √(6α) < √6, hence untilted r > ~5.6e-4 — above SERAPIS-E.
- Data: none (theory). Targets as D717.

## Method
Step 1 (health): sign of E(τ,s) on 0.866 ≤ y ≤ 60 along Re τ = ½ and at i; location of the minimum; K_ττ̄ > 0 everywhere on the line. Step 2 only if Step 1 passes: canonical field, V(φ), first-order slow roll as in D717.

## Decision rule (written before running)
- VIABLE if: E > 0 on the line, minimum of V at ρ with V ≥ 0, K_ττ̄ > 0, n_s = 0.970 reachable, y* ≤ 25, |α_s| ≤ 0.009, r ≤ 1.1e-3.
- NOT VIABLE otherwise; report which step fails.
- What happens if the run crashes or times out: fixes only through D718_DEVIATIONS.md, written before any rerun.

## Labels
Mark every number in the write-up as computed / estimate / literature / from memory.
