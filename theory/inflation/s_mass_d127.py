"""D127 open check: S mass (m_S^2/H^2, real part) along the trajectory, old set-up vs the D127 Kahler metric. Full two-field
F-term potential V = e^K (K^{ij} D_i W conj(D_j W) - 3|W|^2), numerical Kahler derivatives, mpmath. zeta = 3e4, mu = 1. AI-assisted."""
import mpmath as mp
mp.mp.dps = 50
MU, NN, m2, ZETA = 1, 125, 4 / mp.pi, mp.mpf(3e4)
cl = lambda T: mp.exp(-NN * (1 - mp.exp(-T / m2)))
def setup(new):
    if new:
        K = lambda T, Tb, S, Sb: -3 * mp.log(T + Tb - S * Sb * (1 + (T + Tb) / (2 * MU)) + ZETA * (S * Sb) ** 2)
        W = lambda T, S: mp.sqrt(3) * S * T * cl(T)
    else:
        K = lambda T, Tb, S, Sb: -3 * mp.log(T + Tb - S * Sb + ZETA * (S * Sb) ** 2)
        W = lambda T, S: mp.sqrt(3) * S * T / mp.sqrt(1 + T / MU) * cl(T)
    return K, W
def V(K, W, T, S):
    Tb, Sb = mp.conj(T), mp.conj(S); h = mp.mpf("1e-12")
    k = lambda a, b, c, d: K(a, b, c, d)
    KT = (k(T + h, Tb, S, Sb) - k(T - h, Tb, S, Sb)) / (2 * h); KS = (k(T, Tb, S + h, Sb) - k(T, Tb, S - h, Sb)) / (2 * h)
    def d2(i, j):
        def f(e1, e2):
            a = [T, Tb, S, Sb]; a[i] += e1; a[j] += e2; return k(*a)
        return (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
    G = mp.matrix([[d2(0, 1), d2(0, 3)], [d2(2, 1), d2(2, 3)]]); Gi = G ** -1
    WT = (W(T + h, S) - W(T - h, S)) / (2 * h); WS = (W(T, S + h) - W(T, S - h)) / (2 * h); w = W(T, S)
    D = [WT + KT * w, WS + KS * w]
    F = sum(Gi[i, j] * D[i] * mp.conj(D[j]) for i in range(2) for j in range(2))   # K^{i jbar} D_i W conj(D_j W)
    return mp.re(mp.exp(k(T, Tb, S, Sb)) * (F - 3 * abs(w) ** 2)), G[1, 1]
for x in ("1.3e-4", "0.01", "1", "89"):
    T = mp.mpf(x); out = []
    for lab, new in (("old", False), ("new", True)):
        K, W = setup(new); s = mp.mpf("1e-6")
        v0, kss = V(K, W, T, mp.mpf(0)); vp, _ = V(K, W, T, s); vm, _ = V(K, W, T, -s)
        Vss = (vp - 2 * v0 + vm) / (s * s)
        out.append(f"{lab}: m_S^2/H^2 {float(Vss / (2 * kss) / (v0 / 3)):.4g}")
    print(f"x {x}: " + "   ".join(out))
