"""N12 (PREREG_N12_CLOSE)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
EA = F.two_body_split('DT')[1]; M_new, TBR, sTBR = 1.161, 1.021, 0.004
ref = X.goal_dials_fast(F.ITER, EA, F.PLANT_DEMO)
pin = dict(F.PLANT_DEMO, M=M_new); same = F.plant(ref['P_fus'], ref['P_aux'], pin)
Pn = ref['P_fus'] * F.two_body_split('DT')[0] / F.q_value('DT')
expect = F.PLANT_DEMO['eta_th'] * (ref['M'] - M_new) * Pn * (1 + F.PLANT_DEMO['f_pump'])
dP = ref['P_net'] - same['P_net']
new = X.goal_dials_fast(F.ITER, EA, pin)
hold, dbl = F.tbr_required(1, 10, 1e6), F.tbr_required(1, 10, 5)
G = dict(C1=abs(dP / expect - 1) <= .01, C2=(TBR - hold) > 2 * sTBR and (dbl - TBR) > 2 * sTBR)
res = dict(goals=G, ref_PROCESS_M=ref, same_point_new_M=same, dP_net=dP, expected_dP=expect, best_new_M=new, TBR=TBR, TBR_hold=hold, TBR_double5y=dbl,
           coverage_min_to_hold=hold / TBR)
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'n12_close.json'), 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
