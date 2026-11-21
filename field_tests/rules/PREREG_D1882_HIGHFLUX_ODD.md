# PREREG D1882 — reverse thread via a higher-flux pyramid odd mode (locked 21 Nov 2026 before computing; repo at d7ea4f96)
Same set-up as D1873 (τ = i, corner discs r = 𝒱^{-1/6} = 0.171 around the 4 Z₂ fixed points, 300² grid, s = ⟨|ψ|²⟩_discs / ⟨|ψ|²⟩_cell), flux M ∈ {4, 6, 8, 12}.
For each M the thread mode is the BEST odd mode: the lowest generalised eigenvalue of (disc Gram matrix, cell Gram matrix) on the odd subspace spanned by (ψ^j − ψ^{M−j})/√2 — i.e. the most corner-avoiding odd combination available (this is the most favourable case for U27).
Verdict: PASS if any M gives s_min < 4.3e-3; PARTIAL if 4.3e-3 ≤ s_min < 1/80; FAIL otherwise. Also report r = 0.10.
