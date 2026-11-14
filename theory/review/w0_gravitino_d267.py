"""D267: what a constant SUSY-breaking term W0 does in the Twist's no-scale sector (TWIST-K, n = 125, zeta = 3e5).
(1) full two-field F-term potential with W = sqrt3 m S T + W0, S relaxed to its minimum, at the CMB point, cliff and today;
(2) gravitino mass e^{K/2}|W0| ∝ x^{-3/2} along the history. Units: M_P = 1, m = 1 inside V (W0 quoted as W0/m). AI-assisted."""
import mpmath as mp
mp.mp.dps = 200
n, ZETA = 125, mp.mpf(3e5)
E = lambda u: mp.exp(2 * n * (1 - mp.exp(-mp.pi * u / 8)))
def K(T, Tb, S, Sb):
    u = T + Tb; e = E(u); return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
def V(T, S, w0, hT, hS):
    Tb, Sb = mp.conj(T), mp.conj(S); hs = (hT, hT, hS, hS)
    W = lambda T_, S_: mp.sqrt(3) * S_ * T_ + w0
    def f(i, j, e1, e2):
        a = [T, Tb, S, Sb]; a[i] += e1; a[j] += e2; return K(*a)
    d1 = lambda i: (f(i, i, hs[i], 0) - f(i, i, -hs[i], 0)) / (2 * hs[i])
    d2 = lambda i, j: (f(i, j, hs[i], hs[j]) - f(i, j, hs[i], -hs[j]) - f(i, j, -hs[i], hs[j]) + f(i, j, -hs[i], -hs[j])) / (4 * hs[i] * hs[j])
    G = mp.matrix([[d2(0, 1), d2(0, 3)], [d2(2, 1), d2(2, 3)]]); Gi = G ** -1
    w = W(T, S); D = [mp.sqrt(3) * S + d1(0) * w, mp.sqrt(3) * T + d1(2) * w]
    F = sum(Gi[i, j] * D[i] * mp.conj(D[j]) for i in range(2) for j in range(2))
    return mp.re(mp.exp(K(T, Tb, S, Sb)) * (F - 3 * abs(w) ** 2))
def relaxed(X, w0):
    e = E(2 * X); hT = X * mp.mpf("1e-15"); hS = mp.mpf("1e-15") / mp.sqrt(e)
    v0 = V(mp.mpf(X), mp.mpf(0), mp.mpf(0), hT, hS)
    f = lambda s: V(mp.mpf(X), s / mp.sqrt(e), w0, hT, hS)
    s, best = mp.mpf(0), f(0)
    for step in [mp.mpf(10) ** -k for k in range(1, 14)]:      # crude 1-d search along real S (W0 real)
        for sgn in (1, -1):
            while True:
                t = s + sgn * step; ft = f(t)
                if ft < best: s, best = t, ft
                else: break
    return v0, f(0), best, s
MP_GEV, m = 2.435e18, 2.1e-5
for X in ("1.3e-4", "1", "89"):
    X = mp.mpf(X); fac = float((2 * X) ** -1.5)
    for w0 in ("1e-6", "1e-3", "1"):
        v0, vS0, vmin, s = relaxed(X, mp.mpf(w0))
        print(f"x {float(X):g}  W0/m {w0}: V(W0,S=0)/V0 = {float(vS0/v0):.8f}, V(W0,S relaxed)/V0 = {float(vmin/v0):.8f}, "
              f"m32 = {fac*float(w0)*m*MP_GEV:.2e} GeV, H = {float(mp.sqrt(v0/3))*m*MP_GEV:.2e} GeV", flush=True)
