"""PROM-1 cycle 1 goalposts P1-P4, run once as locked."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
Ea = F.two_body_split('DT')[1]; t0 = time.time()
a = F.operating_point(F.ITER, Ea); b = F.operating_point(F.ITER_400, Ea)
keys = ('P_fus', 'Q', 'tau_E', 'W_MJ', 'beta_N', 'P_loss', 'P_LH', 'P_rad', 'P_rad_core', 'Te_avg', 'Ti_avg', 'Te0', 'ne0', 'f_He', 'Zeff', 'f_G', 'he_iterations')
w = lambda x, c, tol: abs(x / c - 1) <= tol
P1 = dict({k: a[k] for k in keys}); P1['pass_'] = bool(w(a['P_fus'], 500, .2) and w(a['tau_E'], 3.4, .15) and w(a['W_MJ'], 353, .15) and w(a['beta_N'], 2.0, .15) and a['P_loss'] >= a['P_LH'])
P2 = dict({k: b[k] for k in keys}); P2['pass_'] = bool(w(b['P_fus'], 400, .2) and w(b['tau_E'], 3.7, .15) and w(b['Q'], 10, .3))
P3 = dict(f_He_500=a['f_He'], f_He_400=b['f_He'], pass_=bool(0.02 <= a['f_He'] <= 0.05 and 0.02 <= b['f_He'] <= 0.05))
prev = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'fusion1_rerun.json')))['G5_G6_DEV7']
dist = lambda o, col: sum(abs(o[k] / v - 1) for k, v in col.items())
col500 = dict(P_fus=500, tau_E=3.4, W_MJ=353, beta_N=2.0)
acc = dict(dist_500_before=dist(prev, col500), dist_500_after=dist(a, col500))
acc['accept'] = bool(acc['dist_500_after'] < acc['dist_500_before'])
r = dict(P1=P1, P2_heldout=P2, P3=P3, accept_rule=acc, seconds=round(time.time() - t0, 2))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom1.json'); json.dump(r, open(out, 'w'), indent=1, default=str)
for k in ('P1', 'P2_heldout'): print(k, {x: (round(v, 3) if isinstance(v, float) else v) for x, v in r[k].items()})
print('P3', r['P3'], '\naccept', acc, r['seconds'], 's')
