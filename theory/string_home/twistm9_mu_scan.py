"""PREREG_TWISTM9 scan (locked ce4be11): TWIST-M9 for mu in {0.125 ... 16}. AI-assisted.
Single-field slow roll along real T (S = 0): V = m^2/(4 g E), g = 1 + u/(2 mu), E = exp(2n(1 - s)), s = 1/(1 + h(u/144)^9).
S-mass check at the CMB point: full two-field F-term potential (D159 method), K = -3 ln(u - g E S Sbar + zeta E^2 (S Sbar)^2), W = sqrt3 S T."""
import mpmath as mp
n, ZETA = 125, mp.mpf(3e4)
def eta(y): return mp.e ** (-2 * mp.pi * y / 24) * mp.qp(mp.e ** (-2 * mp.pi * y))
def h(y):
    if y < mp.mpf(1) / 3: return (3 * eta(1 / y) / eta(1 / (9 * y))) ** 3
    return (eta(y) / eta(9 * y)) ** 3
def Efun(u):
    H9 = h(u / 144) ** 9; return mp.exp(2 * n * H9 / (1 + H9))    # = exp(2n(1-s))
def slow_roll(mu):
    mp.mp.dps = 30
    k = mp.sqrt(mp.mpf(2) / 3)
    f = lambda p: -mp.log(1 + mp.e ** (k * p) / (2 * mu)) - mp.log(Efun(mp.e ** (k * p)))
    d1 = lambda p: mp.diff(f, p); d2 = lambda p: mp.diff(f, p, 2); eps = lambda p: d1(p) ** 2 / 2
    p = mp.mpf(6)
    while eps(p) < 1:
        p -= mp.mpf("0.02")
        if p < -30: return None, "no end at the cliff"
    while eps(p) > 1: p -= mp.mpf("0.02")
    pend = mp.findroot(lambda q: eps(q) - 1, (p, p + mp.mpf("0.02")), solver="anderson")
    res, N, q, dq = [], mp.mpf(0), pend, mp.mpf("-0.004")
    for Ns in (55.7, 57):
        while N < Ns: N += -dq / abs(d1(q)); q += dq
        res.append((Ns, mp.e ** (k * q), 1 + 2 * d2(q) - d1(q) ** 2, 8 * d1(q) ** 2))
    return (mp.e ** (k * pend), res), None
def s_mass(mu, x):
    mp.mp.dps = 60
    def K(T, Tb, S, Sb):
        u = T + Tb; e = Efun(mp.re(u)); return -3 * mp.log(u - (1 + u / (2 * mu)) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
    W = lambda T, S: mp.sqrt(3) * S * T
    def V(T, S, hT, hS):
        Tb, Sb = mp.conj(T), mp.conj(S); hs = (hT, hT, hS, hS)
        def f(i, j, e1, e2):
            a = [T, Tb, S, Sb]; a[i] += e1; a[j] += e2; return K(*a)
        d1 = lambda i: (f(i, i, hs[i], 0) - f(i, i, -hs[i], 0)) / (2 * hs[i])
        d2 = lambda i, j: (f(i, j, hs[i], hs[j]) - f(i, j, hs[i], -hs[j]) - f(i, j, -hs[i], hs[j]) + f(i, j, -hs[i], -hs[j])) / (4 * hs[i] * hs[j])
        G = mp.matrix([[d2(0, 1), d2(0, 3)], [d2(2, 1), d2(2, 3)]]); Gi = G ** -1
        WT = (W(T + hT, S) - W(T - hT, S)) / (2 * hT); WS = (W(T, S + hS) - W(T, S - hS)) / (2 * hS); w = W(T, S)
        D = [WT + d1(0) * w, WS + d1(2) * w]
        F = sum(Gi[i, j] * D[i] * mp.conj(D[j]) for i in range(2) for j in range(2))
        return mp.re(mp.exp(K(T, Tb, S, Sb)) * (F - 3 * abs(w) ** 2)), G[1, 1]
    X = mp.mpf(x); hT = X * mp.mpf("1e-12"); hS = mp.mpf("1e-12"); s = mp.mpf("1e-6")
    v, kss = V(X, mp.mpf(0), hT, hS); vp, _ = V(X, s, hT, hS); vm, _ = V(X, -s, hT, hS)
    return (vp - 2 * v + vm) / (s * s) / (2 * kss) / (v / 3)
gs_today = 0.7 * (89 / 72) ** 1.5
print(f"g_s today (x = 89, independent of mu at fixed tail) = {gs_today:.2f}")
for mu in (0.125, 0.25, 0.5, 1, 2, 4, 8, 16):
    out, why = slow_roll(mp.mpf(mu))
    if out is None: print(f"mu {mu}: EXCLUDED ({why})", flush=True); continue
    uend, res = out
    ms = s_mass(mp.mpf(mu), res[1][1] / 2)
    flag = " EXCLUDED (S tachyonic)" if ms < 0 else ""
    print(f"mu {mu:6}: end u {float(uend):.3g}; " + "; ".join(f"N*={a}: u*={float(b):.3g} n_s={float(c):.4f} r={float(d):.4f}" for a, b, c, d in res)
          + f"; m_S^2/H^2 = {float(ms):.3g}{flag}", flush=True)
