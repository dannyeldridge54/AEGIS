import json, sys
A = (-9.087e-4, -1.0139e-3); D = {'P-ACT': (0.0060, 0.0055), 'P-ACT-LB': (0.0062, 0.0052)}
out = {k: [(a-m)/s for a in A] for k, (m, s) in D.items()}
out['verdict'] = 'PASS' if all(abs(p) < 2 for v in out.values() for p in v) else 'FAIL'
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
