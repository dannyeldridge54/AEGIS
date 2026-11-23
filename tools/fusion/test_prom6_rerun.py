"""PROM-6 rerun with DEV-1..3 (+DEV-5 diagnostic). One rerun only."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
from scipy.optimize import brentq
import test_prom6 as T6   # re-uses the locked machine() builder (its own run re-executes; harmless, results file rewritten below)
EA = F.two_body_split('DT')[1]
SP = dict(T6.SP); fHe = SP['f_He']; SP['f_Be'] = (1 - 0.85 - 2 * fHe) / 4.0          # DEV-1: n_DT/n_e = 0.85
AR = dict(T6.AR)
def t0_ratio(m, T):
    g = X._grid(m); T0 = X._solve_X0(T, g['aT'], g['bT'], g['w'], m['T_ped']); return T0 / T
AR['alpha_T'] = brentq(lambda al: t0_ratio(dict(AR, alpha_T=al), 14.0) - 27 / 14, 0.3, 5.0)   # DEV-2
op = T6.op
out = dict(SPARC=op(SP), ARC=op(AR), ARC_H1=op(dict(AR, H98=1.0)))
diag = {nm: float(X.plasma_fast(m, m['n_avg'], Tp, EA)['P_fus']) for nm, m, Tp in (('SPARC', SP, 7.9), ('ARC', AR, 14.0))}   # DEV-5
w = lambda x, t, tol: x is not None and abs(x / t - 1) <= tol
s, a, a1 = out['SPARC'], out['ARC'], out['ARC_H1']
G = dict(D1=bool(s and w(s['P_fus'], 140, .25) and w(s['Te_avg'], 7.9, .20)), D2=bool(a and w(a['P_fus'], 525, .25) and w(a['Te_avg'], 14.0, .20)),
         D3=bool(a and (a1 is None or abs(a1['P_fus'] / a['P_fus'] - 1) > 0.25)))
it = X.operating_point_fast(F.ITER_400, EA)
res = dict(goals=G, runs=out, P_fus_at_published_T=diag, SPARC_composition=F.composition(SP), ARC_alpha_T=AR['alpha_T'],
           ARC_T0_over_Tavg=t0_ratio(AR, 14.0), ITER400=dict(P_fus=float(it['P_fus']), tau_E=float(it['tau_E'])))
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'prom6_rerun.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('goals', 'P_fus_at_published_T', 'SPARC_composition', 'ARC_alpha_T', 'ITER400')}, indent=0))
for k, v in out.items(): print(k, {x: round(v[x], 3) for x in ('P_fus', 'Te_avg', 'tau_E', 'Q', 'P_loss', 'P_LH', 'P_rad')})
