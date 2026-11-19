import json, sys
P = {'tau_i_NA12': (0.97462, 4.8335e-4, -8.543e-4), 'rho_A1': (0.974393, 4.82095e-4, -9.9814e-4)}
NS = {'CMB': (0.9682, 0.0032), 'CMB+DESI': (0.9728, 0.0029), 'P-ACT-LB2-BK18': (0.9752, 0.0030)}
AS = {'P-ACT': (0.0060, 0.0055), 'P-ACT-LB': (0.0062, 0.0052)}
out = {}
for k, (ns, r, a) in P.items():
    d = {f'ns_{c}': (ns-m)/s for c, (m, s) in NS.items()}
    d.update({f'as_{c}': (a-m)/s for c, (m, s) in AS.items()}); d['r_ok'] = r < 0.034
    ruled = [d['ns_CMB+DESI'], d['ns_P-ACT-LB2-BK18'], d['as_P-ACT'], d['as_P-ACT-LB']]
    d['verdict'] = 'PASS' if all(abs(x) < 2 for x in ruled) and d['r_ok'] else 'FAIL'
    out[k] = d
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, d in out.items(): print(k, {kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in d.items()})
