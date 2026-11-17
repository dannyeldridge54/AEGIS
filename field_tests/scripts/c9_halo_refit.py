import warnings; warnings.filterwarnings('ignore')
import math, numpy as np
from scipy.optimize import least_squares
from galpy.potential import vcirc
from galpy.potential.mwpotentials import McMillan17
G = 4.30091e-6; RO = 8.21
d = np.genfromtxt('field_tests/data/eilers2019_table1.csv', delimiter=',', names=True)
m = d['R_kpc'] <= 20.78; R, V = d['R_kpc'][m], d['vc'][m]; S = 0.5*(d['sig_minus'][m] + d['sig_plus'][m])
bar = [McMillan17[0], McMillan17[2]]
vb2 = lambda r: np.array([float(vcirc(bar, x/RO))**2 for x in np.atleast_1d(r)])
vtot_orig = lambda r: np.array([float(vcirc(McMillan17, x/RO)) for x in np.atleast_1d(r)])
def vnfw2(r, rs_, rss): x = np.atleast_1d(r)/rss; return 4*math.pi*G*rs_*rss**3*(np.log1p(x) - x/(1 + x))/np.atleast_1d(r)
VB2 = vb2(R)
def model(p, r=None, vb=None):
    rs_, rss = 10**p[0], p[1]; r = R if r is None else r; vb = VB2 if vb is None else vb
    return np.sqrt(vb + vnfw2(r, rs_, rss))
out = []
for lab, sig in (('stat', S), ('stat+2%', np.hypot(S, 0.02*V))):
    f = least_squares(lambda p: (model(p) - V)/sig, x0=[math.log10(8.5e6), 19.6], bounds=([5, 2], [9, 80]))
    chi2 = float((f.fun**2).sum()); dof = len(R) - 2
    c0 = float((((vtot_orig(R) - V)/sig)**2).sum())
    r0 = 8.178; h = 0.01; rr = np.array([r0 - h, r0, r0 + h]); v = model(f.x, rr, vb2(rr))
    dv = (v[2] - v[0])/(2*h); Om = v[1]/r0; kap = math.sqrt(2*Om*(Om + dv))
    rho_sun = 10**f.x[0]/((r0/f.x[1])*(1 + r0/f.x[1])**2)*3.8e-8  # Msun/kpc3 -> GeV/cm3 (1 GeV/cm3 = 2.63e7 Msun/kpc3)
    pull = lambda x, mu, up, dn: (x - mu)/(up if x > mu else dn)
    tag = f"{lab}: rho_s={10**f.x[0]:.3e} Msun/kpc3 r_s={f.x[1]:.2f} kpc chi2/dof={chi2/dof:.2f} (McMillan17 orig chi2/dof={c0/dof:.2f})"
    if lab == 'stat': tag += f" Q1 {'PASS' if chi2/dof < 2 else 'FAIL'}"
    tag += f" | v_c(8.178)={v[1]:.1f} (Horta pull {pull(v[1],235.3,2.8,3.7):+.2f}) dv/dR={dv:+.2f}" + (f" Q2 {'PASS' if dv < 0 else 'FAIL'}" if lab == 'stat' else '')
    tag += f" Omega={Om:.2f} ({pull(Om,28.5,0.4,0.1):+.1f}) kappa={kap:.2f} ({pull(kap,36.9,0.8,1.0):+.2f}) rho_DM_sun~{rho_sun:.3f} GeV/cm3"
    out.append(tag)
open('field_tests/results/c9_halo_refit.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
