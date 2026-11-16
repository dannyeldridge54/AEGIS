# PREREG D795: canonical Hessian of the two-term τ = i potential at τ = i (Jl tick 34)
Locked before computing, 2026-11-16.
Potential: V = I²/(I²+1) + ε I₁ (paper eq. twoterm), ε = 1.45e-4. Kähler metric K = −3 ln(2 Im τ), so g = 3/(4y²) in both directions.
Compute: (a) by finite differences on mpmath kleinj (j = 1728·kleinj), at step sizes h = 1e-3 and 1e-4, the second derivatives V_xx and V_yy at τ = i; ratio R = V_xx/V_yy. (b) The angular dependence of V on the circle |τ − i| = δ for δ = 0.01, 0.03, 0.1: A(δ) = (max − min)/mean.
Prediction (pre-stated): since V depends on τ only via |j − 1728| and j − 1728 is even in z = (τ−i)/(τ+i) with a double zero, R = 1 to numerical precision and A(δ) ∝ δ² (anisotropy first at quartic order). This would falsify D794 step 4's [estimate] "Δm ≠ 0" for this potential.
Verdict rule: |R − 1| < 1e-3 → isotropic (D794 step 4 corrected); otherwise anisotropic. A(0.1)/A(0.03) in 8–14 → δ² scaling confirmed.
No reruns; any fix goes in DEVIATIONS first.
