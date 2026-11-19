"""D1480 (L1): convert both vacua's predictions from k = 0.05 to k = 0.002 Mpc^-1 (PREREG_D1480)."""
import json, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
R_, T_, solve = G['R_'], G['T_'], G['solve']
mp.mp.dps = 30
L = mp.log(mp.mpf('0.002') / mp.mpf('0.05'))
beta = json.load(open('field_tests/results/D1466_beta_s.json'))
def follow(Vf, obsf, phi, p, target):
    # integrate back in time (towards larger phi): dphi/dN = V'/V, dlnk = (1 - eps1) dN; RK4 in N
    lnk, h = mp.mpf(0), mp.mpf('0.01')
    def rhs(ph): return mp.diff(lambda q: Vf(q, p), ph) / Vf(ph, p)
    while lnk < target:
        e1 = rhs(phi) ** 2 / 2
        step = min(h, (target - lnk) / (1 - e1))
        k1 = rhs(phi); k2 = rhs(phi + step * k1 / 2); k3 = rhs(phi + step * k2 / 2); k4 = rhs(phi + step * k3)
        phi += step * (k1 + 2 * k2 + 2 * k3 + k4) / 6; lnk += step * (1 - e1)
    return phi
out = {"D": "D1480", "L": float(L)}
for name, mod, guess, scale, NS, R, bkey in (
        ("rho_A1", R_, (mp.mpf('1.2'), mp.log(mp.mpf('14.6')) / mp.sqrt(2)), mp.mpf('1e-6'), mp.mpf('0.974393'), mp.mpf('4.82095e-4'), "rho"),
        ("tau_i_NA12", T_, (mp.mpf('1.4'), mp.log(mp.mpf('23.3') + T_['c']) / mp.sqrt(2)), mp.mpf('1e-4'), mp.mpf('0.97462'), mp.mpf('4.8335e-4'), "tau_i")):
    F = lambda a, phi: (lambda o: [o[0] - NS, (o[1] - R) * 1000])(mod['obs'](phi, a * scale))
    s = mp.findroot(F, guess, tol=1e-18); p, phi_s = s[0] * scale, s[1]
    o = mod['obs'](phi_s, p); ns, r, a = o[0], o[1], o[2]
    phi2 = follow(mod['V'], mod['obs'], phi_s, p, -L)
    o2 = mod['obs'](phi2, p)
    b = beta[bkey]['beta']
    tay_ns = float(ns + a * L + b * L ** 2 / 2); tay_a = float(a + b * L)
    out[name] = dict(param=float(p), phi_star=float(phi_s), phi_002=float(phi2), dphi=float(phi2 - phi_s),
                     k005=dict(ns=float(ns), r=float(r), alpha=float(a)),
                     exact_k0002=dict(ns=float(o2[0]), r=float(o2[1]), alpha=float(o2[2])),
                     taylor_k0002=dict(ns=tay_ns, alpha=tay_a, beta_used=b),
                     gap_ns=float(o2[0]) - tay_ns, gap_alpha=float(o2[2]) - tay_a)
    out[name]['verdict'] = 'CONSISTENT' if abs(out[name]['gap_ns']) < 5e-5 else 'TAYLOR GAP'
    print(name, json.dumps(out[name]), flush=True)
json.dump(out, open('field_tests/results/D1480_pivot.json', 'w'), indent=1)
