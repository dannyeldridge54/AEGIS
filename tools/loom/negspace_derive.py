"""D2139: derive N13 (dS slope today), N4 (tau_q decay T), N3 (mu -> e gamma). See PREREG_D2139."""
import json, math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'weave_cm_v5')); os.environ.setdefault('WEAVE_DATA', '/tmp/claude-0/cobaya_pkgs/data/')
import weave_engine as W
p = json.load(open('field_tests/weave_lcdm/knob_dovekie.json'))['0.0']['p']
bg = W.background(p[0], p[1], math.exp(p[2]), p[3], 0.0)
phi = bg['phi']; u = W.A*__import__('numpy').exp(-W.BETA*phi); sl = W.BETA*u/(1 - u)
n13 = dict(u_i=p[3], u_today=float(u[-1]), slope_today=float(sl[-1]), slope_min_path=float(sl.min()))
n13['verdict'] = 'PASS' if n13['slope_today'] >= math.sqrt(2/3) else ('MARGINAL' if n13['slope_today'] >= 0.5 else 'FAIL')
MP, m, gs = 2.435e18, 2e10, 106.75
def Td(G): return (90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
G1 = m**3/(4*math.pi*MP**2); G2 = G1/(8*math.pi)
n4 = dict(T_d_GeV=[Td(G1), Td(G2)]); n4['verdict'] = 'PASS' if min(n4['T_d_GeV']) >= 5e-3 else 'FAIL'
a, GF, ms, tb = 1/137.036, 1.1664e-5, 2.5e5, 4.0
br1 = a**3*math.pi/GF**2/ms**4*tb**2
n3 = dict(BR_delta1=br1, delta12_max=math.sqrt(1.5e-13/br1)); n3['verdict'] = 'PASS' if br1 < 1.5e-13 else 'FAIL'
out = dict(N13=n13, N4=n4, N3=n3); print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/d2139_negspace_derive.json', 'w'), indent=1)
