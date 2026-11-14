"""D269 test of D267 option (ii): SUSY breaking with an x-independent gravitino mass, W = sqrt3 m S T + w T^{3/2}, plus a constant
uplift +3 m32^2 (m32 = w/2^{3/2} in units of m) that cancels the AdS energy. TWIST-K Kahler (n 125, zeta 3e5). Full two-field F-term
potential; S relaxed by Newton steps along real S; angle mass m_y^2/H^2 at the relaxed point. Units M_P = 1, m = 1. AI-assisted."""
import mpmath as mp, sys
mp.mp.dps = 200
n, ZETA = 125, mp.mpf(3e5)
E = lambda u: mp.exp(2 * n * (1 - mp.exp(-mp.pi * u / 8)))
def K(T, Tb, S, Sb):
    u = T + Tb; e = E(u); return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
def V(T, S, w, hT, hS):
    Tb, Sb = mp.conj(T), mp.conj(S); hs = (hT, hT, hS, hS)
    W = lambda T_, S_: mp.sqrt(3) * S_ * T_ + w * T_ ** mp.mpf(1.5)
    WT = lambda T_, S_: mp.sqrt(3) * S_ + mp.mpf(1.5) * w * T_ ** mp.mpf(0.5)
    def f(i, j, e1, e2):
        a = [T, Tb, S, Sb]; a[i] += e1; a[j] += e2; return K(*a)
    d1 = lambda i: (f(i, i, hs[i], 0) - f(i, i, -hs[i], 0)) / (2 * hs[i])
    d2 = lambda i, j: (f(i, j, hs[i], hs[j]) - f(i, j, hs[i], -hs[j]) - f(i, j, -hs[i], hs[j]) + f(i, j, -hs[i], -hs[j])) / (4 * hs[i] * hs[j])
    G = mp.matrix([[d2(0, 1), d2(0, 3)], [d2(2, 1), d2(2, 3)]]); Gi = G ** -1
    wv = W(T, S); D = [WT(T, S) + d1(0) * wv, mp.sqrt(3) * T + d1(2) * wv]
    F = sum(Gi[i, j] * D[i] * mp.conj(D[j]) for i in range(2) for j in range(2))
    return mp.re(mp.exp(K(T, Tb, S, Sb)) * (F - 3 * abs(wv) ** 2)) + 3 * w * w / 8      # + uplift
MP_GEV, m = 2.435e18, 2.1e-5
for x in ("1.3e-4", "1", "89"):
    X = mp.mpf(x); e = E(2 * X); hT = X * mp.mpf("1e-15"); hS = mp.mpf("1e-15") / mp.sqrt(e)
    v0 = V(X, mp.mpf(0), mp.mpf(0), hT, hS)
    for w in sys.argv[1:] or ["5.5e-3", "0.55"]:
        w = mp.mpf(w); g = lambda s: V(X, s / mp.sqrt(e), w, hT, hS)
        s, h = mp.mpf(0), mp.mpf("1e-12")
        for _ in range(12):
            a, b, c = g(s - h), g(s), g(s + h); d1, d2 = (c - a) / (2 * h), (c - 2 * b + a) / (h * h)
            if d2 <= 0: break
            s -= d1 / d2
        vr = g(s); hy = X * mp.mpf("1e-6"); Tp, Tm = mp.mpc(X, hy), mp.mpc(X, -hy)
        my = (V(Tp, s / mp.sqrt(e), w, hT, hS) - 2 * vr + V(Tm, s / mp.sqrt(e), w, hT, hS)) / (hy * hy) / (2 * 3 / (4 * X * X)) / (vr / 3)
        print(f"x {x}  m32 {float(w)/2**1.5*m*MP_GEV:.1e} GeV: V(S=0)/V0 {float(g(0)/v0):.6g}, V(S relaxed)/V0 {float(vr/v0):.6g}, "
              f"S*sqrt(E) {float(s):.2e}, m_y^2/H^2 {float(my):+.3g}", flush=True)
