"""JANUS tick 59: split derived/LO into offset and SR-order factors per vacuum (PREREG_D1463)."""
import json, math
from scipy.optimize import fsolve
c = math.log(1728)/(2*math.pi)
def eqs(v, ns, r):
    u, x = v; return [8*u*u*((2-x)+c*u*(5-x)) - (1-ns), 64*u**4*(1+x)**2*(1+2*c*u) - r]
def a640(u, x): return -32*u**4*(1+x)*((4+x)+c*u*(23+2*x))
def lo_half(ns, r):
    q = 2*math.sqrt(2)*math.sqrt(r/2)/(1-ns); return -0.5*(1-ns)**2*q*(1+0.5*(q-1))
ns, r = 0.97462, 4.8335e-4
(u, x) = fsolve(eqs, (0.06, 0.5), args=(ns, r), xtol=1e-14)
d48 = json.load(open('field_tests/results/D1448_tau_i_exact_plateau.json'))['rows'][2]['alpha']
LOi, CFi = lo_half(ns, r), a640(u, x)
tau = dict(LO=LOi, closed=CFi, derived=d48, offset_factor=CFi/LOi-1, sr_factor=d48/CFi-1, total=d48/LOi-1,
           check=abs((CFi/LOi)*(d48/CFi)-d48/LOi))
d39 = json.load(open('field_tests/results/D1439_rho_closed_form.json'))
R = 4.82095e-4; LOr = -2*R; CFr = d39['alpha_cf']; d42 = json.load(open('field_tests/results/D1442_rho_second_order.json'))['second']['alpha']
rho = dict(LO=LOr, closed=CFr, derived=d42, plateau_piece=d39['plateau_piece'], offset_piece=d39['offset_piece'],
           offset_factor=CFr/LOr-1, sr_factor=d42/CFr-1, total=d42/LOr-1, check=abs((CFr/LOr)*(d42/CFr)-d42/LOr))
ok = tau['check'] < 1e-12 and rho['check'] < 1e-12
out = dict(D='D1463', tau_i=tau, rho=rho, verdict='computed' if ok else 'no result')
json.dump(out, open('field_tests/results/D1463_correction_split.json', 'w'), indent=1); print(json.dumps(out, indent=1))
