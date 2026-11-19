"""D1494: fine grid of the DILMIX strip (PREREG_D1494)."""
import json, numpy as np
M = {}; exec(open('field_tests/scripts/d1485/dilmix_sr.py').read().split("if __name__")[0], M)
out = {"D": "D1494", "grid": []}
for al in np.round(np.arange(0.20, 0.601, 0.05), 3):
    for C in np.round(np.arange(0.8e-6, 2.201e-6, 0.2e-6), 12):
        try: p = M['point'](float(al), float(C))
        except Exception as ex: p = dict(alpha=float(al), C=float(C), error=str(ex)[:80], in_band=False)
        out['grid'].append(p); print(json.dumps(p), flush=True)
        json.dump(out, open('/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1494_strip_edges.json', 'w'), indent=1)
rows = {}
for p in out['grid']:
    if 'error' not in p: rows.setdefault(p['alpha'], []).append(p)
out['per_alpha'] = {}
for al, ps in rows.items():
    ps.sort(key=lambda q: q['C']); C = np.array([q['C'] for q in ps]); ns = np.array([q['ns'] for q in ps]); r = np.array([q['r'] for q in ps])
    c972 = float(np.interp(0.972, ns, C)) if ns.min() <= 0.972 <= ns.max() else None
    inb = [q['C'] for q in ps if q['in_band']]
    out['per_alpha'][str(al)] = dict(C_in_band=inb, C_at_ns972=c972, r_at_ns972=float(np.interp(c972, C, r)) if c972 else None)
json.dump(out, open('/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1494_strip_edges.json', 'w'), indent=1); print('done')
