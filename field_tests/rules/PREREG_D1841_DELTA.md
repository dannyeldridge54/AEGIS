# PREREG D1841 — can δ = 2/9 be a residual-charge phase? (locked 21 Nov 2026 before computing; repo at 15a732ef)
Koide phase δ from PDG masses (m_e, m_μ, m_τ = 0.51099895, 105.6583755, 1776.93 ± 0.09 MeV), with its 1σ error from m_τ.
A residual-charge (Z_n ⊂ metaplectic/stabiliser) phase is δ = 2πk/n (mod 2π/3, since the circulant shifts δ by 2π/3), n ≤ 60.
Test: any k/n with |2πk/n − δ| ≤ 2σ_δ (mod 2π/3). Chance: the fraction of uniform random δ′ in [0, 2π/3) hit by some 2πk/n (n ≤ 60) within 2σ_δ = p. Verdict: SUPPORTED only if a hit exists with n ≤ 12 AND p < 0.01; otherwise NOT SUPPORTED (δ = 2/9 rad is then "rational in radians", which no residual charge gives).
