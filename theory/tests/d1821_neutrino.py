import numpy as np, math, json
TAU = 1j
def theta(a, b, nu, t, L=25):
    l = np.arange(-L, L + 1)[:, None]
    return np.sum(np.exp(1j * np.pi * (a + l) ** 2 * t + 2j * np.pi * (a + l) * (nu + b)), axis=0)
def psi(j, M, z): return np.exp(1j * np.pi * M * z * z.imag / TAU.imag) * theta(j / M, 0, M * z, M * TAU)
def even(M, z):
    P = np.array([psi(j, M, z) for j in range(M)]).T; cols = [P[:, 0]]
    for j in range(1, M // 2): cols.append((P[:, j] + P[:, M - j]) / math.sqrt(2))
    cols.append(P[:, M // 2]); return np.array(cols).T
rng = np.random.default_rng(5); z = rng.uniform(0, 1, 600) + TAU * rng.uniform(0, 1, 600)
L = even(4, z); H = even(8, z)
P = np.einsum('pi,pj->pij', L, L).reshape(len(z), -1)
c, *_ = np.linalg.lstsq(H, P, rcond=None); res = np.linalg.norm(H @ c - P) / np.linalg.norm(P); c = c.T.reshape(3, 3, 5)
hr = np.random.default_rng(11); h = hr.normal(size=(50000, 5)) + 1j * hr.normal(size=(50000, 5))
s = np.sort(np.linalg.svd(np.einsum('ijk,nk->nij', c, h), compute_uv=False), axis=1)
r23, r12 = s[:, 1] / s[:, 2], s[:, 0] / s[:, 1]
ok = (np.abs(np.log(r23 / math.sqrt(0.1726))) < math.log(1.5)) & (r12 < 0.1)
frac = float(ok.mean()); v = 'NATURAL' if frac >= 0.01 else 'TUNED' if frac > 0 else 'ABSENT'
m3 = 0.0501e-9; vu = 174 * math.sin(math.atan(2)); g = math.sqrt(4 * math.pi / 28.0)
out = dict(gate_residual=float(res), frac=frac, verdict_ratio=v, median_r23=float(np.median(r23)), median_r12=float(np.median(r12)),
           M_N_gauge_yukawa_GeV=g ** 2 * vu ** 2 / m3, y3_for_window=[math.sqrt(m3 * M / vu ** 2) for M in (4.5e10, 2.5e12)])
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1821_neutrino.json', 'w'), indent=1)
