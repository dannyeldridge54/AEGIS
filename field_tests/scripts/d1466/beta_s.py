"""JANUS tick 62: leading-order beta_s from both derived models (PREREG_D1466)."""
import json, mpmath as mp
G = {}; exec(open('field_tests/scripts/d1449/vac_grid.py').read().split("rows = []")[0], G)
R_, T_, solve = G['R_'], G['T_'], G['solve']; c = T_['c']; mp.mp.dps = 30
def eps_n(V):
    def at(phi):
        v = V; Vp = mp.diff(v, phi, 1)/v(phi); ev1 = Vp**2/2
        ev2f = lambda p: 2*((mp.diff(v, p, 1)/v(p))**2 - mp.diff(v, p, 2)/v(p))
        ev2 = ev2f(phi); ev3 = -mp.diff(ev2f, phi)*Vp/ev2
        ev3f = lambda p: -mp.diff(ev2f, p)*(mp.diff(v, p, 1)/v(p))/ev2f(p)
        ev4 = -mp.diff(ev3f, phi)*Vp/ev3
        return ev1*(1-ev2/3), ev2*(1-ev2/6-ev3/3), ev3*(1-ev2/3-ev4/3), ev4
    return at
def beta(e1, e2, e3, e4): return -(1+e1)*(2*e1*e2*(e2+e3) + e2*e3*(e3+e4))
out = dict(D='D1466')
for name, mod, guess, scale, ns, r in (('rho', R_, (mp.mpf('1.25'), mp.log(mp.mpf('14.6'))/mp.sqrt(2)), mp.mpf('1e-6'), '0.974393', '4.82095e-4'),
                                       ('tau_i', T_, (mp.mpf('1.4'), mp.log(mp.mpf('23.3')+c)/mp.sqrt(2)), mp.mpf('1e-4'), '0.97462', '4.8335e-4')):
    NS, R = mp.mpf(ns), mp.mpf(r)
    F = lambda a, phi: (lambda o: [o[0]-NS, (o[1]-R)*1000])(mod['obs'](phi, a*scale))
    s = mp.findroot(F, guess, tol=1e-18); p = s[0]*scale; phi = s[1]
    al = mod['obs'](phi, p)[2]
    V = (lambda q: mod['V'](q, p))
    e = eps_n(V)(phi); b = beta(*e)
    ref = (1-NS)*al
    out[name] = dict(param=float(p), alpha=float(al), eps=[float(x) for x in e], beta=float(b), beta_D1400_form=float(ref), ratio=float(b/ref))
    print(name, out[name], flush=True)
out['verdict_rho'] = 'D1400 CONFIRMED' if abs(out['rho']['ratio']-1) < 0.10 else 'D1400 NOT CONFIRMED'
json.dump(out, open('field_tests/results/D1466_beta_s.json', 'w'), indent=1); print(out['verdict_rho'])
