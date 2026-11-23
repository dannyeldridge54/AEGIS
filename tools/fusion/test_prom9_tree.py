"""PROM-9 TREE (PREREG_PROM9_TREE): every layer of the fusion tree, one run, locked goalposts."""
import io, json, math, os, sys, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X, fusion_cm as FC
with contextlib.redirect_stdout(io.StringIO()): import test_prom6 as T6, test_prom7 as T7, test_prom8 as T8
EA = F.two_body_split('DT')[1]; L = {}
rel = lambda a, b: a / b - 1
# L1 S1
s10, s20 = F.sigmav('DT', 10), F.sigmav('DT', 20); Q = F.q_value('DT'); En = F.two_body_split('DT')[0]
L['L1_S1_reactions'] = dict(sv10=s10, sv20=s20, Q=Q, n_share=En / Q, pass_=abs(rel(s10, 1.136e-16)) <= .005 and abs(rel(s20, 4.330e-16)) <= .005 and abs(Q - 17.589) <= .002 and abs(En / Q - .7997) <= .001)
# L2 S2
T, ntt = F.ignition_min(EA); Ti = F.ideal_ignition_T(EA)
L['L2_S2_ignition'] = dict(T_min=float(T), nTtau=float(ntt), T_ideal=Ti, pass_=bool(2.6e21 <= ntt <= 3.4e21 and 11 <= T <= 16 and 4.0 <= Ti <= 4.8))
# L3 S3 ITER
a = X.operating_point_fast(F.ITER, EA); b = X.operating_point_fast(F.ITER_400, EA)
L['L3_S3_ITER'] = dict(P500=a['P_fus'], Q500=a['Q'], tau500=a['tau_E'], P400=b['P_fus'],
                      pass_=bool(350 <= a['P_fus'] <= 650 and 6 <= a['Q'] <= 15 and 3.0 <= a['tau_E'] <= 4.4 and abs(rel(b['P_fus'], 400)) <= .10))
# L4 S3 SPARC (popcon convention)
S = dict(T8.S); S.update(rad_C3=0.6, rho_core=0.75, synch=True)   # T8.S is the locked PROM-8 SPARC (pre-rerun settings)
Sp = dict(S, convention='popcon', synch=False)
op = lambda m: X.operating_point_fast(m, EA)
sp, si = op(Sp), op(S)
L['L4_S3_SPARC'] = dict(P_fus=sp and sp['P_fus'], T=sp and sp['Te_avg'], Q=sp and sp['Q'], tau_E=sp and sp['tau_E'], W=sp and sp['W_MJ'], P_fus_ITERconv=si and si['P_fus'],
                       pass_=bool(sp and abs(rel(sp['P_fus'], 140)) <= .25 and abs(rel(sp['Te_avg'], 7.3)) <= .20), can_fail=bool(sp and si and abs(rel(si['P_fus'], sp['P_fus'])) > .15))
# L5 S3 ARC (prescribed)
ARp = T7.ARp; pA = float(X.plasma_fast(ARp, ARp['n_avg'], 13.9, EA)['P_fus']); H = T7.P3['H98_implied']
L['L5_S3_ARC'] = dict(P_fus=pA, H98_implied=H, pass_=abs(rel(pA, 525)) <= .20 and abs(rel(H, 1.8)) <= .15)
# L6 S4
y = F.specific_yield_J_per_g(); p = FC.run('fusion_nif_pressure', json.loads(FC.EXAMPLES['fusion_nif_pressure']))['p_Gbar']
L['L6_S4_inertial'] = dict(specific_yield=y, Phi3=F.burn_fraction(3.0), p_Gbar=p, pass_=abs(rel(y, 3.37e11)) <= .005 and F.burn_fraction(3.0) == 1 / 3 and abs(p - 569) <= 61)
# L7 S5
tb = F.burn_kg_per_GWfpy('T'); tbr = F.tbr_required(1, 10, 5)
L['L7_S5_fuel'] = dict(T_kg=tb, TBR=tbr, pass_=abs(rel(tb, 56.08)) <= .01 and 1.04 <= tbr <= 1.06)
# L8 S7
g = F.gamow(1, 1, F.nuc('H1', 1) / 2, T_K=15.7e6)['E0_keV']
L['L8_S7_stars'] = dict(E0=g, pass_=abs(rel(g, 5.9)) <= .03)
# L9 data
be = lambda n: FC.run('nuclide_binding', {'name': n})['BE_per_A_MeV']; h3 = FC.run('nuclide_lookup', {'name': 'H-3'})['half_life_s'] / 31557600
L['L9_data'] = dict(Fe56=be('Fe-56'), He4=be('He-4'), H3_y=h3, pass_=abs(be('Fe-56') - 8.790) <= .01 and abs(be('He-4') - 7.074) <= .01 and abs(rel(h3, 12.32)) <= .002)
res = dict(tree_pass=all(v['pass_'] for v in L.values()), layers=L)
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'prom9_tree.json'), 'w'), indent=1, default=float)
for k, v in L.items(): print(('PASS ' if v['pass_'] else 'FAIL ') + k, {x: (round(y, 4) if isinstance(y, float) else y) for x, y in v.items() if x != 'pass_'})
print('TREE', res['tree_pass'])
