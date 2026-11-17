import sys, math; sys.path.insert(0, '.')
import warnings; warnings.filterwarnings('ignore')
from astropy import units as u, constants as K
from astropy.cosmology import FlatLambdaCDM
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
rc = FlatLambdaCDM(H0=67.66, Om0=0.31).critical_density0.to(u.Msun/u.kpc**3).value
GeV = (u.Msun/u.kpc**3).to(u.GeV/u.cm**3, equivalencies=u.mass_energy())
R0 = 8.178
def halo(M, c):
    r200 = (3*M/(4*math.pi*200*rc))**(1/3); rs = r200/c
    m = math.log(1+c) - c/(1+c); rho0 = M/(4*math.pi*rs**3*m)
    rho_sun = rho0/((R0/rs)*(1+R0/rs)**2)*GeV
    return rs, rho_sun
def Jann(rho, r0): return J.J_route_B(rho, r0, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, r0, psi_max_deg=0.5, b_mask_deg=0.0)
Jb = Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178), 8.178)
CONV = 0.389379e-27*2.99792458e10; Mx = 1000.0; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
sv = {}
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(Mx, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv[lab] = 2*s[1]**2*math.pi*N.ALPHA**2/Mx**2*CONV*k
out = []
for tag, M, c in (('central', 0.55e12, 13.9), ('M-1s', 0.40e12, 13.9), ('M+1s', 0.70e12, 13.9), ('c-1s', 0.55e12, 9.6), ('c+1s', 0.55e12, 20.1)):
    rs, rsun = halo(M, c); jr = Jann(J.normalise(J.nfw(rs), rsun, R0), R0)/Jb
    line = f"{tag}: r_s={rs:.1f} kpc rho_sun={rsun:.3f} GeV/cm3 J/J_bench={jr:.3f}"
    for lab in ('LO', 'NLO'):
        f = [math.sqrt(2.3e-28/(sv[lab]*R*jr)) for R in (0.794, 0.658)]
        v = 'PASS' if f[0] >= 0.26 else ('FAIL' if f[1] < 0.26 else 'BAND-DEP')
        line += f"; {lab} f_max [{f[0]:.3f},{f[1]:.3f}] {v}"
    out.append(line)
open('field_tests/results/a2j_gaia_halo.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
