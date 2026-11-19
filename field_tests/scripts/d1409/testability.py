"""JANUS tick 8: detection / exclusion significance of the forced-negative running vs 2030 forecasts (see PREREG)."""
import json, sys
ALPHA = (-7.5e-4, -1.14e-3)
F95 = {'SO': 0.0066, 'S4+SPHEREx': 0.0024, 'S4+CHIME+DESI+SPHEREx': 0.0018, 'LiteBIRD+S4+CHIME+SPHEREx': 0.0017}
ACT = 0.0062
out = {'sigma1_needed_3sigma_detection': [abs(a)/3 for a in ALPHA], 'surveys': {}}
for k, s in F95.items():
    s1 = s/2
    out['surveys'][k] = dict(sigma1=s1, detect_sigma=[abs(a)/s1 for a in ALPHA], exclude_if_ACT_central=[(ACT-a)/s1 for a in ALPHA])
best = min(F95.values())/2
out['detectable_by_2030'] = any(max(v['detect_sigma']) >= 3 for v in out['surveys'].values())
out['decisive_by_exclusion'] = min((ACT-a)/best for a in ALPHA) >= 5
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
