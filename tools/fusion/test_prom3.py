"""PROM-3 goalposts F1, E1-E5 (+ F2 sensitivity), run once as locked."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
t0 = time.time(); Ea = F.two_body_split('DT')[1]; share = F.two_body_split('DT')[0] / F.q_value('DT')
a = F.operating_point(F.ITER, Ea)
F1 = dict(martin_x_2overA=a['P_LH'], ipb99=F.p_LH_ipb99(F.ITER, a['n_line']), table=51.0); F1['ipb99_within_10pct'] = abs(F1['ipb99'] / 51 - 1) <= 0.10
# E1 ARC bookkeeping
Pf, Pa = 525.0, 38.6; M_arc = (708.0 - Pf * (1 - share) - Pa) / (Pf * share)
arc = F.plant(Pf, Pa, dict(M=M_arc, eta_th=0.40, eta_wp=1.0, f_pump=0.0, P_other=0.0)); Prc = arc['P_gross'] - 190.0
E1 = dict(M_implied=M_arc, P_gross=arc['P_gross'], P_recirc_implied=Prc, Q_e=arc['P_gross'] / Prc); E1['pass_'] = bool(abs(arc['P_gross'] - 283) <= 1 and abs(E1['Q_e'] - 3.0) <= 0.05)
E2 = dict(M=F.M_demoA()); E2['pass_'] = bool(1.2 <= E2['M'] <= 1.3)
pl = F.plant(a['P_fus'], F.ITER['P_aux'], F.PLANT_DEMO); pl25 = F.plant(a['P_fus'], F.ITER['P_aux'], dict(F.PLANT_DEMO, eta_wp=0.25))
E3 = dict(P_fus=a['P_fus'], **{k: pl[k] for k in ('P_th', 'P_gross', 'P_recirc', 'P_net', 'Q_e')}, P_net_eta_wp_0p25=pl25['P_net'], label='PREDICTION, best case (P_other = 0)')
g = F.goal_dials(F.ITER, Ea, F.PLANT_DEMO); g2 = F.goal_dials(F.ITER, Ea, dict(F.PLANT_DEMO, eta_wp=0.25))
E4 = dict(best=g, best_eta_wp_0p25=g2, F2_moves=bool(g and g2 and (abs(g['P_net'] - g2['P_net']) > 1e-6)))
from net import Bus, settle
root = F.build(); bus = Bus(); sw, ok = settle(root, bus)
E5 = dict(settled=ok, sweeps=sw, sv10=bus.v['sv_DT_10keV'], ign=bus.v['ignition_nTtau'], T_burn=bus.v['T_burn_kg_per_GWfpy'])
r = dict(F1=F1, E1=E1, E2=E2, E3=E3, E4=E4, E5=E5, seconds=round(time.time() - t0, 1))
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom3.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
