"""PROM-3 single rerun after DEV-1..7 (fast path)."""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F, fusion_fast as X
t0 = time.time(); Ea = F.two_body_split('DT')[1]
g = X.goal_dials_fast(F.ITER, Ea, F.PLANT_DEMO); nG = F.ITER['Ip'] / (math.pi * F.ITER['a'] ** 2) * 1e20
edge = X.binding_limit(F.ITER, Ea, g['P_aux'], g['n_avg'], g['n_avg'] + 0.02 * nG)
op = edge['op']; rows = {}
for po in (0.0, 50.0, 100.0):
    for fp, lab in ((14.0 / 2058.0, 'DEMO-A pumping'), (0.085, 'helium simple-model pumping')):
        pl = F.plant(op['P_fus'], g['P_aux'], dict(F.PLANT_DEMO, P_other=po, f_pump=fp)); rows[f'P_other={po:.0f}, {lab}'] = dict(P_net=pl['P_net'], Q_e=pl['Q_e'])
pl25 = F.plant(op['P_fus'], g['P_aux'], dict(F.PLANT_DEMO, eta_wp=0.25))
s3 = F.operating_point(F.ITER, Ea); over = F.plant(s3['P_fus'], 50.0, dict(F.PLANT_DEMO, P_other=0.0, f_pump=0.085, pump_in_Pth=False))
r = dict(E3_feasible=dict(n_edge=edge['n_edge'], f_G=op['f_G'], binding_limit=edge['limit'], P_aux=g['P_aux'], P_fus=op['P_fus'], Q=op['Q'], beta_N=op['beta_N'],
                          lh_ratio=op['P_loss'] / op['P_LH'], rows=rows, headline_P_other_100=rows['P_other=100, DEMO-A pumping'], eta_wp_0p25_P_other_100=dict(P_net=pl25['P_net'], Q_e=pl25['Q_e'])),
         E3_old_over_greenwald=dict(f_G=s3['f_G'], P_net=over['P_net'], label='over Greenwald (f_G 0.987), P_other 0, f_pump 0.085: the run-1 number'),
         F1=dict(ipb99_model_point=F.p_LH_ipb99(F.ITER, s3['n_line']), ipb99_at_nline_1e20=F.p_LH_ipb99(F.ITER, 1.0e20), table=51.0, snipes_ITER_FEAT=49.0),
         seconds=round(time.time() - t0, 1))
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom3_rerun.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
