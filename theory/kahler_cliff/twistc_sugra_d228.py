"""D228 TWIST-C full SUGRA check, based on D218 (zeta = 3e5 re-run of D159; the old-Twist comparison column still uses zeta 3e4) (new direction): the cliff WITHOUT any hidden gauge sector. Put it in S's Kahler metric instead of the superpotential:
  K = -3 ln(u - g E(u) SS + zeta E(u)^2 (SS)^2),   u = T + Tbar,  g = 1 + u/2mu,  E(u) = exp(2n (1 - e^{-pi u/8}))
  W = sqrt3 m S T            (no exponential at all: no SU(8), no racetrack, W(S=0) = 0)
E depends on Re T only: shift-symmetric in Im T; on the tail its x-dependence is e^{-pi x/4} = |q|, the form of a worldsheet-instanton
correction to a Kahler metric. Full two-field F-term potential with step sizes scaled to E (S is evaluated at s/sqrt(E)). AI-assisted."""
import sys, mpmath as mp
sys.path.insert(0, "/home/claude/aegis/theory/inflation")
import s_mass_d127 as SM
mp.mp.dps = 200
n, ZETA = 125, mp.mpf(3e5); CC = mp.mpf("3.5e-7")   # D228: TWIST-C check
E = lambda u: mp.exp(2 * n * (1 - mp.exp(-mp.pi * u / 8)))
def Kn(T, Tb, S, Sb):
    u = T + Tb; e = E(u); return -3 * mp.log(u - (1 + u / 2) * e * S * Sb + ZETA * e ** 2 * (S * Sb) ** 2)
Wn = lambda T, S: mp.sqrt(3) * S * (T + CC)          # TWIST-C
def V(K, W, T, S, hT, hS):
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
Ko, Wo = SM.setup(True)
XS = sys.argv[1:] or ["1.3e-4", "0.01", "0.3", "1", "3", "89"]
for x in XS:
    X = mp.mpf(x); e = E(2 * X); hT = X * mp.mpf("1e-15"); hS = mp.mpf("1e-15") / mp.sqrt(e); s = mp.mpf("1e-9") / mp.sqrt(e)
    v, kss = V(Kn, Wn, X, mp.mpf(0), hT, hS)
    vo, _ = V(Ko, Wo, X, mp.mpf(0), hT, mp.mpf("1e-15"))
    vp, _ = V(Kn, Wn, X, s, hT, hS); vm, _ = V(Kn, Wn, X, -s, hT, hS)
    ms = (vp - 2 * v + vm) / (s * s) / (2 * kss) / (v / 3)
    hy = X * mp.mpf("1e-6")
    my = lambda K, W, v0, hs_: (V(K, W, mp.mpc(X, hy), mp.mpf(0), hT, hs_)[0] - 2 * v0 + V(K, W, mp.mpc(X, -hy), mp.mpf(0), hT, hs_)[0]) / (hy * hy) / (2 * 3 / (4 * X * X)) / (v0 / 3)
    print(f"x {x}: V_new/V_twist {float(v/vo):.10f}; m_S^2/H^2 {float(ms):.4g}; m_y^2/H^2 new {float(my(Kn, Wn, v, hS)):+.3f} "
          f"(Twist {float(my(Ko, Wo, vo, mp.mpf('1e-15'))):+.3f})", flush=True)
