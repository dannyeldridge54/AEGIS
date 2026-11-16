# PREREG D796: isotropy and Z₃ breaking of the SERAPIS-E potential at ρ (Jl tick 35)
Locked before computing, 2026-11-16. Code: the potential V(x,y) of theory/modular/inflaton_ad_d790.py (C = 1.15e-6), imported unchanged.
(a) R = V_xx/V_yy at ρ by central differences, h = 1e-3 and 1e-4 (metric conformally flat → canonical ratio = R).
(b) On z-circles, z = (τ−ρ)/(τ−ρ̄), τ(z) = (ρ − ρ̄z)/(1−z), r = |z| ∈ {0.01, 0.03, 0.1}, 96 angles: Fourier amplitudes c_k = |V̂_k|/V̂_0 for k = 1..6.
Predictions: |R−1| < 1e-3 (Z₃ forces isotropy); c1, c2, c4, c5 below 1e-6 at all r (forbidden by Z₃ + CP); c3 ∝ r, so c3(0.1)/c3(0.03) in 2.8–3.9; c6 ∝ r².
Verdict: all four hold → Z₃ structure confirmed (K4 of D777/D790). Any failure → report and analyse; no rerun.
