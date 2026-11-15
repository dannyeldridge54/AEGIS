# PREREG D515 — fully modular Twist, first test (Danny 21:32 CT "Set this up"; roadmap step A), locked before computing.
Toolkit theory/modular/modular_lib.py (selftest: j(i) = 1728, j(ρ) = 0, SL(2,Z) invariance of ln V to 4e-14; results/modular_selftest.txt).
Model: K = −3 ln(2 Im τ), W = S·η(τ)^−6 H(j), V = |H(j)|²/((2 Im τ)³|η|¹²) (exactly modular). Minimal family chosen BEFORE computing:
  H(j) = (j − 1728)^a · j^b · [ln(j/1728)]^{3/2}, with b = −¼ − a (so V → constant on the cusp: the plateau), a ∈ {½, 1, 3/2}.
  Built-in consequences (by construction): V(i) = 0 (square torus = Minkowski vacuum; Λ must come from a separate small term, NOT addressed here); j^b with b < 0 makes the hexagon/triangle
  point ρ a wall (V → ∞).
Tests along Re τ = 0 (inflaton y = Im τ, canonical φ = √(3/2) ln y), inflation on the cusp plateau rolling toward τ = i: end of inflation ε = 1, N* = 58.09: report n_s, r, α_s per a.
Verdicts per a: "VIABLE" if n_s within 2σ of CMB-SPA (0.9684 ± 0.0030) or CMB-SPA+DESI (0.9728 ± 0.0027) and r < 0.036; else "NOT VIABLE". Report all; no tuning of a beyond the three values.
