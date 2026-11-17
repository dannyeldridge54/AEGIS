# PREREG S4d — scalar (dilaton + metric) stability of our subcritical 6D tadpole vacuum (S4b, D1015/D1015a)
Locked 2026-11-17 before any S4d number. Source [fetched, arXiv 2209.10553 §5.1, Basile–Thomée–Raucci — the same paper and conventions as our background]:
master equation (5.3) □A + (D−2)(3Ω′ − e^{2Ω}V₀′/(4φ₀′))A′ − 2(D−3)e^{2Ω}(V₀/(D−2) + (D−2)Ω′V₀′/(8φ₀′))A = 0; Schrödinger form H = b + 𝒜†𝒜 (5.4–5.8),
b = 2(D−3)e^{2Ω}(V₀/(D−2) + (D−2)Ω′V₀′/(8φ₀′)) (5.9); with V₀′ = γV₀ > 0, b ≥ 0 ⇔ Ω′/φ₀′ ≥ −8/(γ(D−2)²) (5.10) — sufficient for m² ≥ 0.
The source shows (5.10) for critical/supercritical cases only; our case is SUBCRITICAL (δ = −0.0528), not covered — that is the test.
Cross-check of the transcription (done, recorded here): at D = 10 the coefficients 3(D−2) = 24, (D−2)/4 = 2, 2(D−3)/(D−2) = 7/4, 2(D−3)(D−2)/8 = 14 equal
Basile–Mourad–Sagnotti 1811.11448 Eq. 5.33 term by term.
Test: Ω = A(y) (warp of the flat directions, gauge B = −γφ/2 as in S4b), φ₀ = P(y); the ratio Ω′/φ₀′ is coordinate-independent. Evaluate R(y) = A′/P′ on 4000
points of (1e-6, 1 − 1e-6)·y_end with 40-digit arithmetic; threshold −8/(γ(D−2)²) = −1/4 for D = 6, γ = 2.
Claim: R(y) ≥ −1/4 everywhere → SCALAR SECTOR STABLE (sufficient condition holds). Else: report where it fails; stability then UNDECIDED by this test
(b < 0 somewhere is not an instability by itself) and the next lock computes the lowest eigenvalue. Results: field_tests/results/s4d_scalar.txt.
