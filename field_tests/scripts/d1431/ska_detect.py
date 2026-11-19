"""JANUS tick 28: detection significance of SERAPIS's running with 1611.05883 forecasts (see PREREG)."""
import json, sys
A = (-8.4e-4, -1.06e-3)
F = {'S4 (beta=0)': 0.0025, 'S4 (beta free)': 0.0026, 'Planck': 0.0053, 'Planck+WFIRST': 0.0026, 'Planck+DESI': 0.0023, 'Planck+SKA': 9.3e-4}
out = {'combinations': {k: [abs(a)/s for a in A] for k, s in F.items()}, 'sigma_needed_3sigma': [abs(a)/3 for a in A]}
best = max(F, key=lambda k: max(out['combinations'][k]))
out['closest'] = best; out['detectable'] = any(max(v) >= 3 for v in out['combinations'].values())
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
