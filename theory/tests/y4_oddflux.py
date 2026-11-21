"""Y4 (locked PREREG_Y4_ODDFLUX): M=9 (1/6) x M=9 (1/6) -> M=18 (1/3) Z3 Yukawas at tau=omega."""
import numpy as np, math, json, sys
sys.path.insert(0, 'theory/tests')
from z3_modes import modes, z3_classes, w, TAU
rng = np.random.default_rng(3)
z = rng.uniform(0, 1, 900) + TAU * rng.uniform(0, 1, 900)
L = modes(9, 1/6, 1/6, z); H = modes(18, 1/3, 1/3, z)
P = np.einsum('pi,pj->pij', L, L).reshape(len(z), -1)
c, *_ = np.linalg.lstsq(H, P, rcond=None)
res_prod = np.linalg.norm(H @ c - P) / np.linalg.norm(P)
c = c.T.reshape(9, 9, 18)
resL, evL, VL, _ = z3_classes(9, 1/6, 1/6); resH, evH, VH, _ = z3_classes(18, 1/3, 1/3)
print('gate: product residual %.1e, Z3 residual L %.1e H %.1e' % (res_prod, resL, resH))
gate = res_prod < 1e-8 and resL < 1e-8 and resH < 1e-8
def cls(ev): return np.round((np.angle(ev) / (2 * math.pi) * 3)) % 3
cL, cH = cls(evL), cls(evH)
print('H classes', {int(k): int((cH == k).sum()) for k in range(3)})
# coefficients in eigenbases: mode_i = sum_a VL[i,a] * eig_a  => psi(eig_a) = sum_i Vinv[a,i] psi_i
VLi = np.linalg.inv(VL); VHi = np.linalg.inv(VH)
# product of eigenmodes a,b = sum_ij VLi[a,i]VLi[b,j] psi_i psi_j = sum_k (...) psi_H_k ; psi_H_k = sum_c VH[k,c] eigH_c
ce = np.einsum('ia,jb,ijk,ck->abc', VL, VL, c, VHi)
t1, t2 = 4.84e-3, 5.95e-2
out = {'gate': bool(gate), 'res_prod': float(res_prod), 'pairs': []}
hrng = np.random.default_rng(7)
for a in range(3):
  for b in range(3):
    ia, ib = np.where(cL == a)[0], np.where(cL == b)[0]
    sub = ce[np.ix_(ia, ib, range(18))]
    norms = [np.linalg.norm(sub[:, :, np.where(cH == k)[0]]) for k in range(3)]
    k = int(np.argmax(norms)); ih = np.where(cH == k)[0]
    leak = sorted(norms)[1] / max(norms); out.setdefault('leak', []).append(float(leak))
    T = sub[:, :, ih]
    h = hrng.normal(size=(20000, len(ih))) + 1j * hrng.normal(size=(20000, len(ih)))
    h /= np.linalg.norm(h, axis=1, keepdims=True)
    Y = np.einsum('ijk,nk->nij', T, h)
    s = np.linalg.svd(Y, compute_uv=False)[:, ::-1]  # ascending
    r12, r23 = s[:, 0] / s[:, 1], s[:, 1] / s[:, 2]
    ok = (np.abs(np.log(r12 / t1)) < math.log(3)) & (np.abs(np.log(r23 / t2)) < math.log(3))
    best = np.argmin(np.log(r12 / t1) ** 2 + np.log(r23 / t2) ** 2)
    row = dict(L=a, R=b, H=k, H_dim=len(ih), norms=[float(x) for x in norms], frac=float(ok.mean()),
               best=[float(r12[best]), float(r23[best])], median=[float(np.median(r12)), float(np.median(r23))])
    out['pairs'].append(row); print(row)
fr = max(p['frac'] for p in out['pairs'])
gate = gate and max(out['leak']) < 1e-8
out['verdict'] = 'NULL-gate' if not gate else ('PASS' if fr >= 0.01 else 'WEAK' if fr > 0 else 'FAIL')
print('verdict', out['verdict'], 'max frac', fr)
json.dump(out, open('field_tests/results/y4_oddflux.json', 'w'), indent=1)
