import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import neutron_birth as NB, fusion as F
rows = []
for T in (5.0, 10.0, 20.0):
    m = NB.spectrum(T); b = NB.ballabio(T); rows.append(dict(m, ball_shift=b['shift_keV'], ball_FWHM=b['FWHM_keV'],
        r_shift=m['shift_keV'] / b['shift_keV'] - 1, r_FWHM=m['FWHM_keV'] / b['FWHM_keV'] - 1))
u = NB.spectrum(10.0, weighted=False); b10 = NB.ballabio(10.0)
G = dict(B1=all(abs(r['r_shift']) <= .05 for r in rows), B2=all(abs(r['r_FWHM']) <= .02 for r in rows),
         B3=abs(u['shift_keV'] / b10['shift_keV'] - 1) > .20, B4=abs(NB.E0 - F.two_body_split('DT')[0]) * 1e3 <= 1.0)
res = dict(goals=G, rows=rows, unweighted_10keV=u, E0_MeV=NB.E0, E0_S1=F.two_body_split('DT')[0])
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n1_birth.json'), 'w'), indent=1, default=float)
print(G); [print({k: round(float(v), 4) for k, v in r.items()}) for r in rows]; print('unweighted', {k: round(float(v), 3) for k, v in u.items()}, 'E0', NB.E0, res['E0_S1'])
