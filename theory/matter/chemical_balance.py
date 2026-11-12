"""Development 2: how much of the axial (spin) source becomes lepton number. Chemical equilibrium of the Standard Model
at T ~ 2e13 GeV with the Twist source mu_A = c_A phidot / M_P acting on each Weyl fermion with sign -1 (left-handed)
and +1 (right-handed). AI-assisted; assumptions stated in the doc.
In equilibrium at this temperature: gauge interactions, the top Yukawa, the Weinberg operator (lepton number),
strong sphalerons (borderline). Not yet: electroweak sphalerons (so B is conserved, B = 0), the other Yukawas
(so e_R carries no asymmetry and light-quark chiral numbers are conserved apart from strong sphalerons).
A process is in equilibrium when the sum over its legs of (mu_i + s_i mu_A) vanishes; asymmetries are n_i = g_i mu_i T^2/6
(fermions) and g_i mu_i T^2/3 (bosons)."""
import numpy as np
# unknowns: muQ1 (= Q2), muR (= u1 = u2 = d1 = d2 = d3), muQ3, muu3, mul (all 3 flavours), muH ; mu_A = 1
A = 1.0
rows, rhs = [], []
def eq(c, r): rows.append(c); rhs.append(r)
# 1 Weinberg operator  l l H H:  2(mul - A) + 2 muH = 0
eq([0, 0, 0, 0, 2, 2], 2 * A)
# 2 top Yukawa  Q3 -> u3 + H~ :  (muQ3 - A) = (muu3 + A) - muH
eq([0, 0, 1, -1, 0, 1], 2 * A)
# 3 strong sphaleron, sum over generations of 2(muQ - A) - (muu + A) - (mud + A) = 0
#   gens 1,2: 2muQ1 - 2muR ; gen 3: 2muQ3 - muu3 - muR ; source: -4A per generation
eq([4, -5, 2, -1, 0, 0], 12 * A)
# 4 hypercharge neutrality: sum g Y mu (fermions, T^2/6 units) + 2 * 2 * (1/2) muH (Higgs doublet, boson factor 2)
#   per gen: Q 6*(1/6), u 3*(2/3), d 3*(-1/3), l 2*(-1/2), e 1*(-1) (mu_e = 0)
eq([2 * 1, 2 * 2 - 3 * 1 + 2 * 0 + (-1) * 2 + 0, 1, 2, -3, 2], 0)   # placeholder, rebuilt below
rows.pop(); rhs.pop()
Q1, R, Q3, u3, l, H = range(6)
c = np.zeros(6)
c[Q1] += 2 * 1          # Q1, Q2: 6 * 1/6 each
c[R] += 2 * 3 * (2 / 3) + 3 * 3 * (-1 / 3)    # u1, u2 (2/3) and d1, d2, d3 (-1/3)
c[Q3] += 1
c[u3] += 3 * (2 / 3)
c[l] += 3 * 2 * (-1 / 2)
c[H] += 2 * 2 * (1 / 2)
eq(list(c), 0)
# 5 generation-1 invariant under strong sphalerons and gauge: N_Q1 + 2 N_u1 = 0  ->  6 muQ1 + 6 muR = 0
eq([6, 6, 0, 0, 0, 0], 0)
# 6 baryon number conserved (no electroweak sphalerons yet): sum (6 muQ + 3 muu + 3 mud) = 0
eq([12, 3 * 2 + 3 * 3, 6, 3, 0, 0], 0)
mu = np.linalg.solve(np.array(rows), np.array(rhs))
names = ["muQ1", "muR", "muQ3", "muu3", "mul", "muH"]
print(dict(zip(names, np.round(mu, 4))))
r = mu[l] / A
gs = 106.75
nL_over_s_per_muA = (45 / (2 * np.pi ** 2 * gs)) * r            # n_L = 3 flavours * 2 dof * mul T^2 / 6 = mul T^2
eta_per = (28 / 79) * abs(nL_over_s_per_muA)
need = 8.7e-11 / eta_per
print(f"mu_l / mu_A = {r:.3f};  n_B/s = {eta_per:.2e} x (mu_A/T);  needed mu_A/T = {need:.2e}")
print(f"earlier generic estimate needed mu/T = 2.30e-08 -> ratio {need / 2.30e-8:.2f}")
