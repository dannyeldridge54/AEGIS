# PREREG N3 — third-order (N3LO) slow-roll n_s vs exact MS (large list 6)
Locked 2026-11-17 18:10 CT before any N3 number.
Source (fetched via WebFetch, arXiv 2205.12608v2, Auclair & Ringeval, App. C, δ_i = 0): ε_{i+1} = d ln|ε_i|/dN, ε_1 = −d ln H/dN, C = γ_E + ln 2 − 2.
n_S − 1 = n^(1) + n^(2) + n^(3): n^(1) = −2ε1 − ε2; n^(2) = −2ε1² − (2C+3)ε1ε2 − Cε2ε3;
n^(3) = −2ε1³ + (π² − 6C − 15)ε1²ε2 + (1/12)(7π² − 12C² − 36C − 84)ε1ε2² + (7π²/12 − C² − 4C − 6)ε1ε2ε3 + (1/24)(π² − 12C²)ε2ε3²
        + (π²/4 − 2)ε2²ε3 + (1/24)(π² − 12C²)ε2ε3ε4.
CAVEAT (recorded before running): the fetch tool reported the text extraction of the last three terms as typographically ambiguous; this test is ALSO a
numerical check of those coefficients.
ε_i evaluated at the pivot (k* = aH, N_p = N_end − N*) from the exact background: ln ε1(N) fitted by a degree-12 Chebyshev polynomial on 41 Chebyshev
nodes in [N_p − 1.5, N_p + 1.5], derivatives analytic. Fit check: degree 10 vs 12 must change n^(3)-order n_s by ≤ 1e-8 (else point listed).
Points: the 16 scored J7m points (TI ×6, SFI p=3 ×2, N* = 50, 60), exact n_s from tools/serapis_calc/ms.spectra_fast with J7b settings (9 k on [−1, 1], bd 1000).
Errors: Δ2 = |n_s(2nd order) − exact|, Δ3 = |n_s(3rd order) − exact|.
Claim N3: median Δ3 ≤ median Δ2 / 3 AND Δ3 < Δ2 on ≥ 12/16 → "N3LO n_s CONFIRMED (coefficients consistent)". Otherwise "NOT CONFIRMED" (either the
coefficients as extracted are wrong, or the exact reference's precision (~1e-7, polyfit leakage of β_s) hides the third order) — reported, no reruns to chase.
Reported only: the same with a narrower exact fit (9 k on [−0.25, 0.25]).
