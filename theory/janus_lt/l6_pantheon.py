"""L6 (locked PREREG_L6_pantheonplus): Pantheon+ SN-only flat LCDM Omega_m with Janus-LT distances."""
import sys, math, numpy as np; sys.path.insert(0, '.')
from tools.janus_lt.background import Cosmo
from scipy.integrate import cumulative_trapezoid
D = np.genfromtxt('data/sn/Pantheon+SH0ES.dat', names=True, dtype=None, encoding=None)
C = np.loadtxt('data/sn/Pantheon+SH0ES_STAT+SYS.cov', skiprows=1).reshape(1701, 1701)
zg = np.concatenate([np.linspace(0, 0.1, 4001), np.linspace(0.1, 2.4, 23001)[1:]])
def DMgrid(om, h=0.7, ob=0.0224):
    c = Cosmo(100*h, ob, om*h*h - ob); E = np.array([c.E(z) for z in zg[::10]])
    Ef = np.interp(zg, zg[::10], E)  # E is smooth; spacing 1e-3 or less
    return 299792.458/(100*h)*cumulative_trapezoid(1/Ef, zg, initial=0.0)
def run(mask, tag, L):
    m = D['m_b_corr'][mask]; zh = D['zHD'][mask]; zl = D['zHEL'][mask]; Ci = np.linalg.inv(C[np.ix_(mask, mask)]); one = np.ones(mask.sum())
    e = one @ Ci @ one; oms = np.arange(0.20, 0.45001, 0.0005); X = []
    for om in oms:
        dm = np.interp(zh, zg, DMgrid(om)); r = m - 5*np.log10((1+zl)*dm*1e6/10)
        a = r @ Ci @ r; b = one @ Ci @ r; X.append(a - b*b/e + math.log(e/(2*math.pi)))
    X = np.array(X); i = X.argmin(); ok = oms[X - X[i] <= 1.0]
    L.append(f"{tag}: N = {mask.sum()}, Omega_m = {oms[i]:.4f} (+{ok.max()-oms[i]:.4f} / -{oms[i]-ok.min():.4f}), chi2_min = {X[i]:.2f}"); print(L[-1], flush=True)
    return oms[i], 0.5*(ok.max()-ok.min())
L = []
# check: grid DM vs quad at Om = 0.3
c = Cosmo(70, 0.0224, 0.3*0.49 - 0.0224); g = DMgrid(0.3)
for z in (0.01, 0.5, 2.26): L.append(f"grid check z={z}: |dDM/DM| = {abs(np.interp(z, zg, g)/c.DM(z)-1):.1e}")
print('\n'.join(L), flush=True)
oa, sa = run(D['zHD'] > 0.01, '(a) zHD > 0.01', L); run(np.ones(1701, bool), '(b) all', L)
v = abs(oa - 0.334) <= 0.009
L.append(f"(a) vs Brout+22 0.334 ± 0.018: diff {oa-0.334:+.4f} -> {'REPRODUCED' if v else 'NOT REPRODUCED'}")
open('field_tests/results/janus_lt_l6_pantheon.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
