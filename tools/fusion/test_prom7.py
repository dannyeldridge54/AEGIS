"""PROM-7 (PREREG_PROM7_PROFILES): published peaking as inputs; prescribed-profile P_fus (P1), SPARC power balance (P2), ARC implied H98 (P3)."""
import io, json, math, os, sys, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
from scipy.optimize import brentq
with contextlib.redirect_stdout(io.StringIO()): import test_prom6 as T6
EA = F.two_body_split('DT')[1]
def ratio(m, which, avg):
    g = X._grid(m); a, b, Xp = (g['an'], g['bn'], m['n_ped']) if which == 'n' else (g['aT'], g['bT'], m['T_ped'])
    return X._solve_X0(avg, a, b, g['w'], Xp) / avg
def shape(m, n_pk, T_pk, Tavg):
    m = dict(m); notes = []
    m['alpha_n'] = brentq(lambda al: ratio(dict(m, alpha_n=al), 'n', m['n_avg']) - n_pk, 1e-3, 30)
    for k in range(40):
        try:
            m['alpha_T'] = brentq(lambda al: ratio(dict(m, alpha_T=al), 'T', Tavg) - T_pk, 1e-3, 30); break
        except ValueError:
            m['T_ped'] *= 0.9; notes.append(f"T_ped lowered to {m['T_ped']:.3f}")
    return m, notes
SP = dict(T6.SP); SP['f_Be'] = (1 - 0.85 - 2 * SP['f_He']) / 4.0; SP['n_ped'] = 2.7e20
AR = dict(T6.AR); AR['f_Be'] = (1.2 - 1 - 2 * AR['f_He']) / 12.0
SPp, nS = shape(SP, 1.3, 2.5, 7.9); ARp, nA = shape(AR, 1.75 / 1.3, 27 / 13.9, 13.9)
pf = lambda m, T: float(X.plasma_fast(m, m['n_avg'], T, EA)['P_fus'])
P1 = dict(SPARC=pf(SPp, 7.9), ARC=pf(ARp, 13.9)); P1_old = dict(SPARC=pf(SP, 7.9), ARC=pf(AR, 13.9))
o = X.operating_point_fast(SPp, EA); P2 = None if o is None else {k: float(o[k]) for k in ('P_fus', 'Te_avg', 'tau_E', 'Q', 'P_loss', 'P_LH', 'P_rad')}
p = X.plasma_fast(ARp, ARp['n_avg'], 13.9, EA); PL = F._ploss(ARp, p, ARp['P_aux']); t98 = F.tau_ipb98(dict(ARp, H98=1.0), PL, p['n_line'])
P3 = dict(W_MJ=float(p['W_MJ']), P_loss=float(PL), tau_needed=float(p['W_MJ'] / PL), tau98_H1=float(t98), H98_implied=float(p['W_MJ'] / PL / t98))
w = lambda x, t, tol: x is not None and abs(x / t - 1) <= tol
G = dict(P1_SPARC=w(P1['SPARC'], 140, .2), P1_ARC=w(P1['ARC'], 525, .2),
         P2=bool(P2 and w(P2['P_fus'], 140, .25) and w(P2['Te_avg'], 7.9, .2)),
         C1=all(abs(P1[k] / P1_old[k] - 1) > 0.15 for k in P1))
it = X.operating_point_fast(F.ITER_400, EA); G['C2'] = abs(it['P_fus'] - 389.53) < 0.5 and abs(it['tau_E'] - 3.406) < 0.005
res = dict(goals=G, P1=P1, P1_PROM6_shapes=P1_old, P2_SPARC=P2, P3_ARC=P3, shapes=dict(SPARC=dict(alpha_n=SPp['alpha_n'], alpha_T=SPp['alpha_T'], T_ped=SPp['T_ped'], notes=nS),
           ARC=dict(alpha_n=ARp['alpha_n'], alpha_T=ARp['alpha_T'], T_ped=ARp['T_ped'], notes=nA)), comp=dict(SPARC=F.composition(SPp), ARC=F.composition(ARp)),
           ITER400=dict(P_fus=float(it['P_fus']), tau_E=float(it['tau_E'])))
if __name__ == '__main__': json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'prom7_profiles.json'), 'w'), indent=1)
if __name__ == '__main__': print(json.dumps(res, indent=1))
