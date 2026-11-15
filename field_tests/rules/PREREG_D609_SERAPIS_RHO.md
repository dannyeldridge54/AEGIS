# PREREG D609: SERAPIS-ρ, a string-natural variant with the vacuum at the hexagonal torus, locked before computing

Model (α = 1/3, post-hoc; scored only on future data):
- V = I_ρ²/(I_ρ² + 1) + ε·(L − L(ρ)).
- I_ρ = (1/4π)ln(1 + |j|²/1728²): KL's L_j, zero at ρ.
- L = −ln(2y|η|⁴): the DKL/species threshold function, an isotropic minimum at ρ (Hessian 0.667, D608).

Path: inflation along Re τ = 1/2 from the cusp down to ρ = 1/2 + i√3/2 (on this line j and q are real, q = −e^{−2πy}).

Checks:
- V(ρ) = 0 and the Hessian at ρ is positive and isotropic (finite differences at ρ in x and y).
- V(i) > 0, i.e. i is not the vacuum.

Inflation:
- The D564/D575 slow-roll machinery along y on the x = 1/2 line, canonical φ = ln(y)/√2.
- Apply the D588 offset Δn_s = −0.0003 and Δy* = −0.4.
- ε ∈ {1e-4, 3e-4, 1e-3}; N* ∈ {47, 50, 53} (reheating not modelled; span stated).

Report: y*, home-safe (≤ 25), n_s, r, σ vs SPA and SPA+DESI, vacuum m/H.

Verdict: SERAPIS-ρ is VIABLE if some ε gives n_s within 2σ of SPA+DESI with y* ≤ 25 for all three N*. Credit: Kallosh–Linde (vacuum at ρ, 2408.05203) and DKL/Casas–Ibáñez (threshold function).
Fixes go in PREREG_D609_DEVIATIONS.md, written first.
