"""D1925: can ONE spurion (shared step u for up and down) carry the quark lock? Tests D1923 point 8 ("two sizes needed").
Same charge grid and filters as D1828, same naturalness method and bars as D1829, but uu = ud = u."""
import itertools, json, math, cmath, sys, numpy as np
rho = cmath.exp(1j * math.pi / 3)
def U(eps): t = rho + eps; return (t - rho) / (t - rho.conjugate())
Qg = [0, .5, 1, 1.5, 2, 2.5, 3]
mu = (5.58e-6, 2.69e-3); md = (6.86e-4, 1.37e-2); V = dict(us=0.2250, cb=0.0410, ub=0.00382)
w2 = lambda p, d: max(p / d, d / p) <= 2
w3 = lambda p, d: max(p / d, d / p) <= 3
def scan(a):
    fits = []
    for qQ1, qQ2, qu1, qu2, qd1, qd2 in itertools.product(Qg, repeat=6):
        if not (w2(a ** (qQ1 + qu1), mu[0]) and w2(a ** (qQ2 + qu2), mu[1]) and w2(a ** (qQ1 + qd1), md[0]) and w2(a ** (qQ2 + qd2), md[1])): continue
        if w3(a ** abs(qQ1 - qQ2), V['us']) and w3(a ** qQ2, V['cb']) and w3(a ** qQ1, V['ub']):
            fits.append(((qQ1, qQ2, 0), (qu1, qu2, 0), (qd1, qd2, 0)))
    return fits
def natural(u, qQ, qu, qd, N=5000, seed=25):
    rng = np.random.default_rng(seed); qQ, qu, qd = map(np.array, (qQ, qu, qd))
    Eu, Ed = qQ[:, None] + qu[None, :], qQ[:, None] + qd[None, :]
    C = lambda: np.exp(rng.uniform(math.log(.5), math.log(2), (3, 3))) * np.exp(1j * rng.uniform(0, 2 * math.pi, (3, 3)))
    ok = 0; okJ = 0
    for _ in range(N):
        Mu = C() * u ** Eu; Md = C() * u ** Ed
        Uu, su, _ = np.linalg.svd(Mu); Ud, sd, _ = np.linalg.svd(Md)
        Vm = (Uu.conj().T @ Ud)[::-1, ::-1]; su, sd = su[::-1], sd[::-1]
        J = abs((Vm[0, 1] * Vm[1, 2] * np.conj(Vm[0, 2]) * np.conj(Vm[1, 1])).imag)
        a = [su[0] / su[2], su[1] / su[2], sd[0] / sd[2], sd[1] / sd[2], abs(Vm[0, 1]), abs(Vm[1, 2]), abs(Vm[0, 2])]
        d = [mu[0], mu[1], md[0], md[1], V['us'], V['cb'], V['ub']]
        if all(w3(x, y) for x, y in zip(a, d)): ok += 1; okJ += w3(J, 3.08e-5)
    return ok / N, (okJ / ok if ok else 0.0)
u = U(0.0457 * cmath.exp(1j * math.radians(49)))      # the D1828/D1829 down step, |u| = 0.0259, NOT re-tuned
out = {}
for tag, a in (('primary_u_d', abs(u)), ('report_u_u', 1.793e-3), ('report_0.1', 0.1)):
    fits = scan(a); res = []
    for f in fits:
        f7, fJ = natural(u if tag == 'primary_u_d' else a, *f); res.append(dict(qQ=f[0], qu=f[1], qd=f[2], f7=f7, fJ=fJ))
    res.sort(key=lambda r: -r['f7']); out[tag] = dict(abs_u=a, n_fit=len(fits), frac=len(fits) / 7 ** 6, best=res[:5])
p = out['primary_u_d']; b = p['best'][0] if p['best'] else None
out['verdict'] = 'PASS' if b and b['f7'] >= 0.05 and b['fJ'] >= 0.2 else ('FIT-NOT-NATURAL' if b else 'NONE')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1925_onespurion.json', 'w'), indent=1)
