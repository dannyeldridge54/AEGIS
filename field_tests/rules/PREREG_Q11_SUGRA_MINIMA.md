# PREREG Q11 — compute the (m,n) supergravity minima directly; remove the "extrapolated" label from rungs ≥ 8 (locked 2026-11-20, before computing)
Setup (2201.02020 conventions): K = −3 ln(2 Im τ); W = H(τ)/η(τ)⁶, H = (j − 1728)^{m/2} j^{n/3}.
V = (2y)^{-3} |H|²/|η|¹² · [ (4y²/3) |H'/H − (iπ/2) E₂ + 3i/(2y)|² − 3 ], with H'/H = (m/2) j'/(j−1728) + (n/3) j'/j, j' = −2πi j E₆/E₄.
q-series to |q|^60. Minimise inside the fundamental domain (|τ| ≥ 1, −½ ≤ Re τ ≤ 0 by CP image), multi-start grid + Nelder–Mead.
Step 1 VALIDATION (must pass before step 2 is used): (m,n) = (1,0),(2,0),(3,0) reproduce the paper's minima −0.484+0.884i, −0.492+0.875i,
 −0.495+0.872i to |Δτ| ≤ 0.003 each. If any fails, stop: record FAIL of the code, no step 2 claims.
Step 2: for m = 1…32 (n = 0), report τ_min, |ε| = |τ − ω|, arg ε, and the ratio to the paper's formula √3·0.0145/(m + 1/16).
 RUNG-8 RULE: the extrapolation label on rungs 8–16 is REMOVED if the computed |ε| agrees with the formula within ±20% for every m = 8…16;
 otherwise the data sheet takes the COMPUTED values and the Q7/Q9 rung assignments are re-derived from them (reported, not rerun).
Step 3 (descriptive): mixed (m,n) for m,n ∈ {1,2,3}: location (arc or not), CP-violating or not.
No reruns; changes via DEVIATIONS written first.
