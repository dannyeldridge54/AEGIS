import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import hmf
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b)
from colossus.cosmology import cosmology as _cc; _cc.setCosmology('planck18')   # A7d D1: colossus cosmology set before first modelTinker08 call
c0 = hmf.camb_linear(0.0); c1 = hmf.camb_linear(0.0587)
ok1 = True
for nm, c in [('massless', c0), ('0.0587 eV', c1)]:
    s8 = hmf.sigma_R(c['k'], c['Pm'], 8.0); e = rel(s8, c['sigma8']); ok1 &= e <= 2e-3
    P(f'H1 {nm}: sigma8 integral={s8:.5f} CAMB={c["sigma8"]:.5f} rel={e:.1e}')
from colossus.cosmology import cosmology; from colossus.lss import mass_function as mf
cosmo = cosmology.setCosmology('planck18'); kk = np.logspace(-4, np.log10(50), 3000); Pk = cosmo.matterPowerSpectrum(kk)
rho_m = hmf.RHO_CRIT_H2*cosmo.Om0*1e9   # colossus rho in Msun h^2/kpc^3 *1e9 -> per Mpc^3
ok2 = True
for M in [1e12, 1e13, 1e14, 1e15]:
    ours = hmf.dndlnM(M, kk, Pk, hmf.RHO_CRIT_H2*cosmo.Om0)[0]
    col = float(mf.massFunction(M, 0.0, mdef='200m', model='tinker08', q_out='dndlnM'))
    e = rel(ours, col); ok2 &= e <= 1e-2; P(f'H2 M={M:.0e}: ours={ours:.5e} colossus={col:.5e} rel={e:.1e}')
P('A7d machinery', 'VALIDATED' if ok1 and ok2 else 'NOT VALIDATED', f'(H1 {ok1}, H2 {ok2})')
h = c0['h']; fnu = (0.0587/93.14/h**2)/c1['Om']
P(f'Application: f_nu = {fnu:.5f}; sigma8 total {c0["sigma8"]:.5f} -> {c1["sigma8"]:.5f} ({c1["sigma8"]/c0["sigma8"]-1:+.4f}); '
  f'sigma8_cb {hmf.sigma_R(c0["k"], c0["Pcb"], 8):.5f} -> {hmf.sigma_R(c1["k"], c1["Pcb"], 8):.5f}; small-scale P_m ratio at k=10 h/Mpc: '
  f'{np.interp(10, c1["k"], c1["Pm"])/np.interp(10, c0["k"], c0["Pm"]) - 1:+.4f} (rule of thumb -8 f_nu = {-8*fnu:+.4f})')
r0 = hmf.RHO_CRIT_H2*c0['Om']; r1 = hmf.RHO_CRIT_H2*c1['Ocb']
for M in [1e13, 1e14, 1e15]:
    n0 = hmf.n_above(M, c0['k'], c0['Pcb'], r0); n1 = hmf.n_above(M, c1['k'], c1['Pcb'], r1)
    P(f'  n(>{M:.0e} Msun/h): {n0:.4e} -> {n1:.4e} h^3/Mpc^3, ratio {n1/n0:.4f} ({n1/n0-1:+.2%})')
open('field_tests/results/janus_astro_a7d.txt', 'w').write('\n'.join(out) + '\n')
