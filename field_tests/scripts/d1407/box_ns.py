"""JANUS tick 6: band_e_audited n_s/r vs end-2025 data (see PREREG)."""
import json, sys
NS = (0.9717, 0.9760); RMAX = 4.90e-4
d = {'cmb_desi': (0.9728, 0.0029), 'cmb': (0.9682, 0.0032)}
g = [NS[0]+(NS[1]-NS[0])*i/1000 for i in range(1001)]
out = {}
for k, (m, s) in d.items():
    f = sum(abs((x-m)/s) < 2 for x in g)/1001
    out[k] = dict(pulls=[(NS[0]-m)/s, (NS[1]-m)/s], frac_in_2sigma=f, rule='PASS' if f == 1 else ('PARTIAL' if f > 0 else 'FAIL'))
out['R3'] = 'PASS' if RMAX < 0.034 else 'FAIL'
out['verdict'] = 'PASS' if out['cmb_desi']['rule'] == 'PASS' and out['R3'] == 'PASS' else out['cmb_desi']['rule']
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
