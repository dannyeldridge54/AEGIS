# PREREG Q2 — does the lepton Koide pattern (A = √2 ⇔ Q = 2/3, δ = 2/9) extend to quarks? (locked 2026-11-20, before computing)
Input (one scheme, fixed now): running masses at M_Z from PDG 2024 RGE (as tabulated in arXiv:2512.13630 Table II):
 u 1.29±0.20 MeV, d 2.80±0.20 MeV, s 55.7±1.3 MeV, c 0.629±0.012 GeV, b 2.794±0.034 GeV, t 169±1.1 GeV.
Compute for (u,c,t) and (d,s,b): Q = Σm/(Σ√m)², Brannen √m_k = μ(1 + A cos(δ + 2πk/3)), A = √(6Q−2)... (A² = 6Q − 2 ... from Q = (1 + A²/2)/3), δ.
Errors by Monte Carlo (Gaussian, independent, 2e5 draws, seed 1).
Rules:
- K1 PASS if Q within 2σ of 2/3 for a triplet (lepton Koide extends to it). Else FAIL.
- K2 PASS if δ within 2σ of 2/9 (mod 2π/3) for a triplet. Else FAIL.
- Only 2/3 and 2/9 are tested. Any other "nice" number noticed afterwards is post-hoc and not counted.
No reruns; changes via DEVIATIONS written first.
