"""D195: inflation in TWIST-M (D194) vs the Twist, single-field along real T with S = 0. AI-assisted.
At S = 0, V = e^K K^{SSbar}|W_S|^2 = m^2 / (4 g(u) E(u)), u = T + Tbar = e^{sqrt(2/3) phi}, g = 1 + u/2 (mu = 1).
Twist: E = exp(2n(1 - e^{-pi u/8})). TWIST-M: E = exp(2n(1 - s)), s = 1/(1 + c h(y)), h = (eta(iy)/eta(9iy))^3, y = Im T_het = u/16."""
import mpmath as mp, sys
mp.mp.dps = 30
n = 125
def eta(y): return mp.e ** (-2 * mp.pi * y / 24) * mp.qp(mp.e ** (-2 * mp.pi * y))
def h(y): return (eta(y) / eta(9 * y)) ** 3
def lnV_twist(u): return -mp.log(1 + u / 2) - 2 * n * (1 - mp.exp(-mp.pi * u / 8))
def make_M(c):
    return lambda u: -mp.log(1 + u / 2) - 2 * n * (c * h(u / 16)) / (1 + c * h(u / 16))
def analyse(lnV, label, Nstar=(55.7, 57)):
    k = mp.sqrt(mp.mpf(2) / 3)
    f = lambda p: lnV(mp.e ** (k * p))
    d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2)
    eps = lambda p: d1(p) ** 2 / 2
    # end of inflation: eps = 1, scanning down from large phi
    p = mp.mpf(3)
    while eps(p) > 1 and p > -40: p -= mp.mpf("0.02")
    pend = mp.findroot(lambda q: eps(q) - 1, p)
    out = []
    for Ns in Nstar:
        # N = int_{pend}^{p*} dphi / sqrt(2 eps) ; integrate backwards (phi decreases into the plateau)
        N, q, dq = mp.mpf(0), pend, mp.mpf("-0.002")
        while N < Ns:
            N += -dq / abs(d1(q)); q += dq
        ns = 1 - 6 * eps(q) + 2 * (d2(q) + d1(q) ** 2) if False else 1 + 2 * d2(q) - d1(q) ** 2   # n_s = 1 - 6eps + 2eta with V'/V form
        r = 8 * d1(q) ** 2
        out.append((Ns, float(mp.e ** (k * q)), float(ns), float(r)))
    print(f"{label}: end at u = {float(mp.e ** (k * pend)):.4g}; " + "; ".join(f"N*={a}: u*={b:.3g}, n_s={c:.4f}, r={d:.4f}" for a, b, c, d in out), flush=True)
analyse(lnV_twist, "Twist (check)")
for c in (1,):          # c = 1e3, 1e10 runs were slow and stopped (not needed: c = 1 is the natural value)
    analyse(make_M(mp.mpf(c)), f"TWIST-M c={c:g}")
