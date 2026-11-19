"""D1663 / Janus genesis G14 (PREREG_D1663_G14_LIGHT_ELEMENTS)."""
import json
t = json.load(open('field_tests/results/GENESIS_MATTER/rd1.json'))['v5']
Yp, DH, Li = t['Yp'], t['D_H'] * 1e5, t['Li'] * 1e10
obs = dict(Yp=(0.2458, 0.0013), DH=(2.527, 0.030), Li=(1.58, 0.31)); pri = dict(Yp=0.24709, DH=2.459)
out = dict(D='D1663', toolkit=dict(Yp=Yp, DH_e5=DH, Li_e10=Li),
           pull_toolkit_obs=dict(Yp=(Yp - obs['Yp'][0]) / obs['Yp'][1], DH=(DH - obs['DH'][0]) / obs['DH'][1], Li=(Li - obs['Li'][0]) / obs['Li'][1]),
           toolkit_minus_PRIMAT=dict(Yp=Yp - pri['Yp'], DH_rel=DH / pri['DH'] - 1),
           pull_PRIMAT_obs=dict(Yp=(pri['Yp'] - obs['Yp'][0]) / obs['Yp'][1], DH=(pri['DH'] - obs['DH'][0]) / obs['DH'][1]),
           D1633_obs_0p245_pm_0p003=dict(vs_LBT=abs(0.245 - 0.2458) <= 0.003, vs_PRIMAT_obs_row=abs(0.245 - 0.2449) <= 0.0040),
           D1651_fullcode_0p247=abs(0.247 - pri['Yp']) <= 0.0005)
out['textbook_grade'] = abs(out['toolkit_minus_PRIMAT']['Yp']) <= 0.003 and abs(out['toolkit_minus_PRIMAT']['DH_rel']) <= 0.10
json.dump(out, open('field_tests/results/D1663_G14_light_elements.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
