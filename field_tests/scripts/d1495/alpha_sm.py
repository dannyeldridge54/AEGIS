"""D1495: alpha -> SMSCAN-equivalent s*m by matching r at C = 0 (PREREG_D1495)."""
import json, numpy as np
d85 = json.load(open('field_tests/results/D1485_dilmix_sr.json'))['part3']
B0 = json.load(open('field_tests/results/DILATON32/B0.json'))
dil = {0.0: (B0['ns'], B0['r'])}
for p in d85:
    if p['C'] == 0 and 'error' not in p and p['alpha'] > 0: dil[round(p['alpha'], 4)] = (p['ns'], p['r'])
sm = {}
for p in json.load(open('field_tests/results/D1483_smscan_sr.json'))['part1'].values(): sm[round(p['sm'], 4)] = (p['ns'], p['r'])
for p in json.load(open('field_tests/results/D1483_smscan_sr.json'))['part2'].values(): sm[round(p['sm'], 4)] = (p['ns'], p['r'])
for p in json.load(open('field_tests/results/D1490_smtilt.json'))['map']:
    if p.get('C') == 0 and 'error' not in p: sm[round(p['sm'], 4)] = (p['ns'], p['r'])
S = sorted(sm); lr = np.log([sm[k][1] for k in S]); ls = np.log(S)
order = np.argsort(lr); out = {"D": "D1495", "smscan_points": {str(k): sm[k] for k in S}, "rows": []}
for al in sorted(dil):
    ns, r = dil[al]
    smeff = float(np.exp(np.interp(np.log(r), lr[order], ls[order]))) if lr.min() <= np.log(r) <= lr.max() else None
    m32 = smeff / 1.5 if smeff else None
    out['rows'].append(dict(alpha=al, ns_C0=ns, r_C0=r, sm_eff=smeff, m_at_s1p5=m32, q_over_p=(1 + 1 / m32) if m32 else None))
    print(out['rows'][-1])
json.dump(out, open('field_tests/results/D1495_alpha_sm.json', 'w'), indent=1)
