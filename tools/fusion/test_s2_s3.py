"""FUSION-1 goalposts G3-G6 (S2, S3), run once as locked."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
Ea = F.two_body_split('DT')[1]; T, ntt = F.ignition_min(Ea); Ti = F.ideal_ignition_T(Ea)
op = F.operating_point(F.ITER, Ea); d = F.dials(F.ITER, Ea)
r = dict(G3=dict(T=T, nTtau=ntt, pass_=2.6e21 <= ntt <= 3.4e21 and 11 <= T <= 16), G4=dict(T=Ti, pass_=4.0 <= Ti <= 4.8),
         G5=dict(P_fus=op['P_fus'], Q=op['Q'], T_avg=op['T_avg'], roots=op['roots'], pass_=350 <= op['P_fus'] <= 650 and 6 <= op['Q'] <= 15),
         G6=dict(tau_E=op['tau_E'], P_loss=op['P_loss'], P_brems=op['P_brems'], P_alpha=op['P_alpha'], pass_=3.0 <= op['tau_E'] <= 4.4),
         dials=dict(n=d['n_avg'] if d else None, Q=d['Q'] if d else None, beta_N=d['beta_N'] if d else None, P_fus=d['P_fus'] if d else None, n_G=op['n_G'], betaN_iter=op['beta_N'], P_LH=op['P_LH']))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'fusion1_s2_s3.json'); json.dump(r, open(out, 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
