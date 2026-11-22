#!/usr/bin/env python3
"""D2130: the Weave UFE v4 as a LCDM-format cosmology on compressed Planck 2018 (CHW 4-par) + DESI DR2 BAO. CAMB background."""
import os, sys, json, math, time
import numpy as np, camb
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'cmb-fit'))
from rt_planck_fit import rt_wtable            # exact reverse-thread w(a) (D1636 code)
C = 299792.458
# CHW 2019 Table 1 (4-parameter, verified)
mu_cmb = np.array([1.7502, 301.471, 0.02236, 0.9649]); sg = np.array([0.0046, 0.0895, 0.00015, 0.0043])
rho = np.array([[1, .46, -.66, -.74], [.46, 1, -.33, -.35], [-.66, -.33, 1, .46], [-.74, -.35, .46, 1]])
ICMB = np.linalg.inv(rho*np.outer(sg, sg))
# DESI DR2 Table IV
BGS = (0.295, 7.942, 0.075)
ANI = [(0.510, 13.588, 0.167, 21.863, 0.425, -0.459), (0.706, 17.351, 0.177, 19.455, 0.330, -0.404), (0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
       (1.321, 27.601, 0.318, 14.176, 0.221, -0.434), (1.484, 30.512, 0.760, 12.817, 0.516, -0.500), (2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]
def zstar_hs(wb, wm):
    g1 = 0.0783*wb**-0.238/(1 + 39.5*wb**0.763); g2 = 0.560/(1 + 21.1*wb**1.81)
    return 1048*(1 + 0.00124*wb**-0.738)*(1 + g1*wm**g2)
def model(p, kind):
    wb, wc, H0 = p[0], p[1], p[2]; h = H0/100
    if not (0.015 < wb < 0.03 and 0.08 < wc < 0.16 and 55 < H0 < 80): return None
    ns = 0.9706; mnu = 0.0587; nmass = 3; hier = 'normal'; de = None
    if kind in ('M1', 'M6'): ns = p[3]; mnu = 0.06; nmass = 1; hier = 'degenerate'
    pars = camb.CAMBparams()
    try:
        pars.set_cosmology(H0=H0, ombh2=wb, omch2=wc, mnu=mnu, num_massive_neutrinos=nmass, neutrino_hierarchy=hier, nnu=3.044, TCMB=2.7255, omk=0)
    except Exception: return None
    pars.InitPower.set_params(ns=ns, nrun=-9.7e-4 if kind not in ('M1', 'M6') else 0.0, r=5.4e-4 if kind not in ('M1', 'M6') else 0.0)
    Om = (wb + wc + mnu/93.14)/h**2
    if kind in ('M2', 'M3'):
        ui = p[3] if kind == 'M2' else 0.1129
        if not (1e-4 < ui < 0.9): return None
        tab = rt_wtable(ui, Om, 2.47e-5/h**2*(1 + 0.2271*3.044))
        if tab is None: return None
        a, w = tab; pars.DarkEnergy = camb.dark_energy.DarkEnergyPPF(); pars.DarkEnergy.set_w_a_table(a, w); de = (a, w)
    elif kind == 'M4': pars.set_dark_energy(w=-0.79, wa=-0.36, dark_energy_model='ppf')
    elif kind == 'M6':
        if not (-1.5 < p[4] < -0.3 and -3 < p[5] < 1.5): return None
        pars.set_dark_energy(w=p[4], wa=p[5], dark_energy_model='ppf')
    try: res = camb.get_background(pars)
    except Exception: return None
    der = res.get_derived_params(); rd = der['rdrag']
    zs = zstar_hs(wb, wb + wc + mnu/93.14)
    DMs = res.comoving_radial_distance(zs); rs = res.sound_horizon(zs)
    R = math.sqrt((wb + wc + mnu/93.14))*100*DMs/C; lA = math.pi*DMs/rs
    d = np.array([R, lA, wb, ns]) - mu_cmb; chi_cmb = float(d @ ICMB @ d)
    zb, v, s = BGS; DMb = res.comoving_radial_distance(zb); DHb = C/res.hubble_parameter(zb)
    DV = (zb*DMb**2*DHb)**(1/3)/rd; chi_bao = ((DV - v)/s)**2
    for z, m, sm, hh, sh, r_ in ANI:
        DM = res.comoving_radial_distance(z)/rd; DH = C/res.hubble_parameter(z)/rd
        cov = np.array([[sm**2, r_*sm*sh], [r_*sm*sh, sh**2]]); x = np.array([DM - m, DH - hh])
        chi_bao += float(x @ np.linalg.inv(cov) @ x)
    out = dict(chi2=chi_cmb + chi_bao, chi_cmb=chi_cmb, chi_bao=chi_bao, H0=H0, Om=Om, rd=rd, R=R, lA=lA, ns=ns)
    if de is not None:
        a, w = de; z = 1/a - 1; sel = (z <= 2) & (z >= 0)
        X = np.vstack([np.ones(sel.sum()), 1 - a[sel]]).T; out['thread_w0wa_cpl_fit'] = [float(x) for x in np.linalg.lstsq(X, w[sel], rcond=None)[0]]
        out['thread_w_min'] = float(w[a > 1e-3].min())
    return out
def chi(p, kind):
    m = model(p, kind); return 1e9 if m is None else m['chi2']
STARTS = {'M1': [[0.02236, 0.120, 67.5, 0.965], [0.0225, 0.118, 68.5, 0.970]], 'M2': [[0.02236, 0.119, 67.5, 0.11], [0.0225, 0.118, 66.5, 0.3]],
          'M3': [[0.02236, 0.119, 67.5], [0.0225, 0.118, 68.0]], 'M4': [[0.02236, 0.119, 66.5], [0.0225, 0.118, 67.5]],
          'M5': [[0.02236, 0.119, 67.5], [0.0225, 0.118, 68.5]], 'M6': [[0.02236, 0.120, 66.5, 0.965, -0.8, -0.6], [0.0225, 0.118, 65.0, 0.967, -0.6, -1.2]]}
K = {'M1': 4, 'M2': 4, 'M3': 3, 'M4': 3, 'M5': 3, 'M6': 6}
R = {}
for kind, starts in STARTS.items():
    best = None
    for s in starts:
        r = minimize(chi, s, args=(kind,), method='Nelder-Mead', options={'maxiter': 1500, 'xatol': 1e-6, 'fatol': 1e-4})
        if best is None or r.fun < best.fun: best = r
    m = model(best.x, kind); m['params'] = [float(x) for x in best.x]; m['k'] = K[kind]; R[kind] = m
    print(kind, round(m['chi2'], 3), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items() if k not in ('params',)}, flush=True)
for kind in R: R[kind]['dchi2_vs_M1'] = R[kind]['chi2'] - R['M1']['chi2']; R[kind]['dAIC_vs_M1'] = R[kind]['dchi2_vs_M1'] + 2*(R[kind]['k'] - R['M1']['k'])
d = R['M2']['dAIC_vs_M1']; R['VERDICT'] = 'PREFERRED' if d < -2 else ('CONSISTENT' if d <= 2 else ('MILD TENSION' if d <= 6 else 'DISFAVOURED'))
R['ns_pull_sigma_raw'] = (0.9706 - 0.9649)/0.0043
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weave_lcdm_results.json'), 'w'), indent=1)
print('VERDICT', R['VERDICT'], {k: (round(v['dchi2_vs_M1'], 2), round(v['dAIC_vs_M1'], 2)) for k, v in R.items() if isinstance(v, dict)})
