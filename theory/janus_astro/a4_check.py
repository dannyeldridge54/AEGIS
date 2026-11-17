import math, sys, numpy as np
sys.path.insert(0, '.')
from colossus.cosmology import cosmology; from colossus.lss import mass_function as mf
from tools.janus_astro import hmf
from tools.janus_lt.background import Cosmo
from tools.janus_lt.growth import growth
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b); ok = {}
cc = cosmology.setCosmology('planck18'); h = cc.H0/100
jl = Cosmo(cc.H0, cc.Ob0*h*h, (cc.Om0 - cc.Ob0)*h*h, Neff=3.046, Tcmb=2.7255)
zs = [0.5, 1, 2, 5]; g = growth(jl, [0.0] + zs)
o = True
for z in zs:
    a, b = g[z][0], float(cc.growthFactor(z)); e = rel(a, b); o &= e <= 1e-3; P(f'M1 z={z}: D ours={a:.6f} colossus={b:.6f} rel={e:.1e}')
ok['M1'] = o
kk = np.logspace(-4, np.log10(50), 3000); Pk = cc.matterPowerSpectrum(kk); rho = hmf.RHO_CRIT_H2*cc.Om0
def ours(M, z, model, Dz):
    R = (3*M/(4*math.pi*rho))**(1/3); s0 = hmf.sigma_R(kk, Pk, R); e = 1e-3
    s1 = hmf.sigma_R(kk, Pk, R*(1+e)**(1/3)); sm = hmf.sigma_R(kk, Pk, R*(1-e)**(1/3)); dl = (math.log(s1) - math.log(sm))/(math.log(1+e) - math.log(1-e))
    s = s0*Dz
    f = {'press74': lambda: mf.modelPress74(s, z), 'sheth99': lambda: mf.modelSheth99(s, z), 'tinker08': lambda: mf.modelTinker08(s, z, '200m')}[model]()
    return float(f)*rho/M*abs(dl)
o = True
for model, mdef in [('press74', 'fof'), ('sheth99', 'fof'), ('tinker08', '200m')]:
    for z, Ms in [(0, [1e12, 1e13, 1e14, 1e15]), (1, [1e12, 1e13, 1e14]), (2, [1e12, 1e13, 1e14])]:
        Dz = 1.0 if z == 0 else g[z][0]
        for M in Ms:
            a = ours(M, z, model, Dz); b = float(mf.massFunction(M, z, mdef=mdef, model=model, q_out='dndlnM'))
            a2 = ours(M, z, model, float(cc.growthFactor(z)))
            e = rel(a, b); o &= e <= 2e-2
            P(f'M2 {model} z={z} M={M:.0e}: ours={a:.5e} colossus={b:.5e} rel={e:.1e} (with colossus growth: {rel(a2,b):.1e})')
ok['M2'] = o
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A4', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
open('field_tests/results/janus_astro_a4.txt', 'w').write('\n'.join(out) + '\n')
