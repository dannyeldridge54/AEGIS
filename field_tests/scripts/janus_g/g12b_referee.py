"""D1660 / Janus genesis G12b (PREREG_D1660_G12B_REFEREE)."""
import json, math, re, subprocess
def first_add(p):
    o = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%at', '--', p], capture_output=True, text=True).stdout.split()
    return int(o[-1]) if o else None
R, S = 'field_tests/rules/', 'field_tests/results/'
pairs = {'D1653': ('PREREG_D1653_G9B_TAU_PLANE.md', 'D1653_G9b_tau_plane.json'), 'D1654': ('PREREG_D1654_G6B_CHANNELS_NEFF.md', 'D1654_G6b_channels.json'),
         'D1655': ('PREREG_D1655_G9C_BASIN.md', 'D1655_G9c_basin.json'), 'D1657': ('PREREG_D1657_G6C_MASSIVE_DP.md', 'D1657_G6c_massive_dp.json'),
         'D1658': ('PREREG_D1658_G9D_FUTURE_D1636.md', 'D1658_G9d_future_d1636.json'), 'D1658dev': ('PREREG_D1658_G9D_FUTURE_D1636_DEVIATIONS.md', 'D1658_G9d_future_d1636.json'),
         'D1659': ('PREREG_D1659_G6D_DP_STRIP.md', 'D1659_G6d_dp_strip.json'), 'D1644dev': ('PREREG_D1644_G9_THREAD_FUTURE_DEVIATIONS.md', 'D1644_G9_thread_future.json')}
order = {k: dict(lock=first_add(R + a), result=first_add(S + b)) for k, (a, b) in pairs.items()}
for v in order.values(): v['ok'] = v['lock'] is not None and v['result'] is not None and v['lock'] <= v['result']
J = lambda f: json.load(open(S + f)); ar = {}
d54 = J('D1654_G6b_channels.json'); ok = True
for k, v in d54['scenarios'].items():
    ok &= abs((3.044 + v['dneff'] - 2.86) / 0.13 - v['pull_ACT']) < 1e-9 and abs((3.044 + v['dneff'] - 2.990) / 0.070 - v['pull_2603']) < 1e-9
ar['D1654_pulls'] = ok
d57 = J('D1657_G6c_massive_dp.json'); al, me, hb = 1 / 137.036, 0.51099895, 6.582119569e-22
ar['D1657_eps'] = all(abs(math.sqrt(hb / (al * r['m_MeV'] / 3 * (1 + 2 * (me / r['m_MeV']) ** 2) * math.sqrt(1 - 4 * (me / r['m_MeV']) ** 2))) / r['eps_min_tau_1s'] - 1) < 1e-9 for r in d57['rows'])
d59 = J('D1659_G6d_dp_strip.json'); ar['D1659_intervals'] = all((x['OPEN'] == any(i['decades'] >= 1 for i in x['open'])) and all(i['eps_lo'] >= x['eps_floor'] * (1 - 1e-12) and i['eps_hi'] <= 1e-3 * (1 + 1e-12) for i in x['open']) for x in d59['rows'])
d58 = J('D1658_G9d_future_d1636.json'); ar['D1658_match'] = all(abs(r['matched']['0.0']['w0'] - r['w0_D1636']) <= 0.002 for r in d58['results'].values())
d55 = J('D1655_G9c_basin.json'); ar['D1655_classes'] = all(r['end_class'] == ('i-class' if r['dist_i'] < 0.02 else ('rho-class' if r['dist_rho'] < 0.02 else 'other')) for r in d55['runs'].values())
ar['D1653_R0'] = J('D1653_G9b_tau_plane.json')['R0_code_check'] == 'PASS'
card = subprocess.run(['python3', 'field_tests/scripts/janus_g/g10_card_check.py'], capture_output=True, text=True).stdout.strip()
# source audit
txt = open('theory/pending_docs/D72_D75_weak_spots.md').read()
secs = re.split(r'(?m)^(?=## D)', txt)
data_pat = re.compile(r'N_eff|observed|\bbound\b|Planck|DESI|Y_p\s*=?\s*[\d.]+\s*±|D/H[^\n]{0,30}±|ε\s*[≲≳<>]', re.I)
ref_pat = re.compile(r'\d{4}\.\d{4,5}|arXiv|Phys\.? ?Rev|JCAP|JHEP|Science 20\d\d|PDG|Planck 20\d\d|Smith–Kawano–Malaney|PArthENoPE|Table [IVX]+|ACT DR6|DESI DR2|Roederer', re.I)
flags = []
for s in secs:
    m = re.match(r'## (D16(2[6-9]|[3-5]\d)a?)\b', s)
    if not m: continue
    if data_pat.search(s) and not ref_pat.search(s):
        flags.append(dict(note=m.group(1), head=s.splitlines()[0][:140], hits=sorted(set(x.group(0) for x in data_pat.finditer(s)))[:6]))
out = dict(D='D1660', order=order, order_ok=all(v['ok'] for v in order.values()), arith=ar, arith_ok=all(ar.values()), card=card, source_flags=flags)
json.dump(out, open(S + 'D1660_G12b_referee.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'order'}, indent=1)); print('order_fail', [k for k, v in order.items() if not v['ok']])
