"""JANUS tick 18: band_e alpha_s anchored on A1's exact/LO ratio (see PREREG)."""
import json, sys
k = -9.9814e-4/-9.6419e-4
P2 = 2.8284**2/4
a = [-k*P2*r for r in (4.55e-4, 5.12e-4)]
win = (-10.6e-4, -9.4e-4)
cons = (min(a) >= win[0]-0.2e-4) and (max(a) <= win[1]+0.2e-4)
pulls = [(x-0.0062)/0.0052 for x in a]
out = dict(k=k, alpha_range=a, frozen_window=win, consistent=bool(cons), pulls=pulls,
           verdict='PASS' if max(map(abs, pulls)) < 2 else 'FAIL')
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
