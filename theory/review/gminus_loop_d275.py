"""D275 (estimate): a one-loop origin of TWIST-G-'s tilt inside the Twist. A chiral field X inside the no-scale log has physical mass
m_X^2 = |W_XX|^2/(2x) (K_XX = 1/(2x), e^K = (2x)^-3). Coupled to the stabiliser, W ⊃ (M/2) X^2 + (lam/2) S X^2, its scalars split by
+-Delta with Delta ∝ lam |F_S| ∝ sqrt(V). Coleman-Weinberg: dV = (N/64 pi^2) STr M^4 ln M^2 ≈ (N/64 pi^2) 2 Delta^2 (ln m_X^2 + 3/2) for
m_X^2 >> Delta, i.e. dV/V = c (-ln x) + const with c = N lam^2/(32 pi^2) (Delta^2 = lam^2 V up to O(1)). Matching V ∝ x^{2 gamma}:
gamma = -c/2. Order-one factors not fixed; AI-assisted."""
import math
g = -0.0085
for N in (1, 2, 4):
    lam2 = -2 * g * 32 * math.pi ** 2 / N
    print(f"N = {N}: lam^2 = {lam2:.2f}, lam = {math.sqrt(lam2):.2f}, lam^2/16pi^2 = {lam2/(16*math.pi**2):.3f}")
# check: tilt of supertrace with exact formula for a few Delta/m^2
for r in (0.01, 0.1, 0.5):
    f = lambda m2, D: (m2 + D) ** 2 * math.log(m2 + D) + (m2 - D) ** 2 * math.log(m2 - D) - 2 * m2 ** 2 * math.log(m2)
    m2a, m2b = 1.0, 2.0; D = r
    exact = (f(m2b, D) - f(m2a, D)) / math.log(2); approx = 2 * D * D
    print(f"Delta/m^2 = {r}: d STr/d ln m^2 exact {exact:.4g}, approx 2 Delta^2 {approx:.4g}")
