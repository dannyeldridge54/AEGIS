"""D1510: DILMIX in-band search in the physical frame (PREREG_D1510). Usage: python3 phys_inband.py <half: 0|1>"""
import json, sys
G = {}; exec(open('field_tests/scripts/d1506/phys_ns.py').read().split('out = {')[0], G)
half = int(sys.argv[1]); lam = 1 / 9930.90
alphas = [0.05, 0.075, 0.1, 0.125] if half == 0 else [0.15, 0.175, 0.2]
Cs = [1.3e-6, 1.4e-6, 1.5e-6, 1.6e-6, 1.7e-6, 1.8e-6, 1.9e-6, 2.0e-6]
out = {"D": "D1510", "half": half, "grid": []}
f = f'/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1510_half{half}.json'
for al in alphas:
    for C in Cs:
        try:
            p = G['point'](al, C, lam); p['in_band'] = bool(0.969 <= p['ns'] <= 0.975 and 4.55e-4 <= p['r'] <= 5.7e-4)
        except Exception as ex:
            p = dict(alpha=al, C=C, error=str(ex)[:80], in_band=False)
        out['grid'].append(p); print(json.dumps(p), flush=True); json.dump(out, open(f, 'w'), indent=1)
print('done')
