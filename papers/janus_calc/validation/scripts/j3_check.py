# AEGIS-FP M4CM5LUGBB3M3DW6 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J3 (locked PREREG_J3): third-order n_s vs D990 references."""
import sys, json, glob, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc import models as J, core
recs = [json.loads(l) for f in sorted(glob.glob('field_tests/results/janus_battery_a_d990.part*.jsonl')) for l in open(f) if l.strip()]
recs = [r for r in recs if r['fam'] != 'stress']; cache = {}; L = []; d2 = []; d3 = []
def mk(r):
    k = (r['fam'], r['spec'])
    if k not in cache:
        p = float(r['spec']); cache[k] = J.serapis_E(p) if r['fam'] == 'SERAPIS-E' else J.serapis_rho(p) if r['fam'] == 'SERAPIS-rho' else J.chronos(p)
    return cache[k]
for r in sorted(recs, key=lambda x: x['i']):
    m = mk(r); s3 = core.spectra3(m, r['N']); a = abs(r['ns_j'] - r['ns_b']); b = abs(s3['ns'] - r['ns_b']); d2.append(a); d3.append(b)
    L.append(f"{r['fam']} {r['spec']} N*={r['N']}: ref {r['ns_b']:.7f} | 2nd {r['ns_j']:.7f} (|d| {a:.1e}) | 3rd {s3['ns']:.7f} (|d| {b:.1e}) | beta_s {s3['beta_s']:.2e}")
    print(L[-1], flush=True)
ok = max(d3) <= 5e-6 and np.median(d3) <= np.median(d2)/3
L.append(f"2nd order median |dns| {np.median(d2):.1e} max {max(d2):.1e}; 3rd order median {np.median(d3):.1e} max {max(d3):.1e} -> {'IMPROVED' if ok else 'NOT IMPROVED'}")
open('field_tests/results/janus_j3_check.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
