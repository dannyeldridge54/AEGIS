# PREREG D575: two-term SERAPIS (plateau + E₆ mass term), locked before computing

Model (post-hoc; scored only on future data):
- V/V₀ = I^p/(I^p + 1) + ε·I₁, with p = 2.
- I = (1/4π) ln(1 + |j − 1728|²/1728²) (D545) and I₁ = (1/4π) ln(1 + |j − 1728|/1728) (D574).
- α = 1/3 kinetic term.

Scan: ε ∈ {1e-4, 3e-4, 1e-3, 3e-3}, all four reported. No ε is selected or called "best".

For each ε and N* ∈ {52, 55.6}, report:
- y_end, y*, home-safe (y* ≤ 25), n_s, r, with distances to SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027);
- the vacuum curvature exponent (slope of log(V − V(i)) against log|δ|, expected 2);
- m/H_inf, with H_inf² = V(y*)/3.

Method: the D564/D574 inflation code, with lv(u) = ln(plateau + ε·I₁y). The end of inflation is ε_H = 1.

Verdict rule: the trade-off from D574 is broken if some ε gives a quadratic vacuum, y* ≤ 25 and n_s within 3σ of both data sets. Otherwise it is not broken. Fixes go in PREREG_D575_DEVIATIONS.md, written first.
