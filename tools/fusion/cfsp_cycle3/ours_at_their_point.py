import io, json, sys, contextlib; sys.path.insert(0, '.')
import fusion as F, fusion_fast as X
with contextlib.redirect_stdout(io.StringIO()): import test_prom8 as T8
from scipy.optimize import brentq
EA = F.two_body_split('DT')[1]
S = dict(T8.S); S.update(rad_C3=0.6, rho_core=0.75, synch=True)
Sp = dict(S, convention='popcon', synch=False, kappa_A_popcon=True, tau_n_volume=True, V=20.9)
th = json.load(open('/tmp/claude-0/cyc3_points.json'))['theirs']
n = th['n_1e19'] * 1e19; T = th['T_keV']
print('n_avg units check', S['n_avg'], 'f_He', S.get('f_He'), 'V', Sp['V'])
nn = n if S['n_avg'] > 1e10 else n / 1e20
p = X.plasma_fast(Sp, nn, T, EA, Sp['f_He'])
W = 1.5 * nn * T * (1 + p['ions_per_e'] * Sp['Ti_over_Te']) * F.KEV_J * Sp['V'] / 1e6
Ph = brentq(lambda P: W / F.tau_ipb98(Sp, P, nn) - P, 0.1, 2000)
out = dict(n=nn, T=T, P_fus=p['P_fus'], P_alpha=p['P_alpha'], W_MJ=W, P_heat=Ph, tau_E=W / Ph, P_aux_req=Ph - p['P_alpha'], Zeff=p['Zeff'], f_DT=p['f_DT'], P_rad=p['P_rad'])
tP = th['P_fusion']; tA = 7.090796524821792
out['dP_fus'] = out['P_fus'] / tP - 1; out['dP_aux_vs_absorbed'] = out['P_aux_req'] / tA - 1; out['dP_aux_vs_absorbed_plus_ohmic'] = out['P_aux_req'] / (tA + 1.1943) - 1
out['pass_L4'] = abs(out['dP_fus']) <= .25 and abs(out['dP_aux_vs_absorbed']) <= .25
print(json.dumps(out, indent=1))
json.dump(out, open('/tmp/claude-0/cyc3_ours.json', 'w'), indent=1)
