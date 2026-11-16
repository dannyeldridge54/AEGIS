# PREREG D741: neutrino ordering and lightest mass from the D664 2 ⊕ 1 Weinberg texture
Locked 2026-11-16 before computing. Script: theory/modular/ordering_d741.py. Output: field_tests/results/ordering_d741.txt.
## Texture (fixed now; D664)
m_ν ∝ [[A(Y), bY],[bYᵀ, 0]] at τ = i (Y = D597 weight-2 doublet), b complex: |b| on a log grid 0.01–100 (400 points) × arg b in 24 steps. Same matrix at ρ as a cross-check (the weight bookkeeping at ρ differs, D661; stated).
## Outputs
Light masses = singular values, sorted m_a ≤ m_b ≤ m_c. Δ_lo = m_b² − m_a², Δ_hi = m_c² − m_b². NO-like if Δ_lo < Δ_hi (the close pair is lightest), IO-like otherwise; R = min(Δ)/max(Δ). Observed R_obs = Δm²₂₁/Δm²₃₁ = 0.0297 (±10% band).
Report: fraction NO/IO over the grid; the points with R within ±10% of R_obs, their ordering, and their m_lightest/m_heaviest. Implied Σm_ν for those points: scale so the large splitting equals 2.5e-3 eV².
## Decision rule
- CONSISTENT with frozen Σm_ν (lock D605) if some R-matching points are NO with Σm_ν ≤ 0.064 eV.
- TENSION if all R-matching points are IO, or NO only with Σm_ν > 0.064 eV (DESI DR2+CMB) → correction note; frozen stays frozen.
- NULL if no grid point matches R_obs.
- Fixes only via D741_DEVIATIONS.md.
