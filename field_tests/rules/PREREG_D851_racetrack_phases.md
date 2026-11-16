# PREREG D851 (Q.1, deep): phase distribution over CP-odd racetrack minima
Locked before computing, 2026-11-16.
Model and grid exactly as PREREG_D845 (W = W0 + e^{2πiT/N1} + B e^{2πiT/N2}, real W0, B; K = −3 ln; 5 ≤ N1 < N2 ≤ 10; W0 ∈ {±1e-4, ±1e-3, ±1e-2}; B ∈ {±0.5, ±1, ±2}; grid 400×400 on s ∈ [0, L), t ∈ [1, 60]; Nelder–Mead refinement; positive-definite Hessian; t ∈ (1, 60)). New script (D845's is not rerun).
Outputs:
(a) For every CP-odd minimum with t > 2: θ₁ = 2π s/N1 and θ₂ = 2π s/N2 (mod 2π). Fractions with |sin θ| > 0.1 and > 0.5, for θ₁, θ₂ separately; histogram of |sin θ₁| in 10 bins.
(b) Per parameter point: is the DEEPEST minimum found CP-odd? Fraction of points. For points whose deepest minimum is CP-even, the median ratio V_odd,best / V_even,best (depth ratio, AdS).
(c) Robustness: for every 10th parameter point, repeat with a 700×700 grid; report the number of CP-odd minima at both resolutions (agreement = same count).
(d) Uplift probe: add a constant uplift ΔV = |V_even,deepest| (lifting the deepest CP-even minimum to ~0) and ask whether CP-odd minima remain local minima (they do, a constant does not change the Hessian) and their sign of V after uplift (dS/AdS). Report the fraction of CP-odd minima that become dS (V > 0) under that uplift.
Comparison: P1's old prior had 6% mass at |sin δ| < 0.1 (D763), i.e. 94% at |sin δ| > 0.1.
Verdict rules: P1′ reproduces P1's phase support iff the fraction with |sin θ₁| > 0.1 ≥ 0.8 AND (b) shows CP-odd deepest minima in ≥ 20% of points; otherwise P1′ needs vacuum selection to be argued (metastability).
Prediction (pre-stated): (a) passes (phases generic); (b) fails (CP-odd minima mostly metastable, ≤ 20%).
