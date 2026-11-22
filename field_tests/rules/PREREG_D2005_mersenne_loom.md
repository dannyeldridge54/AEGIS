# PREREG D2005: Mersenne Loom. Layered prime sieve with nodes and a central referee. Locked before code and runs.
**Why this shape.** D1999 and D2004 found that the exponents carry no digit or vortex pattern beyond "p is prime". So the optimal setup uses the one structure that is real. Any factor q of 2^p − 1 (p an odd prime) must be q = 2kp + 1 with q ≡ ±1 (mod 8). That is the layer law, and each sieve layer is a rung. This is the published GIMPS pipeline, rebuilt as Loom nodes.

**Nodes (outer to inner):**
- **N1, exponent sieve:** p must be prime.
- **N2, trial-factor layers:** test q = 2kp + 1 with q ≡ ±1 (mod 8), one bit-level per layer (2^b to 2^(b+1)), up to the depth set by p: b_max = min(64, 16 + ⌊2·log₂ p⌋).
  - Expected (heuristic): a factor in layer b appears with probability ≈ 1/b.
- **N3, P−1 stage 1:** bound B1 = 10⁴. Finds factors q where q − 1 = 2kp × (B1-smooth part).
- **N4, PRP test:** base 3, 3^(M_p − 1) ≡ 1 (mod M_p). This is the candidate detector.
- **Referee (centre):** an independent Lucas–Lehmer test on every N4 survivor **and** on 5% of N2/N3 eliminations (spot-check: the reported factor must actually divide M_p). A find is accepted only if N4 and the LL test agree. Any disagreement is logged as an engine fault.

**Calibration (pass/fail, fixed now).** Run on all primes p ≤ 12,000. The output must be exactly the 23 known exponents ≤ 12,000: 2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213.
- Sensitivity = 1, specificity = 1.
- 0 referee disagreements.
- 0 bad factors.
- (p = 2 is handled directly, since M_2 = 3.)

**Reported (not pass/fail):**
- elimination rate per layer vs the 1/b heuristic;
- work saved by N2 + N3, as the fraction of exponents removed before N4;
- seconds per node.
