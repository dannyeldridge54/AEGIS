# PREREG D1999: is there a pattern (a Weave arrow) in the 52 known Mersenne prime exponents? (Danny 20:34). Locked before computing.
**Data:** the 52 exponents from the Wikipedia list. The rank order is verified through #51 (p = 82,589,933); #52 (p = 136,279,841) is provisional. Statistics use all 52, plus a check with 51.

**Disclosed before the lock:** I knew the Lenstra–Pomerance–Wagstaff (LPW) prediction, a mean step ln(p_{n+1}/p_n) = ln2·e^{−γ} = 0.3892, and had made a rough mental estimate of the data's mean ratio (×1.42). Both are stated here so the test cannot be tuned to them.

## A. The published model (LPW: exponents behave like a Poisson process in ln p, with rate e^γ/ln 2)
- A1. The mean log-step with its standard error, against 0.3892.
- A2. Kolmogorov–Smirnov test of the normalised steps s = Δln p / 0.3892 against Exp(1).
- A3. Count-function check: N(p ≤ x) against 2.5695·ln x + c.

## B. Weave hypotheses, each pre-registered; Bonferroni over the 6 tests (B1–B6)
- B1. **Step constant = π/8** (= 0.3927, the rung step e^{π/8}) rather than 0.3892. A power estimate is reported first. The expected verdict is **NO-POWER**: the two differ by 0.9 %, while the standard error is about 14 %.
- B2–B4. **Residues of p mod 12, mod 24 and mod 48** (χ = 48), against the residues of all primes in the same ranges. Comparison by χ² against a control distribution built from primes sampled log-uniformly over the same range.
- B5. **Arrows: memory in the steps.** Lag-1 autocorrelation of s, and a Wald–Wolfowitz runs test on sign(s − 1).
- B6. **Close pairs:** the number of steps with ratio < 1.1, against the Poisson expectation 1 − e^{−ln1.1/0.3892}, binomial.

**Numerology guard:** check.py C4 on any constant that matches.

## Verdict rule
A pattern beyond LPW is claimed only if a B test gives Bonferroni-corrected p < 0.01 (raw p < 0.00167) **and** it survives dropping the first 12 exponents (small-number effects such as p = 2, 3, 5, 7). Otherwise the verdict is that the exponents are consistent with the LPW random model, and no Weave pattern is supported.
