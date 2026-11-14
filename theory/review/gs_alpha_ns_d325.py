"""D325 (locked, PREREG_D325_GS_ALPHA): n_s, r when the GS dilaton shifts the no-scale alpha. Based on gminus_ns_d285b.py. AI-assisted."""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
n, mu = 125, 1.0
def make(al):
    c = np.sqrt(2 / (3 * al))
    def V(p):
        x = np.exp(c * p); return np.exp(-2 * n * (1 - np.exp(-np.pi * x / 4))) / (1 + x / mu) * x ** (3 * (1 - al))
    return c, V
def obs(al, Nst=57.0):
    c, V = make(al)
    d = lambda p, h=1e-5: (V(p + h) - V(p - h)) / (2 * h)
    dd = lambda p, h=1e-4: (V(p + h) - 2 * V(p) + V(p - h)) / h ** 2
    eps = lambda p: 0.5 * (d(p) / V(p)) ** 2
    pe = brentq(lambda p: eps(p) - 1, np.log(1e-3) / c, np.log(0.5) / c)
    N = lambda ps: -quad(lambda p: V(p) / d(p), ps, pe, limit=200)[0]
    ps = brentq(lambda p: N(p) - Nst, np.log(1e-7) / c, pe - 1e-3)
    e, eta = eps(ps), dd(ps) / V(ps)
    return 1 - 6 * e + 2 * eta, 16 * e, np.exp(c * ps)
base = obs(1.0)
print(f"alpha 1 (baseline): n_s {base[0]:.4f}, r {base[1]:.4f}, x* {base[2]:.2e}")
for al in (1 - 0.171 / (3 * 3.98), 1 + 0.171 / (3 * 3.98)):
    ns, r, xs = obs(al); print(f"alpha {al:.5f}: n_s {ns:.4f} (dn_s {ns - base[0]:+.4f}), r {r:.4f}, x* {xs:.2e}")
