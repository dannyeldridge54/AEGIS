"""D285b: n_s, r for the TWIST-K plateau times (1 + b x_ref/x) — the form the full-SUGRA one-loop term from a heavy field inside the
no-scale log takes (dV/V ∝ 1/x, D285). Slow roll in canonical phi (x = e^{sqrt(2/3) phi}); N* = 57. AI-assisted."""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
c = np.sqrt(2/3); n, mu = 125, 1.0
def V(p, b):
    x = np.exp(c * p); return np.exp(-2 * n * (1 - np.exp(-np.pi * x / 4))) / (1 + x / mu) * (1 + b * 1.3e-4 / x)
def d(p, b, h=1e-5): return (V(p + h, b) - V(p - h, b)) / (2 * h)
def dd(p, b, h=1e-4): return (V(p + h, b) - 2 * V(p, b) + V(p - h, b)) / h ** 2
def obs(b, Nst=57.0):
    eps = lambda p: 0.5 * (d(p, b) / V(p, b)) ** 2
    pe = brentq(lambda p: eps(p) - 1, np.log(1e-3) / c, np.log(0.5) / c)
    N = lambda ps: quad(lambda p: V(p, b) / d(p, b), ps, pe)[0] * -1
    ps = brentq(lambda p: N(p) - Nst, np.log(1e-7) / c, pe - 1e-3)
    e, eta = eps(ps), dd(ps, b) / V(ps, b)
    return 1 - 6 * e + 2 * eta, 16 * e, np.exp(c * ps)
for b in (0.0, 0.001, 0.003, 0.01, 0.03):
    ns, r, xs = obs(b); print(f"b {b}: n_s {ns:.4f}, r {r:.4f}, x* {xs:.2e}")
