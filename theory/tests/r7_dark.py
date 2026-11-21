"""PREREG_R7_DARK_COUPLING"""
import sys, math, json
sys.path.insert(0, 'tools/weave_cm'); import weave_tools as W
ainv = 21.1 + (4 / 3) / (2 * math.pi) * math.log(7e15 / 12.8); aD = 1 / ainv
rows = {}
for mA in (0.3, 1.0, 3.0, 12.8):
    for v in (30, 200, 1000):
        r = W.weave_sidm({'alpha_D': aD, 'm_A_GeV': mA, 'v_kms': v})
        rows[f'mA={mA} v={v}'] = r['sigma_over_m_cm2_g'] if r['born_valid'] else 'NOT COMPUTED (non-Born, param %.2f)' % r['born_param']
valid = [v for k, v in rows.items() if 'v=1000' in k and isinstance(v, float)]
print(json.dumps(dict(alpha_D_inv_12GeV=ainv, alpha_D=aD, annihilation_ok=aD >= 4.7e-4, rows=rows, PASS=all(x < 0.1 for x in valid)), indent=1))
