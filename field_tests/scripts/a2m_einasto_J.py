import sys, math; sys.path.insert(0, '.'); sys.path.insert(0, 'tools/janus_astro')
import warnings; warnings.filterwarnings('ignore')
from astropy import units as u
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
import serapis_inputs as SI
GeV = (u.Msun/u.kpc**3).to(u.GeV/u.cm**3, equivalencies=u.mass_energy()); R0 = 8.178
def Jann(rho, r0): return J.J_route_B(rho, r0, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, r0, psi_max_deg=0.5, b_mask_deg=0.0)
Jb = Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178), 8.178)
CONV = 0.389379e-27*2.99792458e10; Mx = 1000.0; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
sv = {}
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(Mx, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv[lab] = 2*s[1]**2*math.pi*N.ALPHA**2/Mx**2*CONV*k
flo, fhi = SI.wino_fraction(1.0); out = [f"f_pred(1 TeV) = [{flo:.3f}, {fhi:.3f}]"]
for tag, rho0, rcore, al in (('B0/D1', 0.80, 15.29, 1.01), ('B0/D2', 0.83, 14.84, 0.45), ('B0/D3', 0.55, 16.69, 1.35), ('B0/D4', 1.00, 14.29, 0.74), ('B1/D2', 0.57, 15.97, 0.43)):
    rsun = rho0*1e7*math.exp(-2/al*((R0/rcore)**al - 1))*GeV
    jr = Jann(J.normalise(J.einasto(rcore, al), rsun, R0), R0)/Jb
    line = f"{tag}: r_c={rcore} kpc alpha={al} rho_sun={rsun:.3f} GeV/cm3 J/J_bench={jr:.4f}"
    for lab in ('LO', 'NLO'):
        f = [math.sqrt(2.3e-28/(sv[lab]*R*jr)) for R in (0.794, 0.658)]
        v = 'PASS' if f[0] >= fhi else ('FAIL' if f[1] < flo else 'BAND-DEP')
        line += f"; {lab} f_max [{f[0]:.3f},{f[1]:.3f}] {v}"
    out.append(line)
open('field_tests/results/a2m_einasto_J.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
