import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import beam_target as B
fr = (0.53, 0.33, 0.14)
p71 = {Te: B.P_bt(26.5, 108.0, fr, Te, 6e19, 0.85, 0.85) for Te in (5.0, 6.5, 8.0)}
p522 = B.P_bt(30.0, 108.0, fr, 6.5, 6e19, 0.80, 0.85)
p50 = B.P_bt(26.5, 108.0, fr, 6.5, 6e19, 0.50, 0.85)
comp = B.composition(0.85, 0.85); Es = np.linspace(40, 300, 261); ype = [B.yield_per_ion(E, 6.5, 6e19, comp) / E for E in Es]
Eopt = float(Es[int(np.argmax(ype))]); tau, Ec, lnL = B.slowing(6.5, 6e19, comp)
G = dict(J1=abs(p71[6.5] / 8.7 - 1) <= .40, J2=abs(p522 / 11.6 - 1) <= .40, J3=(1 - p50 / p71[6.5]) > .30, J4=90 <= Eopt <= 140)
res = dict(goals=G, P_bt_99971=p71, P_bt_104522=p522, P_bt_fT05=p50, E_opt_keV=Eopt, tau_s=tau, E_c_keV=Ec, lnL=lnL)
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'jet1.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
