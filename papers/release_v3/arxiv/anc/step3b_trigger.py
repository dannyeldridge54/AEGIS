"""Plan step 3b: does geometry switch the twist field on at matter-radiation equality?

Part 1 (symbolic): in a flat FRW universe,
  (a) the Holst-type contraction eps^{abcd} R_{abcd} of the Levi-Civita curvature vanishes identically, so the minimal
      Holst / Nieh-Yan action gives the field no curvature coupling: only its kinetic term (Taveras & Yunes 2008);
  (b) the Ricci scalar R = 6(a''/a + H^2) is zero for radiation (a ~ t^1/2) and non-zero for matter (a ~ t^2/3);
  (c) with radiation + matter, R / H^2 = 3 Omega_m(a) = 3 / (1 + a_eq / a): it turns on centred exactly at equality.
Part 2 (numeric): add the smallest geometric term, xi * R * phi^2 / 2 (allowed by symmetry; 'early modified gravity'),
  and find when the field starts moving, for a range of xi, relative to equality. Only the coupling term is kept
  (no potential), so this isolates the trigger.
Run: python step3b_trigger.py
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

# ---------- Part 1a: eps^{abcd} R_{abcd} = 0 for FRW ----------
t, x, y, z = sp.symbols("t x y z")
a = sp.Function("a")(t)
X = [t, x, y, z]
g = sp.diag(-1, a ** 2, a ** 2, a ** 2)
gi = g.inv()
Gam = [[[sp.simplify(sum(gi[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s]))
                         for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]


def riemann(r, s, m, n):   # R^r_{smn}
    e = sp.diff(Gam[r][n][s], X[m]) - sp.diff(Gam[r][m][s], X[n])
    e += sum(Gam[r][m][l] * Gam[l][n][s] - Gam[r][n][l] * Gam[l][m][s] for l in range(4))
    return sp.simplify(e)


Rud = [[[[riemann(r, s, m, n) for n in range(4)] for m in range(4)] for s in range(4)] for r in range(4)]
Rdd = [[[[sp.simplify(sum(g[r, q] * Rud[q][s][m][n] for q in range(4))) for n in range(4)] for m in range(4)]
        for s in range(4)] for r in range(4)]
eps = lambda *i: sp.LeviCivita(*i)
holst = sp.simplify(sum(eps(p, q, r, s) * Rdd[p][q][r][s] for p in range(4) for q in range(4) for r in range(4)
                        for s in range(4)))
Ric = [[sp.simplify(sum(Rud[r][m][r][n] for r in range(4))) for n in range(4)] for m in range(4)]
R = sp.simplify(sum(gi[m, n] * Ric[m][n] for m in range(4) for n in range(4)))
print("1a  eps^{abcd} R_abcd (Levi-Civita, FRW) =", holst)
print("1b  Ricci scalar R =", R)
p = sp.symbols("p", positive=True)
Rpow = sp.simplify(R.subs(a, t ** p).doit())
print("    power law a=t^p: R =", sp.factor(Rpow), "| radiation p=1/2:", sp.simplify(Rpow.subs(p, sp.Rational(1, 2))),
      "| matter p=2/3:", sp.simplify(Rpow.subs(p, sp.Rational(2, 3))))

# ---------- Part 1c: R/H^2 with radiation + matter ----------
rm, rr = sp.symbols("rho_m rho_r", positive=True)
H2 = (rm + rr) / 3                                 # units 8 pi G = 1
Hdot = -(rm + sp.Rational(4, 3) * rr) / 2          # Raychaudhuri, p_r = rho_r/3, p_m = 0
R_fl = 6 * (Hdot + 2 * H2)
print("1c  R =", sp.simplify(R_fl), "  R/H^2 =", sp.simplify(R_fl / H2), "= 3 Omega_m; half-way (Omega_m=1/2) at a = a_eq")

# ---------- Part 2: when does a xi R phi^2 coupling move the field? ----------
# e-folds N = ln(a/a_eq): Omega_m = 1/(1+e^-N), H'/H = -2 + Omega_m/2, R/H^2 = 3 Omega_m
def rhs(N, u, xi):
    om = 1 / (1 + np.exp(-N))
    phi, dphi = u
    return [dphi, -(3 - 2 + om / 2) * dphi - 3 * xi * om * phi]


print("\n2   xi      field starts moving at a/a_eq   (z/z_eq)")
rows = []
for xi in (-10, -3, -1, -0.3, 0.3, 1, 3, 10):
    sol = solve_ivp(rhs, (-10, 6), [1.0, 0.0], args=(xi,), max_step=0.01, dense_output=True)
    N = np.linspace(-10, 6, 16001)
    ph = sol.sol(N)[0]
    k = np.argmax(np.abs(ph - 1) > 0.1)              # 10% move from the frozen value
    Nm = N[k] if np.abs(ph[k] - 1) > 0.1 else np.nan
    rows.append((xi, np.exp(Nm)))
    print(f"    {xi:6}   {np.exp(Nm):10.3f}                   ({1/np.exp(Nm):.3f})")
