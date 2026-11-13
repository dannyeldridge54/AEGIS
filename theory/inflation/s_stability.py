"""Development 72a (exploratory): is the helper field S stable at S = 0 during inflation? AI-assisted.
Full N = 1 supergravity scalar potential with two fields (T, S), computed numerically:
    V = e^K ( K^{i jbar} D_i W conj(D_j W) - 3 |W|^2 ),  D_i W = W_i + K_i W.
K = -3 ln(T + Tbar - S Sbar + zeta (S Sbar)^2)  (zeta = 0: the model as written; zeta > 0: the usual stabilising term)
W = sqrt(3) m S F(T), F(T) = T / sqrt(1 + T/mu) * exp(-n T/(T + m2)); m = 1 (units of m^2), mu = 1, n = 125, m2 = 1.
At S = 0 along the plateau (real T = x), we need the S mass^2 (both real and imaginary directions, canonically
normalised) and compare with H^2 = V/3. Stable and heavy means m_S^2 / H^2 > ~ +1 (well above zero)."""
import cmath, math
import numpy as np

MU, N, M2 = 1.0, 125.0, 1.0
F = lambda T: T / cmath.sqrt(1 + T / MU) * cmath.exp(-N * T / (T + M2))


def make(zeta):
    def K(T, S):
        return -3 * math.log((T + T.conjugate() - S * S.conjugate() + zeta * (S * S.conjugate()) ** 2).real)
    def W(T, S):
        return math.sqrt(3) * S * F(T)
    def V(z):                                   # z = [T, S] complex
        T, S = z
        h = 1e-4 * abs(T)
        def dK(i):                              # holomorphic derivative K_i = 1/2 (d/dRe - i d/dIm)
            e = [0, 0]; e[i] = h
            re = (K(T + e[0], S + e[1]) - K(T - e[0], S - e[1])) / (2 * h)
            e = [0, 0]; e[i] = 1j * h
            im = (K(T + e[0], S + e[1]) - K(T - e[0], S - e[1])) / (2 * h)
            return 0.5 * (re - 1j * im)
        def dW(i):
            e = [0, 0]; e[i] = h
            return (W(T + e[0], S + e[1]) - W(T - e[0], S - e[1])) / (2 * h)
        g = np.zeros((2, 2), complex); hh = 1e-3 * abs(T)
        for i in range(2):
            for j in range(2):
                # K_{i jbar} = d_i d_jbar K = 1/4 (d_x_i - i d_y_i)(d_x_j + i d_y_j) K
                def K2(a, b):
                    zz = [T, S]; zz[i] += a; zz[j] += b
                    return K(zz[0], zz[1])
                dxx = (K2(hh, hh) - K2(hh, -hh) - K2(-hh, hh) + K2(-hh, -hh)) / (4 * hh * hh)
                dyy = (K2(1j * hh, 1j * hh) - K2(1j * hh, -1j * hh) - K2(-1j * hh, 1j * hh) + K2(-1j * hh, -1j * hh)) / (4 * hh * hh)
                dxy = (K2(hh, 1j * hh) - K2(hh, -1j * hh) - K2(-hh, 1j * hh) + K2(-hh, -1j * hh)) / (4 * hh * hh)
                dyx = (K2(1j * hh, hh) - K2(1j * hh, -hh) - K2(-1j * hh, hh) + K2(-1j * hh, -hh)) / (4 * hh * hh)
                g[i, j] = 0.25 * (dxx + dyy + 1j * (dxy - dyx))
        gi = np.linalg.inv(g)
        w = W(T, S); DW = np.array([dW(i) + dK(i) * w for i in range(2)])
        return math.exp(K(T, S)) * ((DW @ gi.T @ DW.conj()).real - 3 * abs(w) ** 2), g
    return V


for zeta in [float(z) for z in __import__("sys").argv[1:]] or (0.0, 1.0, 10.0):
    V = make(zeta)
    print(f"zeta = {zeta}:")
    for x in (1e-4, 3e-4, 1e-3, 3e-3):
        V0, g = V([complex(x, 0), 0j]); H2 = V0 / 3; d = 1e-2 * math.sqrt(x)
        for lab, step in (("Re S", d), ("Im S", 1j * d)):
            Vp, _ = V([complex(x, 0), step]); Vm, _ = V([complex(x, 0), -step])
            m2 = (Vp + Vm - 2 * V0) / (d * d) / (2 * g[1, 1].real)        # canonical: L = g_SSbar |dS|^2
            print(f"   x {x:.0e}: V {V0:.3e}, m^2({lab}) / H^2 = {m2 / H2:+.2f}")
