# PREREG D726: does the degenerate Γ2 heavy-neutrino doublet at τ = i split linearly (cone coupling)?
Locked 2026-11-16 before computing. Script: theory/modular/cone_i_d726.py. Output: field_tests/results/cone_i_d726.txt.
## Method (fixed now)
- M_phys(τ) = (2y)·A(Y(τ)) (D597 doublet; physical factor uniform). Also the 2 ⊕ 1 at i (D690-type, W2 mixing, b = 0; c ∈ {0.3, 1, 3}).
- Degeneracy-safe Takagi (symmetric square root on degenerate blocks, as D725). P = Uᴴ ∂_y M_phys U* along the imaginary axis. Splitting rates = eigenvalues of Re P on the degenerate block; check against direct SVs at τ = i(1 + δ), δ = 1e-4, 1e-5 (1%).
- If linear: Yukawa g = rate·(M/M_model)·y√(2/3)/M_P with y = 1; m_φ = 1.9e11 GeV (D597), M/m ∈ {0.1, 0.33, 0.45}; Γ = g² m (1−4x²)^{3/2}/(16π) per diagonal channel plus off-diagonal (as D725); T_R as D725. N* shift estimate ΔN* ≈ 0.76 per decade of T_R relative to the frozen bracket (D682); n_s change ≈ 2ΔN*/N² × (1−n_s)·N/2 → use dn_s/dN* ≈ 0.0008/e-fold (D644) as the estimate.
## Decision rule
- NULL (and loop stops) if the split is quadratic (rates < 1e-6).
- If linear: correction note to D601/D602 (no retuning of the τ = i frozen bands); state whether the implied n_s (frozen band edge 0.975) and y* ≤ 25 still hold, and the effect on the AD/massless-ν1 argument.
- Fixes only via D726_DEVIATIONS.md.
