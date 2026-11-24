"""D2233 (PREREG_D2233_GH_AT_WEAVE)."""
import json, math
import sys; sys.path.insert(0, 'tools/strings'); from gh_thresholds_v2 import *
gs = 2 / math.sqrt(3); ainv = 28.0
out = {}
for lab, w, Va in (('omega1', 1, 0.16), ('omega2', 2, 0.11)):
    MPs = ainv / Va; vW = 0.5 * (gs * MPs) ** (2 / 3)
    Va_req = gs * ainv / 2 ** 1.5                     # v = 1  <=>  g_s M_P/M_s = 2^(3/2)  <=>  Vol_a = g_s * 28 / 2^(3/2)
    cases = [c for c in CASE if CASE[c][0] == w]
    d = {c: {f'v{vv:.3g}': float((D3(vv, w) - D2(vv, c)) / (4 * mp.pi)) for vv in (1.0, vW)} for c in cases}
    out[lab] = dict(Vol_a=Va, MP_over_Ms=MPs, v_W=vW, Vol_a_required_for_v1=Va_req, delta32=d)
out['reading'] = 'INCONSISTENT: tau = i needs Vol_a ~ %.1f vs published 0.11-0.16' % out['omega1']['Vol_a_required_for_v1'] if out['omega1']['v_W'] > 3 else 'v ~ 1 reachable'
json.dump(out, open('field_tests/results/d2233_gh_weave.json', 'w'), indent=1); print(json.dumps(out, indent=1))
