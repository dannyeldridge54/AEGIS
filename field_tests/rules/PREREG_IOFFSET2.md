# PREREG_IOFFSET2 — supercritical or first-order split at i? Four more hidden terms (locked D1618, 2026-11-19 14:47 CT)
Follows D1612 (−κF jumps to ρ) and D1614a. Model: V_f = V₀ + s·κ·W, with V₀ the Zhinü factor (V∞ = 1) and W ∈ {F = y^{1/2}|η|²/F(i), G = E(τ,2)/E(i,2)}, s ∈ {+1, −1}; the case (F, −1) is D1612, not rerun. Cases: (F,+1), (G,+1), (G,−1).
For each case: Hessians at i; κ_c where the smallest eigenvalue of Hess(V_f)(i) crosses 0 (bisection), with its eigen-direction (x or y); then for κ/κ_c ∈ {1.001, 1.01, 1.1, 1.5} the minimum found by Nelder–Mead from i + 1e-3 along the unstable direction. Report |u| = |τ − i|/|τ + i|, whether it is on a CP line, and V(min) − V(ρ).
Classification: SUPERCRITICAL if |u| grows continuously from 0 (|u|(1.001) < 0.05 and |u| increasing with κ) with V(min) < V(ρ); FIRST-ORDER if the minimum jumps (|u|(1.001) > 0.1) or ρ is lower; NO-SPLIT if κ_c does not exist.
Script: field_tests/scripts/ioffset/run2.py
