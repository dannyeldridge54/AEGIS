"""PROM-2 goalposts Q1-Q3, run once as locked."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
Ea = F.two_body_split('DT')[1]; prev = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom1.json')))
a = F.operating_point(F.ITER, Ea); b = F.operating_point(F.ITER_400, Ea)
diag5 = F.operating_point(dict(F.ITER, rad_C3=1.0, rho_core=1.0), Ea); diag4 = F.operating_point(dict(F.ITER_400, rad_C3=1.0, rho_core=1.0), Ea)
Q1 = dict(P_LH_500=a['P_LH'], P_LH_500_prom1=prev['P1']['P_LH'], table=51.0, ratio_400=b['P_loss'] / b['P_LH'], polevoi_ratio=1.8, floor=1.3)
Q1['pass_'] = abs(a['P_LH'] - 51) < abs(prev['P1']['P_LH'] - 51)
Q2 = dict(W=b['W_MJ'], f_He=b['f_He'], tau=b['tau_E'], pass_=bool(abs(b['W_MJ'] / 323.5 - 1) <= 0.10 and abs(b['f_He'] - 0.0315) <= 0.01 and abs(b['tau_E'] / 3.71 - 1) <= 0.15))
Q2['not_worse_than_prom1'] = abs(b['tau_E'] / 3.71 - 1) <= abs(prev['P2_heldout']['tau_E'] / 3.71 - 1) + 1e-12 and abs(b['W_MJ'] / 323.5 - 1) <= abs(prev['P2_heldout']['W_MJ'] / 323.5 - 1) + 1e-12
diag = dict(ITER_convention_500=dict(tau=diag5['tau_E'], P_fus=diag5['P_fus'], Q=diag5['Q']) if diag5 else None, ITER_convention_400=dict(tau=diag4['tau_E'], P_fus=diag4['P_fus'], Q=diag4['Q']) if diag4 else None)
r = dict(Q1=Q1, Q2_heldout=Q2, diagnostic_C2=diag, accept=bool(Q1['pass_'] and Q2['not_worse_than_prom1']))
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom2.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
