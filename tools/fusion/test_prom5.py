"""PROM-5 goalposts L1-L4, run once as locked."""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F, fusion_fast as X, adas as A
t0 = time.time(); Ea = F.two_body_split('DT')[1]
L1 = {}
for el in ('he', 'be', 'ar', 'w'):
    sums = [abs(A.fractions(el, ne, T).sum() - 1) for ne in (1e19, 1e20) for T in (0.01, 0.1, 1, 8, 30)]
    L1[el] = dict(max_sum_err=max(sums), top2_8keV=float(sum(sorted(A.fractions(el, 1e20, 8.0))[-2:])), He_stripped_1keV=float(A.fractions('he', 1e20, 1.0)[-1]) if el == 'he' else None)
L1['pass_'] = all(v['max_sum_err'] <= 1e-10 for v in L1.values() if isinstance(v, dict)) and L1['ar']['top2_8keV'] >= 0.9 and L1['he']['He_stripped_1keV'] > 0.99
m = dict(F.ITER, line_model='adas'); m4 = dict(F.ITER_400, line_model='adas')
old5 = X.operating_point_fast(F.ITER, Ea); a = X.operating_point_fast(m, Ea)
p_at_old = X.plasma_fast(m, F.ITER['n_avg'], old5['Te_avg'], Ea, old5['f_He'])        # same plasma state as PROM-1, line radiation derived
L2 = dict(P_line_derived_at_PROM1_state=p_at_old['P_line'], table=27.0, rel=p_at_old['P_line'] / 27 - 1); L2['pass_'] = abs(L2['rel']) <= 0.40
b = X.operating_point_fast(m4, Ea); w_ = lambda x, c, t: abs(x / c - 1) <= t
P1 = {k: a[k] for k in ('P_fus', 'Q', 'tau_E', 'W_MJ', 'beta_N', 'P_line', 'P_rad', 'P_loss', 'P_LH', 'f_He', 'Te_avg')}
P2 = {k: b[k] for k in ('P_fus', 'Q', 'tau_E', 'W_MJ', 'P_line', 'f_He')}; P2['pass_'] = bool(w_(b['P_fus'], 400, .2) and w_(b['tau_E'], 3.7, .15) and w_(b['Q'], 10, .3))
d = lambda o: sum(abs(o[k] / v - 1) for k, v in dict(P_fus=500, tau_E=3.4, W_MJ=353, beta_N=2.0).items())
L3 = dict(P1=P1, P2_heldout=P2, d500_before=d(old5), d500_after=d(a)); L3['accept'] = bool(P2['pass_'] and L3['d500_after'] <= L3['d500_before'])
pAr = X.plasma_fast(dict(m, f_Ar=m['f_Ar'] * 1.1), F.ITER['n_avg'], old5['Te_avg'], Ea, old5['f_He'])['P_line']
L3['F2_sensitivity_fAr+10%'] = pAr / p_at_old['P_line'] - 1
L4 = dict(W_L_1keV=A.L_line('w', 1e20, 1.0), W_L_5keV=A.L_line('w', 1e20, 5.0), W_L_10keV=A.L_line('w', 1e20, 10.0), note='Puetterich 2019: c_W,max ~1.9e-4 (DEMO); W cooling ~1e-31 W m^3 near 1-2 keV')
r = dict(L1=L1, L2=L2, L3=L3, L4=L4, seconds=round(time.time() - t0, 1))
json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'prom5.json'), 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
