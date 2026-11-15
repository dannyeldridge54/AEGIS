# PREREG D647: modular-covariant completion of the SUSY-breaking sector (W0 → W0·η(τ)^{-2})
Locked before computation, 2026-11-15. Script theory/modular/covariant_w_d647.py; output results/covariant_w_d647.txt.
Motivation: the paper's chain (D584, D639, D643) uses constant W0 (as in Kallosh–Linde 2408.05203), which has no modular weight, so G = K + ln|W|² is not SL(2,Z) invariant. The minimal invariant completion for K = −ln(2 Im τ) is W = W0 η(τ)^{-2} (weight −1), giving G = −ln(2y|η|⁴) + ln|W0|² = L(τ) + const.
Claims to compute:
1. G_τ at τ = i and τ = ρ for W = W0 η^{-2} (numerical, mpmath): expect 0 (L stationary at both fixed points). Compare constant W0: G_τ(i) = K_τ = i/2 (non-zero).
2. Consequences (analytic, given 1): F_τ = e^{G/2}G^{ττ̄}G_τ̄ = 0 at the vacuum → the inflaton carries no SUSY breaking; (a) the inflaton→gravitino F-term channel of D584 vanishes at leading order, so m3/2 > m_φ/2 is no longer required; (b) visible soft masses m_Q² = m3/2² + V0 for every matter weight k (no F_τ cancellation) — compute m_Q²/m3/2² for k = 0, 1 by finite differences in this covariant set-up with S (f² = 2|W0|²e^{…} so V0 = 0); (c) A-terms: still 0 at i by D646.
3. Report m3/2 at τ = i for W0 = 1: e^{G/2} = |η(i)|^{-2}/√2.
Verdict: if G_τ(i) = 0, the paper must state that its gravitino/soft-mass chain refers to the constant-W0 embedding and that the covariant completion gives a different chain (no inflaton F-term; soft masses ~ m3/2 with m3/2 free). No reruns; fixes via DEVIATIONS first.
