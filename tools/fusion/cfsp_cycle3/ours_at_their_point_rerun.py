"""Cycle 3 rerun (STAGEMAP_CYCLE3_SPARC_DEVIATIONS DEV-2..4): our engine at cfspopcon's PRD cell, SPARC dict rebuilt at (n, T) by the PROM-8 recipe."""
import io, json, os, sys, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import fusion as F, fusion_fast as X
with contextlib.redirect_stdout(io.StringIO()): import test_prom6 as T6, test_prom7 as T7, test_prom8 as T8
from scipy.optimize import brentq
EA = F.two_body_split('DT')[1]
RES = os.path.join(HERE, '..', '..', '..', 'field_tests', 'results', 'stagemap_cycle3_sparc.json')
R = json.load(open(RES)); th = R['their_code_their_radas']
n, T = th['n_1e19'] * 1e19, th['T_keV']
def engine(n_pk):
    S = dict(T8.S); S.update(n_avg=n, n_ped=2.7 / 3.1 * n, T_ped=0.39 * T, n_sep=T8.S['n_sep'] * n / 3.1e20)
    S, notes = T7.shape(S, n_pk, 2.5, T)
    S.update(rad_C3=0.6, rho_core=0.75); Sp = dict(S, convention='popcon', synch=False, kappa_A_popcon=True, tau_n_volume=True, V=20.9)
    p = X.plasma_fast(Sp, n, T, EA, Sp['f_He'])
    W = 1.5 * n * T * (1 + p['ions_per_e'] * Sp['Ti_over_Te']) * F.KEV_J * Sp['V'] / 1e6
    Ph = brentq(lambda P: W / F.tau_ipb98(Sp, P, n) - P, 0.1, 2000)
    return dict(n_pk=n_pk, P_fus=p['P_fus'], P_alpha=p['P_alpha'], W_MJ=W, P_heat=Ph, tau_E=W / Ph, P_aux_req=Ph - p['P_alpha'], ne0_over_avg=p['ne0'] / n, Te0=p['Te0'], notes=notes)
A_abs, P_ohm, A_launch = 7.0979, 1.1943, th['P_auxiliary_launched']
o = engine(1.3); side = engine(1.5)
o.update(dP_fus=o['P_fus'] / th['P_fusion'] - 1, dPaux_vs_abs_plus_ohmic=o['P_aux_req'] / (A_abs + P_ohm) - 1,
         dPaux_vs_abs=o['P_aux_req'] / A_abs - 1, dPaux_vs_launched_plus_ohmic=o['P_aux_req'] / (A_launch + P_ohm) - 1)
ok = abs(o['dP_fus']) <= .25 and abs(o['dPaux_vs_abs_plus_ohmic']) <= .25
o['B_L4'] = 'EDGE' if ok else 'OUT'
R['rerun'] = dict(engine_npk13=o, side_npk15=side, rule='STAGEMAP_CYCLE3_SPARC_DEVIATIONS: pass -> EDGE (ceiling), else OUT')
if __name__ == '__main__':
    json.dump(R, open(RES, 'w'), indent=1); print(json.dumps(R['rerun'], indent=1, default=str))
