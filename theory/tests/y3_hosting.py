"""PREREG_Y3_HOSTING"""
import sys, numpy as np, json, random, math
from scipy.optimize import minimize
sys.path.insert(0, 'theory/tests')
import importlib.util
spec = importlib.util.spec_from_file_location('y2', 'theory/tests/y2_orbifold.py')
src = open('theory/tests/y2_orbifold.py').read().split('res = {}')[0]; ns = {}; exec(src, ns)
Y, CL, CR, CH = ns['Y'], ns['CL'], ns['CR'], ns['CH']
cl = [c for c in CL if CL[c].shape[1] == 3][0]; cr = [c for c in CR if CR[c].shape[1] == 3][0]; ch = (-(cl + cr)) % 3
B = np.einsum('ijk,ia,jb,kc->abc', Y, CL[cl], CR[cr], CH[ch].conj()); nH = B.shape[2]
def svals(x):
    h = x[:nH] + 1j * x[nH:]; h = h / np.linalg.norm(h); s = np.sort(np.linalg.svd(B @ h, compute_uv=False))[::-1]; return s, h
def D(x):
    s, _ = svals(x)
    if s[0] <= 0 or s[2] <= 0: return 1e3
    return math.log(s[1] / s[0] / 0.0595) ** 2 + math.log(s[2] / s[0] / 2.88e-4) ** 2
rng = random.Random(33); best = (1e9, None)
starts = sorted(((D(x), x) for x in (np.array([rng.gauss(0, 1) for _ in range(2 * nH)]) for _ in range(300))), key=lambda t: t[0])
for _, x0 in starts[:8]:
    r = minimize(D, x0, method='Nelder-Mead', options=dict(maxiter=6000, xatol=1e-10, fatol=1e-12))
    if r.fun < best[0]: best = (r.fun, r.x)
s, h = svals(best[1])
print(json.dumps(dict(nH=nH, D=float(best[0]), ratios=[float(s[1] / s[0]), float(s[2] / s[0])], Q=float(s.sum() / np.sqrt(s).sum() ** 2),
                      max_mode_overlap=float(np.max(np.abs(h))), weights=list(map(float, np.abs(h))), HOSTS=bool(best[0] < 0.1)), indent=1))
