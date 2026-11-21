"""PREREG_C3_SIDM: Born transfer cross-section, repulsive Yukawa, 12.8 GeV asymmetric DM."""
import math, json
M, GEV2CM2, GEV2G, C = 12.8, 3.894e-28, 1.783e-24, 299792.458
def sm(aD, mA, vkms):
    v = vkms / C; R = M * v / mA
    s = 8 * math.pi * aD ** 2 / (M ** 2 * v ** 4) * (math.log(1 + R ** 2) - R ** 2 / (1 + R ** 2))
    return s * GEV2CM2 / (M * GEV2G), aD * M / mA
out = {}
for aD in (4.7e-4, 4.7e-3):
    for mA in (0.3, 1.0, 3.0, 12.8):
        out[f'aD={aD} mA={mA}'] = {f'{v}kms': dict(zip(('sigma_over_m_cm2_g', 'born_param'), sm(aD, mA, v))) for v in (30, 200, 1000)}
mx = max(out[k]['1000kms']['sigma_over_m_cm2_g'] for k in out if k.startswith('aD=0.00047 '))
out['verdict'] = dict(max_cluster_at_aDmin=mx, PASS=mx < 0.1, any_core_30kms=any(v['30kms']['sigma_over_m_cm2_g'] >= 0.5 for v in out.values() if isinstance(v, dict) and '30kms' in v),
                      born_valid_all=all(v[k]['born_param'] < 1 for v in out.values() if isinstance(v, dict) and '30kms' in v for k in v))
print(json.dumps(out, indent=1))
