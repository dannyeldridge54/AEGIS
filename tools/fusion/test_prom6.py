"""PROM-6 DEVICES (PREREG_PROM6_DEVICES): the ITER-tuned 0-D engine on SPARC and ARC, unchanged except the locked mechanical inputs."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
EA = F.two_body_split('DT')[1]; I = F.ITER
cV = I['V'] / (2 * math.pi ** 2 * I['R'] * I['a'] ** 2 * I['kappa'])
cS = I['S'] / (4 * math.pi ** 2 * I['R'] * I['a'] * math.sqrt((1 + I['kappa'] ** 2) / 2))
def machine(R, a, kappa, B, Ip, n_avg, P_aux, T_pub, H98, Zeff, f_W=0.0, V=None):
    fHe = I['f_He']; fBe = (Zeff - 1 - 2 * fHe) / 12.0
    m = dict(I); m.update(R=R, a=a, kappa=kappa, B=B, Ip=Ip, V=V or cV * 2 * math.pi ** 2 * R * a ** 2 * kappa,
                          S=cS * 4 * math.pi ** 2 * R * a * math.sqrt((1 + kappa ** 2) / 2), n_avg=n_avg, P_aux=P_aux, H98=H98,
                          f_Be=fBe, f_Ar=0.0, f_W=f_W, Ti_over_Te=1.0, line_model='adas',
                          n_ped=0.708 * n_avg, n_sep=0.354 * n_avg, T_ped=0.39 * T_pub, src='PROM-6')
    m['n_ped'] = I['n_ped'] / I['n_avg'] * n_avg; m['n_sep'] = I['n_sep'] / I['n_avg'] * n_avg
    return m
def nG(Ip, a): return Ip / (math.pi * a ** 2) * 1e20
SP = machine(1.85, 0.57, 1.97, 12.2, 8.7, 0.37 * nG(8.7, 0.57), 140 / 11.2, 7.9, 1.0, 1.5, f_W=1.5e-5)
AR = machine(3.3, 1.13, 1.84, 9.2, 7.8, 1.3e20, 38.6, 14.0, 1.8, 1.5, V=141.0)
def op(m): 
    o = X.operating_point_fast(m, EA)
    return None if o is None else {k: float(o[k]) for k in ('P_fus', 'Q', 'tau_E', 'Te_avg', 'P_rad', 'f_He', 'f_G', 'beta_N', 'P_loss', 'P_LH')}
out = {}
out['SPARC'] = op(SP); out['ARC'] = op(AR); out['ARC_H1'] = op(dict(AR, H98=1.0))
rob = {}
for nm, m in (('SPARC', SP), ('ARC', AR)):
    for f in (0.7, 1.3): rob[f'{nm}_Tped_x{f}'] = op(dict(m, T_ped=m['T_ped'] * f))
within = lambda x, t, tol: x is not None and abs(x / t - 1) <= tol
s, a, a1 = out['SPARC'], out['ARC'], out['ARC_H1']
G = dict(D1=bool(s and within(s['P_fus'], 140, .25) and within(s['Te_avg'], 7.9, .20)),
         D2=bool(a and within(a['P_fus'], 525, .25) and within(a['tau_E'], 0.64, .25) and within(a['Te_avg'], 14.0, .20)),
         D3=bool(a and (a1 is None or abs(a1['P_fus'] / a['P_fus'] - 1) > 0.25)))
iter400 = X.operating_point_fast(F.ITER_400, EA)
res = dict(goals=G, runs=out, robustness=rob, geometry=dict(SPARC_V=SP['V'], SPARC_S=SP['S'], ARC_S=AR['S'], cV=cV, cS=cS),
           ITER400_regression=dict(P_fus=float(iter400['P_fus']), tau_E=float(iter400['tau_E'])))
if __name__ == '__main__': json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'prom6_devices.json'), 'w'), indent=1)
if __name__ == '__main__': print(json.dumps(res, indent=1)[:3500])
