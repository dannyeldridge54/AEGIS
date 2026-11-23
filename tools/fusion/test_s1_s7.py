"""FUSION-1 goalposts G1, G2 (S1) and G13 (S7), run once as locked."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
r = {}
r['G1'] = dict(sv10=F.sigmav('DT', 10), sv20=F.sigmav('DT', 20), rel10=F.sigmav('DT', 10) / 1.136e-16 - 1, rel20=F.sigmav('DT', 20) / 4.330e-16 - 1)
r['G1']['pass'] = abs(r['G1']['rel10']) <= 0.005 and abs(r['G1']['rel20']) <= 0.005
En, Ea = F.two_body_split('DT'); Q = F.q_value('DT')
r['G2'] = dict(Q=Q, E_n=En, E_alpha=Ea, n_share=En / Q, pass_Q=abs(Q - 17.589) <= 0.002, pass_share=abs(En / Q - 0.7997) <= 0.001)
r['G2']['pass'] = r['G2']['pass_Q'] and r['G2']['pass_share']
g = F.gamow(1, 1, F.nuc('H1', 1) / 2, T_K=15.7e6); r['G13'] = dict(E0=g['E0_keV'], rel=g['E0_keV'] / 5.9 - 1, pass_=abs(g['E0_keV'] / 5.9 - 1) <= 0.03,
                                                                     dt_10keV_E0=F.gamow(1, 1, F.nuc('D', 1) * F.nuc('T', 1) / (F.nuc('D', 1) + F.nuc('T', 1)), kT_keV=10)['E0_keV'])
r['extra'] = dict(Q_DDn=F.q_value('DDn'), Q_DDp=F.q_value('DDp'), Q_DHe3=F.q_value('DHe3'), sv_DT_peak_keV=max((t / 10 for t in range(20, 1000)), key=lambda t: F.sigmav('DT', t)))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'fusion1_s1_s7.json'); json.dump(r, open(out, 'w'), indent=1); print(json.dumps(r, indent=1))
