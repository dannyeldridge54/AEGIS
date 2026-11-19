"""JANUS tick 44: tau=i exact plateau (V = 1 - 1/(I^2+1) + eps I/2, phi = ln(I+c)/sqrt2) at second-order SR (see PREREG_D1448)."""
import json, mpmath as mp
mp.mp.dps = 30
c = mp.log(1728)/(2*mp.pi); Cc = mp.euler + mp.log(2) - 2
def V(phi, e):
    I = mp.e**(mp.sqrt(2)*phi) - c; return 1 - 1/(I**2 + 1) + e*I/2
def obs(phi, e):
    v = lambda p: V(p, e)
    d = [mp.diff(v, phi, n) for n in range(4)]
    Vp = d[1]/d[0]; ev1 = Vp**2/2
    ev2f = lambda p: 2*((mp.diff(v, p, 1)/v(p))**2 - mp.diff(v, p, 2)/v(p))
    ev2 = ev2f(phi); ev3 = -mp.diff(ev2f, phi)*Vp/ev2
    ev3f = lambda p: -mp.diff(ev2f, p)*(mp.diff(v, p, 1)/v(p))/ev2f(p)
    ev4 = -mp.diff(ev3f, phi)*Vp/ev3
    e1 = ev1*(1-ev2/3); e2 = ev2*(1-ev2/6-ev3/3); e3 = ev3*(1-ev2/3-ev4/3); e4 = ev4
    ns = 1-2*e1-e2-(3+2*Cc)*e1*e2-2*e1**2-Cc*e2*e3; r = 16*e1*(1+Cc*e2)
    a = -(1+e1)*(2*e1*e2+e2*e3)-(3+2*Cc)*e1*e2*(e2+e3)-4*e1**2*e2-Cc*e2*e3*(e3+e4)
    V0 = d[0]; eps = 0.5*(d[1]/V0)**2; eta = d[2]/V0; xi = d[1]*d[3]/V0**2
    return ns, r, a, dict(ns=1-6*eps+2*eta, r=16*eps, a=16*eps*eta-24*eps**2-2*xi)
PTS = [('1.30e-4','0.97368','4.6846e-4','-8.454e-4'), ('1.35e-4','0.97415','4.7584e-4','-8.501e-4'), ('1.40e-4','0.97462','4.8335e-4','-8.543e-4'),
       ('1.45e-4','0.97509','4.9100e-4','-8.587e-4'), ('1.50e-4','0.97556','4.9878e-4','-8.635e-4')]
rows = []
for e0, ns0, r0, a0 in PTS:
    NS, R, AE, E0 = mp.mpf(ns0), mp.mpf(r0), mp.mpf(a0), mp.mpf(e0)
    def F(e4, phi):
        o = obs(phi, e4*mp.mpf('1e-4')); return [o[0]-NS, (o[1]-R)*1000]
    s = mp.findroot(F, (E0*1e4, mp.log(mp.mpf('17.0')+c)/mp.sqrt(2)), tol=1e-18)
    ns, r, a, f = obs(s[1], s[0]*mp.mpf('1e-4'))
    eps_s = float(s[0])*1e-4
    rows.append(dict(eps_NA12=float(E0), eps_solved=eps_s, impl_ok=abs(eps_s/float(E0)-1) < 0.1,
                     I_star=float(mp.e**(mp.sqrt(2)*s[1])-c), alpha=float(a), alpha_exact=float(AE), err=float(a/AE-1),
                     first_order_alpha_same_point=float(f['a']), err_first=float(f['a']/AE-1)))
    print(rows[-1], flush=True)
out = dict(D='D1448', c=float(c), rows=rows, max_abs_err=max(abs(x['err']) for x in rows))
out['verdict'] = 'no result' if not all(x['impl_ok'] for x in rows) else ('PASS' if out['max_abs_err'] < 0.003 else 'FAIL')
json.dump(out, open('field_tests/results/D1448_tau_i_exact_plateau.json', 'w'), indent=1); print(out['verdict'], out['max_abs_err'])
