"""D1929: alpha_s(M_Z) at unification with the S-at-i spectrum (D1919: m3/2 7.6e5, wino 2.0 TeV, gluino 14.5 TeV)."""
import json, sys
sys.path.insert(0, 'tools/weave_cm'); from weave_tools import weave_rg2
base = weave_rg2({'m_wino': 690, 'm_gluino': 4930, 'm_scalar': 4.7e5})
heavy = weave_rg2({'m_wino': 2000, 'm_gluino': 14500, 'm_scalar': 4.7e5 * 7.6e5 / 2.58e5})
heavy_ms_fixed = weave_rg2({'m_wino': 2000, 'm_gluino': 14500, 'm_scalar': 4.7e5})
valid = abs(base['alpha_s_unif'] - 0.1147) < 5e-4
a = heavy['alpha_s_unif']; pull = (a - 0.1180) / 0.0009
out = dict(base=base, heavy=heavy, heavy_ms_fixed=heavy_ms_fixed, alpha_s_heavy=a, pull=pull, shift=a - base['alpha_s_unif'],
           verdict='VOID' if not valid else ('PASS' if abs(pull) <= 2 else 'FAIL'))
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1929_heavy_spectrum_as.json', 'w'), indent=1)
