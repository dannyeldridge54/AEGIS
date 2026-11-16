# PREREG D831 (P3.4): T²-shape of the anti-D3 interaction at the D830 placement
Locked before computing, 2026-11-16.
Placement (D830): anti-D3 stuck at an O3 point displaced in T⁴, projecting to T² point z_a ∈ {0, ½}. D3s (N, N0) = (5, 2): 5 at each half-period, 2 at origin. O3s: 4 units per T² fixed point (16 total).
Physics: k = 0 (T⁴ zero-mode) part of the 6D compact Green's function gives (1/Vol₄)·G(Δz,U); for Δz = 0 the T⁴ displacement regularises it to Δ(U) + const(d) up to e^{−2π R₂/R₄} corrections. Weights: anti-D3–D3 attract (NS+RR) with +2, anti-D3–O3 repel with −2 per unit. V(z_a,U) = −2κ[Σ_j N_j G̃(z_a−z_j) − 4 Σ_k G̃(z_a−z_k)], κ > 0.
Compute (same G, Δ as D829 script) at U = i, ρ, ½+iy (y = 2, 5, 10, 20):
 B(0) = Σ_j N_j G̃(−z_j) − 4(Δ + S),  B(½) similarly.  V = −2κB (report B, and the slope dB/dy at y = 10→20).
Prediction (pre-stated): B(0) ≈ −2Δ + const, B(½) ≈ Δ − 3G(½) + const; both ∝ −(2π/3)y at large y, so V = +(4π/3)κy: a rising WALL, not a plateau.
Size criterion [derived]: added slope must stay below the plateau slope, |V_add'|/V0 ≲ √(2ε) ≈ 1.7e-2 (ε = 1.4e-4), with d/dφ = √2·d/d(ln y)·... giving κ/V0 ≲ 1.7e-2/(√2·(4π/3)·y*) = 2.9e-3/y*.
