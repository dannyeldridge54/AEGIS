# PREREG D648: upper bound on m3/2 from the covariant F-term potential (follows D647)
Locked before computation, 2026-11-15. Script theory/modular/m32_bound_d648.py; output results/m32_bound_d648.txt.
With W = (W0 + fS)η^{-2}, |G_S|² = 3: V_F(τ) = e^{G}G^{ττ̄}|G_τ|² = m3/2(i)²M_P² · e^{L(τ)−L(i)} · 4y²|∂_τL|² (L = −ln(2y|η|⁴)), which grows like e^{πy/3} toward the cusp and is zero at i.
Compute along τ = iy (y = Im τ, canonical φ = ln y/√2), with V_pl = 3H²M_P²·[I²/(I²+1) + εI1] (ε = 1.3e-4, 1.6e-4):
- f(y) = e^{L(iy)−L(i)}·4y²|∂_τL(iy)|²; ratio R(y*) = (m3/2²/3H²)·f(y*)/[V_pl/3H²M_P²] and the induced Δη = d²(V_F)/dφ² / V_pl, Δε_V via first derivative, at y* = 23 and 24.5.
- Bound: largest m3/2/H with |Δn_s| = |2Δη − 6Δε_V + …| < 1e-3 (a third of the current σ(n_s)) at both y*. Convert with H_inf = 3.7e12 GeV (D584/D586 value; estimate).
Report f(y*), the bound on m3/2/H and on m3/2 in GeV. No tuning; DEVIATIONS first.
