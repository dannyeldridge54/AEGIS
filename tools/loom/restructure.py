"""D2150: score the g_s restructure options (PREREG_D2150)."""
import json, math
def m_ns(ns): return 2 - abs(ns - 0.974)/0.003
def m_r(r): return math.log(0.036/r)
def m_ctl(g): return math.log(0.5/g)
UNPROT_A = ['alpha_GUT from f_vis = T + 9S (perturbative gauge kinetic function)', 'magnetised-D7 family flux |M| = 9 (perturbative D-brane flux)',
            'D-instanton / E3 mu-term weight', 'Yukawa normalisations (worldsheet instantons)', 'KKLT W0-volume-m3/2 chain (perturbative Kahler potential)']
opts = {
 'A': dict(gs=1.155, ns=0.9706, r=5.4e-4, moved=[], note='null'),
 'F': dict(gs=None, ns=0.9706, r=5.4e-4, moved=[], unprotected=UNPROT_A, note='F-theory constant-coupling point at rho'),
 'B_D1398': dict(gs=0.2, ns=0.9606, r=1.56e-3, moved=['n_s', 'r', 'A=7.30 at both ends', 'inflaton identity'], note='U3 inflaton, full-Y variant'),
 'D_r0.005': dict(gs=0.2, ns=1 - math.sqrt(0.005/6), r=0.005, moved=['n_s', 'r', 'A=7.30 link', 'm3/2 and wino chain', 'tau_q', 'alpha_GUT', 'needs blow-up/K3 fibre'], note='fibre inflation, low-r end'),
 'D_r0.01': dict(gs=0.2, ns=1 - math.sqrt(0.01/6), r=0.01, moved=['n_s', 'r', 'A=7.30 link', 'm3/2 and wino chain', 'tau_q', 'alpha_GUT', 'needs blow-up/K3 fibre'], note='fibre inflation, high-r end'),
}
rows = []
for k, o in opts.items():
    m = dict(n_s=m_ns(o['ns']), r=m_r(o['r']))
    if o['gs'] is not None: m['control_gs'] = m_ctl(o['gs'])
    rows.append(dict(option=k, margins={a: round(b, 3) for a, b in m.items()}, min_margin=round(min(m.values()), 3), n_moved=len(o['moved']),
                     n_unprotected=len(o.get('unprotected', [])) if k == 'F' else (len(UNPROT_A) if k == 'A' else 0), note=o['note'], ns=round(o['ns'], 4), r=o['r']))
rows.sort(key=lambda x: (-x['min_margin'], x['n_moved']))
out = dict(rows=rows, unprotected_list_A_F=UNPROT_A); print(json.dumps(rows, indent=1))
json.dump(out, open('field_tests/results/d2150_restructure.json', 'w'), indent=1)
