"""EZ1 (locked PREREG_EZ1): eternal inflation + swampland scorecard per SERAPIS branch (Janus models)."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc import models as J
L = []
branches = [('SERAPIS-E C=1.15e-6', lambda: J.serapis_E(1.15e-6)), ('Chronos eps=1.3e-4', lambda: J.chronos(1.3e-4)),
            ('SERAPIS-rho eps=6e-5', lambda: J.serapis_rho(6e-5)), ('Kairos', lambda: J.chronos(0.0))]
for name, mk in branches:
    m = mk(); s = m.sol; Nend = m.Nend
    Ns = np.linspace(0, Nend - 1e-3, 4000); y = s.sol(Ns); phi, pn = y[0], y[1]
    eps = pn**2/2; V = np.array([m.V(p) for p in phi]); H2 = V/(3 - eps)
    PR = H2/(8*math.pi**2*eps)
    # extend up the plateau: slow-roll P_R = V/(24 pi^2 eps_V) at larger field (beyond the start), within the spline range
    p0 = phi[0]; ext = np.linspace(p0, p0 + 3.0, 300) if phi[-1] < p0 else np.linspace(p0, p0 - 3.0, 300)
    PRx = []
    for p in ext:
        try:
            v = m.V(p); dv = m.dV(p); ev = 0.5*(dv/v)**2; PRx.append(v/(24*math.pi**2*ev) if ev > 0 else float('inf'))
        except Exception: break
    Np0 = Nend - 50.0; norm = 2.1e-9/PR[np.argmin(abs(Ns - Np0))]          # DEVIATIONS D1: physical amplitude A_s at the pivot
    PR = PR*norm; PRx = [x*norm for x in PRx]
    PRmax = max(PR.max(), max(PRx) if PRx else 0)
    i1 = np.argmax(PR >= 1) if (PR >= 1).any() else None
    eternal = (PR >= 1).any() or any(x >= 1 for x in PRx)
    where = (f"within the computed background at N_before_end = {Nend - Ns[i1]:.1f}" if i1 is not None else
             ("only on the extended plateau above the start" if eternal else "nowhere in range"))
    # scorecard at N* = 50
    Np = Nend - 50.0; yp = s.sol(Np); pp = yp[0]; h = 1e-4
    Vp = m.V(pp); slope = abs(m.dV(pp))/Vp; Vpp = (m.dV(pp + h) - m.dV(pp - h))/(2*h)/Vp
    dphi60 = abs(s.sol(Nend - 60.0)[0] - s.sol(Nend)[0]); r = m.spectra(50.0)['r']
    L.append(f"{name}: E: max P_R in range {PRmax:.3e} -> {'ETERNAL WITHIN RANGE' if eternal else 'NOT WITHIN RANGE'} ({where}); P_R at pivot {PR[np.argmin(abs(Ns-Np))]:.2e}")
    L.append(f"   Z: |V'|/V at N*=50 = {slope:.2e} ({'violates' if slope < 0.1 else 'satisfies'} dS slope ~O(1)); V''/V = {Vpp:.2e} ({'violates' if Vpp > -0.1 else 'satisfies'} refined dS); "
             f"field range (60 e-folds) = {dphi60:.2f} M_P ({'satisfies' if dphi60 < 1 else 'tension with'} distance ~O(1)); r = {r:.2e} ({'violates' if r > 1e-30 else 'satisfies'} TCC r<1e-30)")
    print(L[-2]); print(L[-1], flush=True)
open('field_tests/results/eternal_swampland_ez1.txt', 'w').write('\n'.join(L) + '\n')
