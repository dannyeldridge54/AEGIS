import sys, math; sys.path.insert(0, '.'); sys.path.insert(0, 'tools/janus_astro'); sys.path.insert(0, 'theory/wiring')
import warnings; warnings.filterwarnings('ignore')
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
import serapis_inputs as SI
import importlib.util
spec = importlib.util.spec_from_file_location('nll', 'theory/wiring/a2d_line_nll.py')
src = open('theory/wiring/a2d_line_nll.py').read().split("out = []")[0]; nll = {}; exec(src, nll)
R0 = 8.178; CONV = 0.389379e-27*2.99792458e10
def Jann(rho, r0): return J.J_route_B(rho, r0, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, r0, psi_max_deg=0.5, b_mask_deg=0.0)
Jb = Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178), 8.178)
rc = FlatLambdaCDM(H0=67.66, Om0=0.31).critical_density0.to(u.Msun/u.kpc**3).value
GeV = (u.Msun/u.kpc**3).to(u.GeV/u.cm**3, equivalencies=u.mass_energy())
def nfw_gaia(M=0.55e12, c=13.9):
    r200 = (3*M/(4*math.pi*200*rc))**(1/3); rs = r200/c; m = math.log(1+c) - c/(1+c); rho0 = M/(4*math.pi*rs**3*m)
    return J.nfw(rs), rho0/((R0/rs)*(1+R0/rs)**2)*GeV
halos = [('HESS bench', None, None)]
sh, rsun = nfw_gaia(); halos.append(('Gaia NFW', sh, rsun))
for tag, s in [('Bur B0/D1', J.burkert(3.37)), ('Bur B0/D2', J.burkert(3.79)), ('Bur B0/D3', J.burkert(2.91)), ('Bur B0/D4', J.burkert(2.87)), ('Bur B1/D2', J.burkert(4.13)),
               ('Ein B0/D1', J.einasto(15.29, 1.01)), ('Ein B0/D2', J.einasto(14.84, 0.45)), ('Ein B0/D3', J.einasto(16.69, 1.35)), ('Ein B0/D4', J.einasto(14.29, 0.74)), ('Ein B1/D2', J.einasto(15.97, 0.43))]:
    halos.append((tag, s, 0.40))
jr = {t: (1.0 if s is None else Jann(J.normalise(s, r, R0), R0)/Jb) for t, s, r in halos}
R1 = nll['Sig'](1000.0); 
def Rcen(M):
    S1, S12, *_ = nll['Sig'](M); out = {}
    for lab, nlo in (('LO', False), ('NLO', True)):
        s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2))
        out[lab] = abs(s[0]*S12 + math.sqrt(2)*s[1]*S1)**2/abs(math.sqrt(2)*s[1])**2
    return out
r1 = Rcen(1000.0); lines = []; edge_ok = {}
for Mt in (1.0, 1.25, 1.5):
    M = Mt*1000; k = 1 + N.ALPHA2*N.CW2/N.ALPHA; lim = 2.3e-28*Mt**(math.log(6.5/2.3)/math.log(2.9)); flo, fhi = SI.wino_fraction(Mt); rc_ = Rcen(M)
    lines.append(f"M={Mt} TeV: limit={lim:.3e} f_pred=[{flo:.3f},{fhi:.3f}] Rcen LO {rc_['LO']:.3f} NLO {rc_['NLO']:.3f}")
    allpass = True
    for t, _, _ in halos:
        seg = f"  {t}: J/Jb={jr[t]:.4f}"
        for lab, nlo in (('LO', False), ('NLO', True)):
            s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv = 2*s[1]**2*math.pi*N.ALPHA**2/M**2*CONV*k
            band = [rc_[lab]*0.794/r1[lab], rc_[lab]*0.658/r1[lab]] if Mt != 1.0 else [0.794, 0.658]
            f = [math.sqrt(lim/(sv*R*jr[t])) for R in band]
            v = 'PASS' if f[0] >= fhi else ('FAIL' if f[1] < flo else 'BAND-DEP')
            seg += f"; {lab} [{f[0]:.3f},{f[1]:.3f}] {v}"
            if t not in ('HESS bench',) and lab == 'LO' and v != 'PASS': allpass = False
            if Mt == 1.0 and t == 'Bur B0/D1' and lab == 'LO': s1 = f[0]
        lines.append(seg)
    edge_ok[Mt] = allpass
lines.append(f"S1 check: B0/D1 LO lower f_max at 1 TeV = {s1:.3f} vs A2n 0.286 -> {'OK' if abs(s1/0.286-1) <= 0.01 else 'STOP'}")
lines.append("All Gaia/Singh-Desai haloes PASS (LO): " + ", ".join(f"{m} TeV: {edge_ok[m]}" for m in edge_ok))
open('field_tests/results/a2o_upper_edge.txt', 'w').write("\n".join(lines)+"\n"); print("\n".join(lines))
