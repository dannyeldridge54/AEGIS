"""Development 72 check: the S mass with 40-digit arithmetic (mpmath), so finite differences cannot lose precision.
Same model and formula as s_stability.py: K = -3 ln(T + Tbar - S Sbar + zeta (S Sbar)^2), W = sqrt(3) S F(T),
V = e^K (K^{i jbar} D_i W conj(D_j W) - 3|W|^2), mu = 1, n = 125, m2 = 1. m_S^2 (canonical) / H^2 at S = 0. AI-assisted."""
import sys, os
import mpmath as mp
mp.mp.dps = 40
MU, N, M2 = 1, 125, 1
F = lambda T: T / mp.sqrt(1 + T / MU) * mp.exp(-N * T / (T + M2))


def V(T, S, z):
    # analytic derivatives of K for Omega = T + Tb - S Sb + z (S Sb)^2
    Tb, Sb = mp.conj(T), mp.conj(S); ss = S * Sb
    Om = T + Tb - ss + z * ss ** 2
    OT, OS = 1, -Sb + 2 * z * ss * Sb                       # dOmega/dT, dOmega/dS
    OSSb = -1 + 4 * z * ss                                  # d2 Omega / dS dSb
    KT, KS = -3 * OT / Om, -3 * OS / Om
    g = mp.matrix([[3 * OT * OT / Om ** 2, 3 * OT * mp.conj(OS) / Om ** 2],
                   [3 * OS * OT / Om ** 2, -3 * OSSb / Om + 3 * OS * mp.conj(OS) / Om ** 2]])
    W = mp.sqrt(3) * S * F(T); WT = mp.sqrt(3) * S * mp.diff(F, T); WS = mp.sqrt(3) * F(T)
    D = [WT + KT * W, WS + KS * W]
    gi = g ** -1
    s = sum(gi[j, i] * D[i] * mp.conj(D[j]) for i in range(2) for j in range(2))   # K^{i jbar} D_i W conj(D_j W)
    return mp.re(mp.exp(-3 * mp.log(mp.re(Om))) * (s - 3 * abs(W) ** 2)), g


for z in [mp.mpf(a) for a in sys.argv[1:]] or [0]:
    print(f"zeta = {z}:")
    for x in os.environ.get("XS", "1e-4 3e-4 1e-3 3e-3 1e-2 3e-2 0.1 1 10 30").split():
        x = mp.mpf(x); T = mp.mpc(x, 0)
        V0, g = V(T, mp.mpc(0), z); d = mp.mpf("1e-12")
        out = []
        for lab, st in (("Re", d), ("Im", 1j * d)):
            m2 = (V(T, st, z)[0] + V(T, -st, z)[0] - 2 * V0) / d ** 2 / (2 * mp.re(g[1, 1]))
            out.append(f"{lab} {float(m2 / (V0 / 3)):+.2f}")
        print(f"   x {float(x):.0e}: V {float(V0):.3e}, m_S^2/H^2: " + ", ".join(out))
