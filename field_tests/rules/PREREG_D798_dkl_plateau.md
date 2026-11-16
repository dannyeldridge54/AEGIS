# PREREG D798: a one-loop (DKL-threshold) plateau with its vacuum at ρ (Jl tick 37)
Locked before computing, 2026-11-16.
Δ(τ) = −ln(y|η(τ)|⁴) (Dixon–Kaplunovsky–Louis threshold), Δ̃ = Δ − Δ(ρ). Kähler metric −3 ln(2y).
Models: V_p = Δ̃^p/(Δ̃^p + 1), p = 1, 2.
Compute:
(a) min of Δ on a 60×60 grid of the fundamental domain (x ∈ [−½, ½], |τ| ≥ 1, y ≤ 3) and its location;
(b) Hessian ratio V_xx/V_yy at ρ for p = 1 (h = 1e-4);
(c) single-field slow roll along x = ½ (the CP line from ρ to the cusp; check that ∂_x V = 0 there numerically), canonical φ = √(3/2) ln y: ε, η from V(y); end at ε = 1; n_s, r at N* = 50 and 55.
Pre-stated expectations (leading-order α-attractor reasoning: Δ ≈ πy/3, so V_p ≈ 1 − c y^{−p} = 1 − c e^{−p√(2/3)φ}):
- (a) min at ρ;
- (b) R = 1 ± 1e-3 for p = 1 (Z₃), while p = 2 has a massless quartic vacuum;
- (c) p = 1: n_s ≈ 1 − 2/N, r ≈ 12/N² (≈4.8e-3 at N = 50); p = 2: r ≈ 3/N² (≈1.2e-3), both ABOVE the family strip (r ≈ 3–6e-4).
Verdict: if (c) holds, the DKL plateau is a viable one-loop plateau shape only with r ~ 1e-3–5e-3, distinct from SERAPIS. Report either way; no reruns.
