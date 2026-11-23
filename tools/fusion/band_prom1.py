"""PROM-1 DEV-1/DEV-2: accept rule on both columns, and the Lux-band report."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
Ea = F.two_body_split('DT')[1]
old = dict(F.ITER, profile='parabolic', he_selfconsistent=False); old400 = dict(F.ITER_400, profile='parabolic', he_selfconsistent=False)
d = lambda o, col: sum(abs(o[k] / v - 1) for k, v in col.items()) if o else float('inf')
c5, c4 = dict(P_fus=500, tau_E=3.4, W_MJ=353, beta_N=2.0), dict(P_fus=400, tau_E=3.7)
new5, new4, o5, o4 = F.operating_point(F.ITER, Ea), F.operating_point(F.ITER_400, Ea), F.operating_point(old, Ea), F.operating_point(old400, Ea)
acc = dict(d500_before=d(o5, c5), d500_after=d(new5, c5), d400_before=d(o4, c4), d400_after=d(new4, c4))
acc['accept'] = acc['d500_after'] < acc['d500_before'] and acc['d400_after'] < acc['d400_before']
band = []
for C3 in (0.5, 0.6, 0.7):
    for rc in (0.7, 0.75, 0.8):
        a = F.operating_point(dict(F.ITER, rad_C3=C3, rho_core=rc), Ea); b = F.operating_point(dict(F.ITER_400, rad_C3=C3, rho_core=rc), Ea)
        band.append(dict(C3=C3, rho_core=rc, tau500=a['tau_E'], Pf500=a['P_fus'], tau400=b['tau_E'], Pf400=b['P_fus']))
r = dict(accept=acc, band=band, tau500_range=[min(x['tau500'] for x in band), max(x['tau500'] for x in band)], tau400_range=[min(x['tau400'] for x in band), max(x['tau400'] for x in band)])
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom1_band.json'), 'w'), indent=1); print(json.dumps({k: r[k] for k in ('accept', 'tau500_range', 'tau400_range')}, indent=1))
