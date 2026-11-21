"""Numerical Z3 action on magnetised torus zero modes at tau = omega (arXiv:1309.4925 eq. 2.19/4.7), any M and SS phases."""
import numpy as np, cmath, math
w = cmath.exp(2j * math.pi / 3); TAU = w
def theta(a, b, nu, t, L=25):
    l = np.arange(-L, L + 1)[:, None]
    return np.sum(np.exp(1j * np.pi * (a + l) ** 2 * t + 2j * np.pi * (a + l) * (nu + b)), axis=0)
def psi(j, M, a1, at, z):
    return np.exp(1j * np.pi * M * z * z.imag / TAU.imag) * theta((j + a1) / M, -at, M * z, M * TAU)
def modes(M, a1, at, z): return np.array([psi(j, M, a1, at, z) for j in range(M)]).T   # (points, M)
def z3_classes(M, a1, at, npts=400, seed=1):
    rng = np.random.default_rng(seed)
    z = rng.uniform(0, 1, npts) + TAU * rng.uniform(0, 1, npts)
    F = modes(M, a1, at, z); G = modes(M, a1, at, w * z)
    C = np.linalg.lstsq(F, G, rcond=None)[0].T          # psi^j(wz) = sum_i C[j,i] psi^i(z)
    res = np.linalg.norm(F @ C.T - G) / np.linalg.norm(G)
    ev, V = np.linalg.eig(C.T)
    return res, ev, V, C
if __name__ == '__main__':
    for M, a in ((6, 0), (8, 0), (10, 0), (3, 1/6), (5, 1/6), (7, 1/6), (9, 1/6), (9, 1/2), (9, 5/6)):
        res, ev, V, C = z3_classes(M, a, a)
        ph = np.sort(np.round((np.angle(ev) / (2 * math.pi)) % 1, 3))
        vals, cnt = np.unique(np.round(ph * 3) % 3, return_counts=True)
        print(M, a, 'residual %.1e' % res, 'eig phase classes', dict(zip(vals.astype(int), cnt)))
