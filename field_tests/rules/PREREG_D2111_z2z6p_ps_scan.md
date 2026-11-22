# PREREG D2111: Seed v6 outward scan on Z₂×Z₆′ AAA (η = −1), Pati–Salam. Locked before running. Engine: z2z6p.py as validated in D2110.

**Space**
- Bulk SUSY wrappings with |n|, |m| ≤ 3 and coprime per torus. Y = 0 and t = 2X + Y > 0, giving t ∈ {2, 6, 14, 26, 38}.
- Fractional data per stack: Z₂ eigenvalues (t₃ = t₁ + t₂ mod 2; 4 choices) × τ ∈ {0,1}³ × σ ∈ {0,1}³, so 256 variants.

**Visible sector:** a (N=4), b (N=2), c (N=2) on the **same bulk wrapping**. This matches Table 27 and gives the equal-volume tree-level unification hint from D2108. The bulk budget forces t = 2, which uses 16 of the 32.
- Every visible stack must be distinct from its own orientifold image, so it is U(N) and not USp/SO.
- Family condition: χ(a,b) + χ(a,b′) = ±3, and χ(a,c) + χ(a,c′) = ∓3 (opposite sign).

**Hidden sector:** at most 2 stacks, any wrapping with t ≤ 14, N ≥ 1, with Σ N t = 16.
- All 24 twisted RR residuals must be 0, along with the bulk total of 32.
- Both (j,k) orderings P1 and P2 must pass, per the D2110 rule.

**Built-in positive control:** the scan must rediscover the Table 27 model (a, b, c, d, e as in D2110). If it does not, the scan is broken and no result is used.

**Reported, not filtered:**
- the χ(x,x′) self-image intersections, flagged as possible sym/antisym exotics (the O6 term is not implemented);
- the visible–hidden chiral total;
- the number of distinct spectra.

**Verdict:**
- A = count of globally consistent 3-family PS models (raw and distinct spectra).
- PASS if the control is found. A ≥ 2 distinct means v6 has a landscape to rank by α_s, done next under D2112 after the gauge-kinetic formula is written down from the paper.
- Run on 2 cloud cores (sharded over the visible wrapping list), with no PC.
