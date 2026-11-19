"""D1509: DILMIX in-band search in the physical frame (PREREG_D1509). Usage: python3 phys_inband.py <half: 0|1>"""
import json, sys
G = {}; exec(open('field_tests/scripts/d1506/phys_ns.py').read().split('out = {')[0], G)
half = int(sys.argv[1]); lam = 1 / 9930.90
alphas = [0, 0.125, 0.25, 0.375, 0.5] if half == 0 else [0.625, 0.75, 0.875, 1.0]
Cs = [1e-6, 2e-6, 3e-6, 4e-6, 6e-6, 8e-6, 12e-6, 16e-6]
out = {"D": "D1509", "half": half, "grid": []}
f = f'/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1509_half{half}.json'
for al in alphas:
    for C in Cs:
        try:
            p = G['point'](al, C, lam); p['in_band'] = bool(0.969 <= p['ns'] <= 0.975 and 4.55e-4 <= p['r'] <= 5.7e-4)
        except Exception as ex:
            p = dict(alpha=al, C=C, error=str(ex)[:80], in_band=False)
        out['grid'].append(p); print(json.dumps(p), flush=True); json.dump(out, open(f, 'w'), indent=1)
print('done')
