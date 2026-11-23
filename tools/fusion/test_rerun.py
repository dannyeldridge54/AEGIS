"""FUSION-1 single rerun after all deviations (DEV-1..14). Locked goalposts re-evaluated; post-hoc goalposts labelled."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
from net import Bus, settle
root = F.build(); bus = Bus(); sw, ok = settle(root, bus); b = bus.v
Ea = F.two_body_split('DT')[1]; En = F.two_body_split('DT')[0]; Q = F.q_value('DT')
T, ntt = F.ignition_min(Ea); Ti = F.ideal_ignition_T(Ea); op = F.operating_point(F.ITER, Ea); d = F.dials(F.ITER, Ea)
w = lambda x, c, tol: abs(x / c - 1) <= tol
r = dict(settled=dict(sweeps=sw, converged=ok),
 G1=dict(v10=F.sigmav('DT', 10), v20=F.sigmav('DT', 20), pass_=bool(w(F.sigmav('DT', 10), 1.136e-16, .005) and w(F.sigmav('DT', 20), 4.330e-16, .005))),
 G2_DEV1=dict(share=En / Q, Q=Q, pass_=bool(abs(En / Q - 0.7976) <= 0.001 and abs(Q - 17.589) <= 0.002), label='post-hoc goalpost (DEV-1)'),
 G3=dict(T=T, nTtau=ntt, pass_=bool(2.6e21 <= ntt <= 3.4e21 and 11 <= T <= 16)), G4=dict(T=Ti, pass_=bool(4.0 <= Ti <= 4.8)),
 G5_G6_DEV7={k: op[k] for k in ('P_fus', 'Q', 'tau_E', 'W_MJ', 'beta_N', 'P_rad', 'P_brems', 'P_synch', 'P_loss', 'Te_avg', 'Ti_avg', 'Zeff', 'f_DT', 'f_G', 'P_LH')},
 G7=dict(y=F.specific_yield_J_per_g(), pass_=bool(w(F.specific_yield_J_per_g(), 3.37e11, .005) and F.burn_fraction(3) == 1 / 3)),
 G8_DEV11={k: v for k, v in b.items() if k.startswith('NIF_target_gain')}, G9=dict(pass_=b['IFE_gain_needed_eta0.1'] == 100),
 G10b_DEV10=dict(T_kg=b['T_burn_kg_per_GWfpy'], pass_=bool(w(b['T_burn_kg_per_GWfpy'], 56.08, .001)), label='post-hoc goalpost'),
 G11=dict(load_730=b['iter_wall_load_MW_m2'], load_FW670=b['iter_wall_load_FW_only_MW_m2'], design_500MW_730=b['design_wall_load_500MW'], ITER_avg=0.55),
 G12_DEV14=dict(dpa_per_fpy=b['dpa_per_fpy_at_model_load'], He_per_dpa=b['He_appm_per_dpa_steel']),
 G13_DEV2=dict(E0_15MK=F.gamow(1, 1, F.nuc('H1', 1) / 2, T_K=15e6)['E0_keV'], E0_157MK=F.gamow(1, 1, F.nuc('H1', 1) / 2, T_K=15.7e6)['E0_keV']),
 TBR_example_DEV12=b['TBR_example_1GW_10kg_5y'], dials_DEV8=dict(Q=d['Q'], n=d['n_avg'], f_G=d['f_G'], binding=d['binding']) if d else None)
o = r['G5_G6_DEV7']; r['G5_G6_DEV7']['pass_'] = bool(w(o['P_fus'], 500, .2) and w(o['tau_E'], 3.4, .15) and w(o['W_MJ'], 353, .15) and w(o['beta_N'], 2.0, .15) and w(o['P_rad'], 61, .25) and w(o['P_loss'], 104, .2))
r['G5_G6_DEV7']['label'] = 'post-hoc goalposts set after run 1 (DEV-7), ITER 500 MW column'
g = r['G13_DEV2']; g['pass_'] = bool(w(g['E0_15MK'], 5.9, .03) and w(g['E0_157MK'], 6.07, .03)); g['label'] = 'post-hoc (DEV-2)'
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'fusion1_rerun.json'); json.dump(r, open(out, 'w'), indent=1, default=str)
print(json.dumps({k: (v.get('pass_') if isinstance(v, dict) else v) for k, v in r.items()}, default=str)); print(json.dumps(r['G5_G6_DEV7'], default=str)); print(r['dials_DEV8'], r['G11'], r['G12_DEV14'], r['G13_DEV2'], r['TBR_example_DEV12'])
