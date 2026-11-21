import numpy as np, cmath, math, json
rho = cmath.exp(1j * math.pi / 3)
def U(eps): t = rho + eps; return (t - rho) / (t - rho.conjugate())
uu, ud = U(0.00311 * cmath.exp(1j * math.radians(50))), U(0.0457 * cmath.exp(1j * math.radians(49)))
qQ, qu, qd = np.array([1.5, 1, 0]), np.array([.5, 0, 0]), np.array([.5, 0, 0])
Eu, Ed = qQ[:, None] + qu[None, :], qQ[:, None] + qd[None, :]
rng = np.random.default_rng(21); N = 20000
def C(): return np.exp(rng.uniform(math.log(.5), math.log(2), (3, 3))) * np.exp(1j * rng.uniform(0, 2 * math.pi, (3, 3)))
data = dict(mu=(5.58e-6, 2.69e-3), md=(6.86e-4, 1.37e-2), V=(0.2250, 0.0410, 0.00382))
w3 = lambda p, d: max(p / d, d / p) <= 3
rows = []
for _ in range(N):
    Mu = C() * uu ** Eu; Md = C() * ud ** Ed
    Uu, su, _ = np.linalg.svd(Mu); Ud, sd, _ = np.linalg.svd(Md)   # descending
    V = Uu.conj().T @ Ud            # rows: u,c,t (desc) -> reorder to ascending
    V = V[::-1, ::-1]; su, sd = su[::-1], sd[::-1]
    J = (V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])).imag
    a = [su[0] / su[2], su[1] / su[2], sd[0] / sd[2], sd[1] / sd[2], abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2])]
    rows.append(a + [abs(J)])
R = np.array(rows)
ok7 = np.array([w3(r[0], data['mu'][0]) and w3(r[1], data['mu'][1]) and w3(r[2], data['md'][0]) and w3(r[3], data['md'][1]) and all(w3(r[4 + k], data['V'][k]) for k in range(3)) for r in R])
f7 = float(ok7.mean()); J7 = R[ok7, 7]
fJ = float(np.mean([w3(j, 3.08e-5) for j in J7])) if len(J7) else 0.0
# delta from J and |V|s: sin(delta) = J / (s12 c12 s23 c23 s13 c13^2)
s12, s23, s13 = R[ok7, 4], R[ok7, 5], R[ok7, 6]
sd_ = J7 / (s12 * np.sqrt(1 - s12 ** 2) * s23 * np.sqrt(1 - s23 ** 2) * s13 * (1 - s13 ** 2))
out = dict(u_u=[abs(uu), math.degrees(cmath.phase(uu))], u_d=[abs(ud), math.degrees(cmath.phase(ud))], f7=f7, n7=int(ok7.sum()),
           median_J=float(np.median(J7)) if len(J7) else None, fJ=fJ, median_sin_delta=float(np.median(np.clip(sd_, 0, 1))) if len(J7) else None,
           verdict_matrix='PASS' if f7 >= 0.05 else 'FAIL', verdict_CP='PASS' if fJ >= 0.2 else 'FAIL',
           medians_all=dict(zip(['mu/mt', 'mc/mt', 'md/mb', 'ms/mb', 'Vus', 'Vcb', 'Vub', 'J'], map(float, np.median(R, axis=0)))))
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1829_cp.json', 'w'), indent=1)
