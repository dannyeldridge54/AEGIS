# PREREG D684: can the covariant F-term itself be the tilt + vacuum mass (an origin for ε)? (Danny: "Origin of ε")
Locked before computation, 2026-11-15. Script theory/modular/fterm_tilt_d684.py; output results/fterm_tilt_d684.txt.
Model (covariant completion D647, no ad-hoc εI1 term): V/V0 = I²/(I²+1) + R·f(y), with f(y) = e^{L(iy)−L(i)}·4y²|∂_τL(iy)|² (D648) and R = m3/2²/(3H²) (V0 = 3H²M_P²). Field along τ = iy, φ = ln y/√2.
Compute:
1. Near i: f ∝ |δ|² (quadratic → massive vacuum)? Fit the exponent of f vs |δ| for δ = 1e-2…1e-4. Report m²/H² = 3R·f''(φ) at the vacuum.
2. Exact first-order slow roll (∫V/V′ from ε_V = 1, mpmath, as D669): for R on a log grid (1e-16 … 1e-10) and N* ∈ {46.08, 49.21}: y*, n_s, r, α_s. Find R giving n_s = 0.9682 (CMB) and 0.9728 (CMB+DESI); report y*, r, α_s there and the implied m3/2 = √(3R)·H with H_inf = 3.7e12 GeV (estimate).
Verdict rules (fixed now): VIABLE as an origin of the tilt if some R gives n_s within 0.965–0.975 with y* ≤ 25 and |α_s| ≤ 0.009 (current 2σ-ish bound, Planck-like σ ≈ 0.0067 around −0.0045, labelled approximate). Then state the implied m3/2 and its consistency with D650's superpartner window (gaugino masses would need X-dependent gauge kinetic functions if m3/2 is ~10–100 TeV). NOT VIABLE otherwise. No tuning beyond R.
