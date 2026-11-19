"""D1650 / Janus genesis G12: whole-chain referee, mechanical part (PREREG_D1650_G12_REFEREE)."""
import json, math, subprocess
def first_add(path):
    o = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%at', '--', path], capture_output=True, text=True).stdout.split()
    return int(o[-1]) if o else None
R = 'field_tests/rules/'; S = 'field_tests/results/'
pairs = {'GENESIS_DE': ('PREREG_GENESIS_DE.md', 'GENESIS_DE/out.json'), 'GENESIS_DE2': ('PREREG_GENESIS_DE2.md', 'GENESIS_DE/rescore.json'),
         'GENESIS_DE3': ('PREREG_GENESIS_DE3.md', 'GENESIS_DE/tuning.json'), 'GENESIS_MATTER': ('PREREG_GENESIS_MATTER.md', 'GENESIS_MATTER/out.json'),
         'BBN2': ('PREREG_GENESIS_BBN2.md', 'GENESIS_MATTER/bbn2.json'), 'BBN3': ('PREREG_GENESIS_BBN3.md', 'GENESIS_MATTER/bbn3.json'),
         'LI7': ('PREREG_GENESIS_LI7.md', 'GENESIS_MATTER/li7.json'), 'RC2': ('PREREG_RC2_START.md', 'GENESIS_DE/rc2.json'),
         'D1637': ('PREREG_D1637_G1_REHEAT.md', 'D1637_G1_reheat.json'), 'D1638': ('PREREG_D1638_G2_THREAD_SHAPE.md', 'D1638_G2_thread_shape.json'),
         'D1641': ('PREREG_D1641_G1B_RHO_CURVATURE.md', 'D1641_G1b_rho_curvature.json'), 'D1644': ('PREREG_D1644_G9_THREAD_FUTURE.md', 'D1644_G9_thread_future.json'),
         'D1644dev': ('PREREG_D1644_G9_THREAD_FUTURE_DEVIATIONS.md', 'D1644_G9_thread_future.json'),
         'D1646': ('PREREG_D1646_G6_DARK_RADIATION.md', 'D1646_G6_dark_radiation.json'), 'D1647': ('PREREG_D1647_G10_CARD.md', 'D1647_G10_card_check.json')}
order = {}
for k, (p, r) in pairs.items():
    tp, tr = first_add(R + p), first_add(S + r)
    order[k] = dict(lock=tp, result=tr, ok=(tp is not None and tr is not None and tp <= tr))
for d in ('PREREG_GENESIS_DE_DEVIATIONS.md', 'PREREG_GENESIS_DE3_DEVIATIONS.md', 'PREREG_GENESIS_BBN2_DEVIATIONS.md'):
    order[d] = dict(added=first_add(R + d))
J = lambda f: json.load(open(S + f))
ar = {}
mo = J('GENESIS_MATTER/out.json'); ar['a_mDM'] = dict(json=mo['T1']['1'], recompute=0.1200 / 0.02237 * 0.93827, ok=abs(mo['T1']['1'] / (0.1200 / 0.02237 * 0.93827) - 1) < 0.01)
g1 = J('D1637_G1_reheat.json'); MP = 2.435e18
m = math.sqrt(g1['at_rho']['Vpp_over_Vinf_MP2'] * g1['Vinf_GeV4']) / MP
TR = lambda k: (90 / (math.pi ** 2 * 106.75)) ** 0.25 * math.sqrt(k * m ** 3 / MP)
ar['b_reheat'] = dict(m=m, TR_lo=TR(1 / (8 * math.pi)), TR_hi=TR(1), ok=abs(m / g1['m_GeV'] - 1) < 1e-9 and abs(TR(1) / g1['TR_band']['kappa_1'] - 1) < 1e-9)
g1b = J('D1641_G1b_rho_curvature.json'); ar['c_rho'] = dict(ok=all(abs(r['Vpp'] - (r['D'] - 2) / 32) < 1e-12 for r in g1b['rows']))
g6 = J('D1646_G6_dark_radiation.json'); xi = (5.5 / 2) ** (1 / 3) / (106.75 / 3.909) ** (1 / 3)
ar['d_dark'] = dict(xi=xi, dneff=2 / 1.75 * 2.75 ** (4 / 3) * xi ** 4, ok=abs(xi - g6['B_minimal_ADM']['xi']) < 1e-12)
g2 = J('D1638_G2_thread_shape.json'); pas = [r for r in g2['rows'] if r.get('pass_all')]
ar['e_thread'] = dict(n_pass=len(pas), ok=all(r['dmax'] <= 6.18 and r['w_min'] >= -1 - 1e-9 for r in pas) and all(r['w_min'] >= -1 - 1e-9 for r in g2['rows'] if r['viable']))
g9 = J('D1644_G9_thread_future.json'); ar['f_mH'] = dict(ok=abs(g9['m_over_HLambda'] - math.sqrt(3) / 2) < 1e-12)
Vinf = g1['Vinf_GeV4']; Hend = math.sqrt(Vinf / 3) / MP
phys = {}
phys['g_reheat'] = {k: dict(Gamma=kk * m ** 3 / MP ** 2, H_inf=Hend, Gamma_lt_H=kk * m ** 3 / MP ** 2 < Hend, TR_lt_m=TR(kk) < m) for k, kk in (('k_1/8pi', 1 / (8 * math.pi)), ('k_1', 1.0))}
phys['h_mirror'] = dict(value=2 / 1.75 * 2.75 ** (4 / 3) + 3, ok=abs(2 / 1.75 * 2.75 ** (4 / 3) + 3 - 7.40) < 0.01)
rc2 = J('GENESIS_DE/rc2.json'); phys['i_quantum'] = {k: dict(ratio=v['quantum_spread_MP'] / v['window_dpsi_MP'], ok=v['quantum_spread_MP'] < 1e-2 * v['window_dpsi_MP']) for k, v in rc2.items() if isinstance(v, dict) and 'window_dpsi_MP' in v}
allok = all(v['ok'] for v in order.values() if 'ok' in v) and all(v['ok'] for v in ar.values()) and all(x['Gamma_lt_H'] and x['TR_lt_m'] for x in phys['g_reheat'].values()) and phys['h_mirror']['ok'] and all(v['ok'] for v in phys['i_quantum'].values())
out = dict(D='D1650', order=order, arithmetic=ar, physics=phys, mechanical='PASS' if allok else 'FAIL')
json.dump(out, open(S + 'D1650_G12_referee.json', 'w'), indent=1, default=float)
print(json.dumps({'mechanical': out['mechanical'], 'order_fail': [k for k, v in order.items() if v.get('ok') is False], 'arith_fail': [k for k, v in ar.items() if not v['ok']],
                  'reheat': phys['g_reheat'], 'mirror': phys['h_mirror'], 'quantum': phys['i_quantum'], 'dev_files': {k: v for k, v in order.items() if 'added' in v}}, indent=1, default=float))
