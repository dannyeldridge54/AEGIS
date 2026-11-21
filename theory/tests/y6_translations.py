"""D1805 numeric check: magnetic translations on M=18 (SS 1/3) surviving the Z3 orbifold; joint classes with the Z3 rotation."""
import numpy as np, math, json, sys
sys.path.insert(0, 'theory/tests')
from z3_modes import theta, z3_classes, TAU
M, a1, a2 = 18, 1/3, 1/3
rng = np.random.default_rng(4); z = rng.uniform(0, 1, 500) + TAU * rng.uniform(0, 1, 500)
def h(zz): return np.array([theta((j + a1) / M, -a2, M * zz, M * TAU) for j in range(M)]).T
H0 = h(z)
_, ev, V, C = z3_classes(M, a1, a2)        # C: psi^j(wz) = sum_i C[j,i] psi^i(z)
res_out = []; surv = []
for p in range(M):
    for q in range(M):
        v = (p + q * TAU) / M
        G = h(z + v) * np.exp(2j * math.pi * q * z)[:, None]
        T = np.linalg.lstsq(H0, G, rcond=None)[0].T   # h^j(z+v) e^{2pi i q z} = sum_i T[j,i] h^i(z)
        r = np.linalg.norm(H0 @ T.T - G) / np.linalg.norm(G)
        res_out.append(r)
        # commutes with Z3 up to a phase?
        A, B = C @ T, T @ C
        k = np.vdot(B.ravel(), A.ravel()) / np.vdot(B.ravel(), B.ravel())
        if np.linalg.norm(A - k * B) / np.linalg.norm(A) < 1e-8 and (p, q) != (0, 0): surv.append((p, q, T))
print('max translation-fit residual %.1e' % max(res_out), ' surviving translations (≠0):', [(p, q) for p, q, _ in surv])
out = dict(max_residual=max(res_out), surviving=[(p, q) for p, q, _ in surv])
if surv:
    T = surv[0][2]
    cls = np.round(np.angle(ev) / (2 * math.pi) * 3) % 3
    dims = []
    for c in range(3):
        idx = np.where(cls == c)[0]; Vc = V[:, idx]
        # restrict T to the class subspace (coefficient vectors are columns of V)
        P = np.linalg.lstsq(Vc, T.T @ Vc, rcond=None)[0]
        w = np.linalg.eigvals(P); ph = np.round((np.angle(w) / (2 * math.pi)) % 1, 4)
        u, cnt = np.unique(ph, return_counts=True); dims.append(dict(cls=c, eig_phases=u.tolist(), dims=cnt.tolist()))
    out['joint'] = dims; print(dims)
json.dump(out, open('field_tests/results/y6_translations.json', 'w'), indent=1, default=str)
# check the commutation phase k: C T = k T C ; k != 1 means T permutes the Z3 classes (non-abelian group)
T = surv[0][2]; A, B = C @ T, T @ C
k = np.vdot(B.ravel(), A.ravel()) / np.vdot(B.ravel(), B.ravel())
print('commutation phase k =', np.round(k, 6), ' arg/2pi =', round(float(np.angle(k) / (2 * math.pi)) % 1, 4))
T3 = np.linalg.matrix_power(T, 3); print('T^3 proportional to identity:', np.linalg.norm(T3 - T3[0, 0] * np.eye(M)) / np.linalg.norm(T3) < 1e-8)
out['k_phase'] = float(np.angle(k) / (2 * math.pi)) % 1
json.dump(out, open('field_tests/results/y6_translations.json', 'w'), indent=1, default=str)
