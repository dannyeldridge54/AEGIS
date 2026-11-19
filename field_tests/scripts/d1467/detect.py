import json
d = json.load(open('field_tests/results/D1466_beta_s.json'))
B = {'rho': d['rho']['beta'], 'tau_i': d['tau_i']['beta']}; S = {'Planck2018': 0.013, 'CMB-S4_hypothetical': 0.0045}
out = dict(D='D1467', beta=B, sigma=S, significance={v: {s: abs(b)/sg for s, sg in S.items()} for v, b in B.items()},
           sigma_needed_3sigma={v: abs(b)/3 for v, b in B.items()})
out['verdict'] = 'beta_s undetectable on listed surveys' if all(x < 1 for v in out['significance'].values() for x in v.values()) else 'detectable somewhere'
json.dump(out, open('field_tests/results/D1467_beta_detect.json', 'w'), indent=1); print(json.dumps(out, indent=1))
