"""JANUS tick 75: derived points vs SPT-3G D1 (2506.20707) n_s, Tables I and VI, 68 % (PREREG_D1472)."""
import json
T = {'SPT-3G D1': (0.951, 0.011), 'SPT+ACT': (0.9671, 0.0058), 'SPT+Planck': (0.9636, 0.0035), 'CMB-SPA': (0.9679, 0.0033),
     'SPT-3G D1+DESI': (0.949, 0.012), 'CMB-SPA+DESI': (0.9726, 0.0028)}
P = {'rho_A1': 0.974393, 'tau_i_NA12': 0.97462}
out = dict(D='D1472', pulls={p: {k: (v-c)/s for k, (c, s) in T.items()} for p, v in P.items()}, running='not reached (text truncated at 300k of 375k chars)')
mx = max(abs(x) for d in out['pulls'].values() for x in d.values()); out['max_abs_pull'] = mx
out['verdict'] = 'PASS' if mx < 2 else 'FAIL'
json.dump(out, open('field_tests/results/D1472_spt3g.json', 'w'), indent=1); print(json.dumps(out, indent=1))
