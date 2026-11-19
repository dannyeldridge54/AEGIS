"""D1666 / Janus genesis G12d (PREREG_D1666_G12D_REFEREE)."""
import json, math, re, subprocess
fa = lambda p: (lambda o: int(o[-1]) if o else None)(subprocess.run(['git', 'log', '--diff-filter=A', '--format=%at', '--', p], capture_output=True, text=True).stdout.split())
R, S = 'field_tests/rules/', 'field_tests/results/'
pairs = {'D1663': ('PREREG_D1663_G14_LIGHT_ELEMENTS.md', 'D1663_G14_light_elements.json'), 'D1664': ('PREREG_D1664_G6E_DARKCAST.md', 'D1664_G6e_darkcast.json'), 'D1665': ('PREREG_D1665_G15_KAPPA.md', 'D1665_G15_kappa.json')}
order = {k: (fa(R + a) or 0) <= (fa(S + b) or -1) for k, (a, b) in pairs.items()}
J = lambda f: json.load(open(S + f)); ar = {}
a = J('D1663_G14_light_elements.json'); t = a['toolkit']
ar['D1663'] = abs((t['Yp'] - 0.2458) / 0.0013 - a['pull_toolkit_obs']['Yp']) < 1e-9 and abs((t['DH_e5'] - 2.527) / 0.030 - a['pull_toolkit_obs']['DH']) < 1e-9
b = J('D1664_G6e_darkcast.json'); merge = [r for r in b['rows'] if r['m_GeV'] > 0.1 and len(r['intervals']) == 1 and r['intervals'][0][1] > 1e-4][0]['m_GeV']
ar['D1664'] = abs(merge - 0.808) < 0.005 and all(r['widest_decades'] >= 1 for r in b['rows'] if 0.3 <= r['m_GeV'] <= 5.03)
c = J('D1665_G15_kappa.json'); g1 = J('D1637_G1_reheat.json'); k = 12 * 4 / (128 * math.pi)
TR = (90 / (math.pi ** 2 * 106.75)) ** 0.25 * math.sqrt(k * g1['m_GeV'] ** 3 / 2.435e18)
ar['D1665'] = abs(c['kappa_gg'] - k) < 1e-12 and abs(c['T_R_GeV'] / TR - 1) < 1e-12
card = subprocess.run(['python3', 'field_tests/scripts/janus_g/g10_card_check.py'], capture_output=True, text=True).stdout.strip()
log = open('theory/derivations/DERIVATION_LOG.md').read()
src = {}
for d in ('D1663', 'D1664', 'D1665'):
    m = re.search(rf'(?ms)^## {d}\b.*?(?=^## |\Z)', log); s = m.group(0) if m else ''
    src[d] = bool(re.search(r'\d{4}\.\d{4,5}|hep-ph/\d{7}', s))
ok = all(order.values()) and all(ar.values()) and card.endswith('CONSISTENT []') and all(src.values())
out = dict(D='D1666', order=order, arith=ar, card=card, sourced=src, verdict='PASS' if ok else 'FAIL')
json.dump(out, open(S + 'D1666_G12d_referee.json', 'w'), indent=1); print(json.dumps(out, indent=1))
