"""D287 (weight-3/2 chi check; copy of D285 with K ⊃ X Xb/(T+Tb)^{3/2}) D285: full-supergravity check of D275. Fields T, S, X; TWIST-K Kahler with X inside the no-scale log:
  K = -3 ln(T + Tb - g E S Sb + zeta E^2 (S Sb)^2 - X Xb / 3),  W = sqrt3 m S T + (M/2) X^2 + (lam/2) S X^2   (m = 1 units, M_P = 1).
At S = X = 0: tree V(x); X's two real scalar masses^2 from the F-term potential (finite differences), its fermion mass
m_F = e^{K/2} |W_XX| / K_XXb; one-loop CW  dV = (1/64 pi^2)[sum_s m_s^4 (ln m_s^2 - 3/2) - 2 m_F^4 (ln m_F^2 - 3/2)] (canonical masses).
Report gamma_eff = (1/2) d ln(1 + dV/V) / d ln x on the plateau, to compare with D275's -N lam^2/(64 pi^2) (N = 1 here). AI-assisted."""
import mpmath as mp, sys
mp.mp.dps = 60
n, ZETA = 125, mp.mpf(3e5)
E = lambda u: mp.exp(2 * n * (1 - mp.exp(-mp.pi * u / 8)))
def K(z):   # z = [T, Tb, S, Sb, X, Xb]
    T, Tb, S, Sb, X, Xb = z; u = T + Tb; e = E(u)
    return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2) + X * Xb / u ** mp.mpf(1.5)
def make(M, lam):
    W = lambda T, S, X: mp.sqrt(3) * S * T + M / 2 * X ** 2 + lam / 2 * S * X ** 2
    dW = lambda T, S, X: [mp.sqrt(3) * S, mp.sqrt(3) * T + lam / 2 * X ** 2, M * X + lam * S * X]
    def V(T, S, X, h=mp.mpf("1e-20")):
        z0 = [T, mp.conj(T), S, mp.conj(S), X, mp.conj(X)]
        def k(dz):
            z = list(z0)
            for i, d in dz: z[i] += d
            return K(z)
        Ki = [(k([(2 * a, h)]) - k([(2 * a, -h)])) / (2 * h) for a in range(3)]
        G = mp.matrix(3, 3)
        for a in range(3):
            for b in range(3):
                G[a, b] = (k([(2 * a, h), (2 * b + 1, h)]) - k([(2 * a, h), (2 * b + 1, -h)]) - k([(2 * a, -h), (2 * b + 1, h)]) + k([(2 * a, -h), (2 * b + 1, -h)])) / (4 * h * h)
        Gi = G ** -1; w = W(T, S, X); d = dW(T, S, X); D = [d[a] + Ki[a] * w for a in range(3)]
        F = sum(Gi[a, b] * D[a] * mp.conj(D[b]) for a in range(3) for b in range(3))
        return mp.re(mp.exp(k([])) * (F - 3 * abs(w) ** 2)), G
    return V
def masses(V, x, M):
    T = mp.mpf(x); v0, G = V(T, mp.mpf(0), mp.mpf(0)); gxx = G[2, 2]; e = mp.mpf("1e-12")
    out = []
    for dirn in (1, 1j):            # real and imaginary X
        X1 = e * dirn
        vp = V(T, mp.mpf(0), X1)[0]; vm = V(T, mp.mpf(0), -X1)[0]
        out.append((vp - 2 * v0 + vm) / (e * e) / (2 * gxx))   # canonical: kinetic 2 Gxx |dX|^2 -> real field norm
    mF = mp.exp(-3 * mp.log(2 * T) / 2) * M / gxx
    return v0, out, mF
lam = mp.mpf(sys.argv[1]) if len(sys.argv) > 1 else mp.mpf(1)
M = mp.mpf(sys.argv[2]) if len(sys.argv) > 2 else mp.mpf("1e-3")
V = make(M, lam)
res = []
for x in ("5e-5", "1e-4", "1.3e-4", "2e-4", "4e-4"):
    v0, ms, mF = masses(V, x, M)
    cw = (sum(m2 ** 2 * (mp.log(abs(m2)) - 1.5) for m2 in ms) - 2 * mF ** 4 * (mp.log(mF ** 2) - 1.5)) / (64 * mp.pi ** 2)
    res.append((mp.log(mp.mpf(x)), mp.log(1 + cw / v0)))
    print(f"x {x}: V {float(v0):.5g}, m_s^2 {float(ms[0]):.5g}, {float(ms[1]):.5g}, m_F^2 {float(mF**2):.5g}, dV/V {float(cw/v0):+.4e}", flush=True)
g = [(res[i + 1][1] - res[i][1]) / (res[i + 1][0] - res[i][0]) / 2 for i in range(len(res) - 1)]
print("gamma_eff between points:", [f"{float(t):+.4e}" for t in g], " D275 estimate -lam^2/(64 pi^2) =", f"{float(-lam**2/(64*mp.pi**2)):+.4e}")
