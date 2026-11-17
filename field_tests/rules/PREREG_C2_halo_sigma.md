# PREREG C2 — Milky Way halo-star dispersions vs Jeans in MWPotential2014 (Djl C) — locked 2026-11-17
Data (quoted, Battaglia et al. 2005, astro-ph/0506102; 240 halo objects): σ_GSR ≈ 120 km/s roughly constant to r ≈ 30 kpc; for r > 40 kpc the fit is σ = −0.6 r + 132 (r in kpc); last point 50 ± 22 km/s at ~120 kpc. Per-bin errors are not in the text.
Tracer: ρ* ∝ r^−3.5 (their adopted). Anisotropy: β ∈ {0, 0.5, 0.8}. β = 0.8 is Bird et al. 2019's whole-sample value (arXiv:1805.04503), quoted.
Model: spherical Jeans σ_r in galpy's MWPotential2014 (ro = 8 kpc, vo = 220 km/s) via galpy.df.jeans.sigmar. This is the referee code D1083 showed our jeans.py matches to 1.5e-11; it is used here because the potential is non-spherical (galpy evaluates at R = z = r/√2; stated approximation).
Comparison points: r = 20 kpc (120 km/s), 50 kpc (102), 80 kpc (84), 120 kpc (50 ± 22).
Rule, set before running: with no per-bin errors, CONSISTENT if |σ_r − data| ≤ 20 km/s at 20/50/80 kpc (an a-priori tolerance, labelled) AND within 2σ (44 km/s) at 120 kpc.
Caveat: σ_GSR is a line-of-sight dispersion. It equals σ_r only far from the Sun or for β = 0; the projection is not modelled.
Reported per β: CONSISTENT/NOT. Also reported: σ_r for a 1.5× heavier halo (halo amplitude × 1.5), as the halo-mass handle for W2.
Script theory/wiring/c2_halo_sigma.py (written after this lock).
