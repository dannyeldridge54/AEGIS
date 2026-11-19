"""JANUS tick 20: band_e_audited alpha_s A1-anchored vs D1262 computed (see PREREG)."""
import json, sys
k = -9.9814e-4/-9.6419e-4; P2 = 2.8284**2/4
r = (4.389e-4, 4.897e-4); comp = (-9.11e-4, -10.14e-4)
a = [-k*P2*x for x in r]
dev = [a[i]/comp[i]-1 for i in range(2)]
pulls = [(x-0.0062)/0.0052 for x in a]
out = dict(k=k, alpha_anchored=a, alpha_D1262=comp, rel_dev=dev, consistent=bool(max(map(abs, dev)) < 0.02),
           pulls=pulls, verdict='PASS' if max(map(abs, pulls)) < 2 else 'FAIL')
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
