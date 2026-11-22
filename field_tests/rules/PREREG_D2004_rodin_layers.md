# PREREG D2004: Mersenne exponents as a decimal "dimensional ladder", with Rodin digit rules as filters. Locked before code and runs.
**Idea (Danny, 21 Nov 2026).**
- Split each Mersenne exponent p into decimal layers (ones, tens, hundreds, …). Each layer is a rung.
- Use Rodin "vortex math" digit counting **as a filter, not as math**:
  - the digital root (p mod 9);
  - the doubling circuit 1-2-4-8-7-5;
  - the 3-6-9 axis.
- Question: does any filter keep the real Mersenne exponents more often than it keeps ordinary primes of the same size? A filter that does could rank GIMPS candidates.

**Data.** The 52 known exponents, 2 … 136,279,841 (same list as D1999).

**Baseline.** For each p, 400 random primes drawn uniformly from [p/2, 2p] (sympy.randprime, seed 2004). For p < 50 the range is [2, 100]. Every filter is scored as Mersenne pass rate vs baseline pass rate on matched magnitudes.

**Filters and tests (fixed now):**
| filter | rule | test |
|---|---|---|
| R1 | digital root of p is on the doubling circuit {1,2,4,5,7,8} | pass rates (calibration: every prime > 3 passes) |
| R2 | position on the circuit: digital root of p in each of 1,2,4,8,7,5 | χ², Mersenne counts vs baseline proportions (df 5) |
| R3 | digital root of 2^p − 1 (Rodin root of the number itself) | χ² vs baseline (df ≤ 5) |
| R4 | count of layers whose digit is 3, 6 or 9 (the "axis"), per number | Mann–Whitney U, Mersenne vs baseline, as fraction of layers |
| R5 | count of layers whose digit is on the circuit | same test |
| L1 | leading-digit layer vs Benford's law (the scale-invariant "fractal" law expected for geometric growth) | χ² (df 8), and the same against baseline primes |
| L2 | each lower layer (2nd, 3rd, … digit) uniform | χ² per layer, layers with ≥ 20 numbers |

- p < 10 has only one layer and is used only where it has one.
- **Significance:** Bonferroni over all tests run (R2, R3, R4, R5, L1-vs-baseline and each L2 layer). α = 0.05 / m.
- **Expected by known maths, stated now:**
  - R1: every prime > 3 passes, so the filter has no power.
  - R3: 2^p mod 9 depends only on p mod 6, so for prime p > 3 the digital root of M_p is 1 or 4, set by p mod 6. That makes R3 equivalent to a p mod 6 test.
  - L1: Benford should fit if growth is geometric (D1999).
- **Verdict:** a filter is useful only if it passes Bonferroni **and** its pass rate beats the baseline. Otherwise it is null and is not used for targeting.
