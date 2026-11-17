import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import galaxy as G, fast, jfactor as J
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True)); ok = {}
rel = lambda a, b: abs(a - b)/abs(b) if b != 0 else abs(a)
n = 200; r = np.random.default_rng(11)
ph = r.uniform(-0.37, 0.37, n); Rg = 8.0 + r.uniform(-3, 3, n); zg = r.uniform(-0.5, 0.5, n)
x, y = -Rg*np.cos(ph), Rg*np.sin(ph); vR, vphi, vz = r.normal(0, 35, n), r.uniform(220, 232, n) + r.normal(0, 25, n), r.normal(0, 20, n)
er, ep = np.array([x, y])/Rg, np.array([-y, x])/Rg; ep = -ep if (ep[1, 0] < 0 and x[0] < 0) else ep
P_, V_ = np.array([x, y, zg]), np.array([vR*er[0] + vphi*ep[0], vR*er[1] + vphi*ep[1], vz])
fref = {0.66: 0.19, 1.0: 0.24, 1.85: 0.18}; fpred = {0.66: 0.14, 1.0: 0.26, 1.85: 0.67}  # ARCHIVAL D732 values; current = D784 thermal (D1153); Jref = 4.413e21
def chain(s):
    p = dict(G.params()); p['hamp'] *= s; mw = G.MW(p)
    o = fast.orbits_fast(*P_, *V_, mw=mw)
    stats = dict(zmax=float(np.median(o['zmax'])), ecc=float(np.median(o['ecc'])), rapo=float(np.median(o['rapo'])))
    rho = G.natural_to_rho_GeVcm3(mw.rho_halo(1.0))
    Jv = J.J_route_B(J.normalise(J.nfw(16.0), rho, 8.0), 8.0)
    fmax = {M: fref[M]*math.sqrt(Jref/Jv) for M in fref}
    return dict(mw=mw, o=o, stats=stats, rho=rho, J=Jv, fmax=fmax, vc=G.vcirc_array(mw, np.array([1.0]))[0]*220)
res = {s: chain(s) for s in (0.8, 0.9, 1.0, 1.1, 1.2)}
# W2a lossless
c = res[1.0]; mw = c['mw']
d_rho = G.natural_to_rho_GeVcm3(mw.rho_halo(1.0)); d_J = J.J_route_B(J.normalise(J.nfw(16.0), d_rho, 8.0), 8.0)
d_o = fast.orbits_fast(*P_, *V_, mw=mw)
e = max(rel(c['rho'], d_rho), rel(c['J'], d_J), max(float(np.max(np.abs(c['o'][k]/d_o[k] - 1))) for k in ('rperi', 'rapo', 'zmax', 'ecc')))
ok['W2a'] = e <= 1e-12; P(f'W2a wired vs direct: {e:.1e}')
c2 = chain(1.0); e2 = max(rel(c2['rho'], c['rho']), rel(c2['J'], c['J']), max(rel(c2['stats'][k], c['stats'][k]) for k in c['stats']))
ok['W2b'] = e2 <= 1e-12; P(f'W2b closure (second pass): {e2:.1e}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if x_ else "FAIL"}' for k, x_ in ok.items()), '-> W2', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
for s, c in res.items():
    passes = ' '.join(f'{M}TeV:{"PASS" if fpred[M] <= c["fmax"][M] else "FAIL"}({c["fmax"][M]:.2f})' for M in fref)
    P(f'W2c s={s}: v_c(8kpc)={c["vc"]:.1f} km/s rho_sun={c["rho"]:.4f} GeV/cm3 J={c["J"]:.3e} | median z_max={c["stats"]["zmax"]:.4f} kpc e={c["stats"]["ecc"]:.4f} r_apo={c["stats"]["rapo"]:.3f} | wino {passes}')
dz = (res[1.2]['stats']['zmax'] - res[0.8]['stats']['zmax'])/res[1.0]['stats']['zmax']
P(f'W2c Mapper response: median z_max changes by {dz:+.2%} for halo amplitude 0.8 -> 1.2 (orbit precision 1e-3): {"measurable in principle" if abs(dz) > 1e-2 else "weak"}')
open('field_tests/results/wiring_w2.txt', 'w').write('\n'.join(out) + '\n')
