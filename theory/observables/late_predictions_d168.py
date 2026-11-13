"""D168: the Twist's late-universe predictions beyond (w0, wa): w(z), H(z)/H_LCDM, distances, growth f sigma8 and S8, versus LCDM with
the same Omega_m and H0 (Omega_m = 0.31). Tail: rung-3 thawing quintessence V ~ exp(-sqrt(2/3) phi) from rest (D125/D151 — the tail is
insensitive to the heat share). Growth: linear sub-horizon d'' + (2 + dlnH/dN) d' - 1.5 Om(a) d = 0 (the field does not cluster:
sound speed 1). AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
Om, Or = 0.31, 9.1e-5; ODE = 1 - Om - Or; lam = math.sqrt(2 / 3)
def go(V0):
    def rhs(N, y):
        p, v = y; a = math.exp(N); V = V0 * math.exp(-lam * p); H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
        eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2; return [v, -(3 - eps) * v + lam * V / H2]
    return solve_ivp(rhs, [math.log(1e-4), 0], [0, 0], rtol=1e-11, atol=1e-13, dense_output=True)
def f0(V0):
    s = go(V0); p, v = s.y[:, -1]; V = V0 * math.exp(-lam * p); H2 = (Om + Or + V / 3) / (1 - v * v / 6); return (v * v * H2 / 6 + V / 3) / H2 - ODE
V0 = brentq(f0, 1e-2, 1e3); S = go(V0)
def E2(a):                       # (H/H0)^2 for the Twist
    N = math.log(a); p, v = S.sol(N); V = V0 * math.exp(-lam * p); return (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
def w(a):
    N = math.log(a); p, v = S.sol(N); V = V0 * math.exp(-lam * p); H2 = E2(a); K = v * v * H2 / 6; return (K - V / 3) / (K + V / 3)
E2L = lambda a: Om * a ** -3 + Or * a ** -4 + ODE
def growth(E2f):
    dl = lambda a, h=1e-5: (math.log(E2f(a * (1 + h))) - math.log(E2f(a * (1 - h)))) / (4 * h)    # dlnH/dlna
    def rhs(N, y):
        a = math.exp(N); d, dp = y; return [dp, -(2 + dl(a)) * dp + 1.5 * Om * a ** -3 / E2f(a) * d]
    a0 = 1e-3; s = solve_ivp(rhs, [math.log(a0), 0], [a0, a0], rtol=1e-10, atol=1e-13, dense_output=True); return s
GT, GL = growth(E2), growth(E2L)
D = lambda G, a: G.sol(math.log(a))[0]; f = lambda G, a: G.sol(math.log(a))[1] / G.sol(math.log(a))[0]
chi = lambda E, z: quad(lambda zz: 1 / math.sqrt(E(1 / (1 + zz))), 0, z)[0]
s8 = D(GT, 1) / D(GL, 1)          # same primordial amplitude, same early growth
print(f"S8 (sigma8) relative to LCDM with the same Omega_m and early amplitude: {s8:.4f} ({100*(s8-1):+.2f}%)")
print(" z    w(z)     H/H_LCDM   D_M/D_M,LCDM   f/f_LCDM   f sigma8 / LCDM")
for z in (0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0):
    a = 1 / (1 + z); hr = math.sqrt(E2(a) / E2L(a)); dm = chi(E2, z) / chi(E2L, z) if z > 0 else 1.0
    fr = f(GT, a) / f(GL, a); fs8 = fr * (D(GT, a) / D(GL, a))
    print(f"{z:4.1f}  {w(a):+.4f}   {hr:.5f}     {dm:.5f}       {fr:.4f}     {fs8:.4f}")
print("\ngrowth index gamma(z) = ln f / ln Omega_m(a):")
for z in (0.0, 0.5, 1.0):
    a = 1 / (1 + z)
    omT = Om * a ** -3 / E2(a); omL = Om * a ** -3 / E2L(a)
    print(f"  z {z}: Twist {math.log(f(GT, a))/math.log(omT):.4f}, LCDM {math.log(f(GL, a))/math.log(omL):.4f}")
