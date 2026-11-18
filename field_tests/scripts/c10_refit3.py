import warnings; warnings.filterwarnings('ignore')
import math, numpy as np
from scipy.optimize import least_squares
from galpy.potential import vcirc
from galpy.potential.mwpotentials import McMillan17
G = 4.30091e-6; RO = 8.21
d = np.genfromtxt('field_tests/data/eilers2019_table1.csv', delimiter=',', names=True)
m = d['R_kpc'] <= 20.78; R, V = d['R_kpc'][m], d['vc'][m]; S = 0.5*(d['sig_minus'][m] + d['sig_plus'][m])
vdisk2 = lambda r: np.array([float(vcirc(McMillan17[0], x/RO))**2 for x in np.atleast_1d(r)])
vbul2 = lambda r: np.array([float(vcirc(McMillan17[2], x/RO))**2 for x in np.atleast_1d(r)])
vb2 = lambda r: (vdisk2(r), vbul2(r))
vtot_orig = lambda r: np.array([float(vcirc(McMillan17, x/RO)) for x in np.atleast_1d(r)])
def vnfw2(r, rs_, rss): x = np.atleast_1d(r)/rss; return 4*math.pi*G*rs_*rss**3*(np.log1p(x) - x/(1 + x))/np.atleast_1d(r)
VB2 = vb2(R)
def model(p, r=None, vb=None):
    fd, rs_, rss = p[0], 10**p[1], p[2]; r = R if r is None else r; vb = VB2 if vb is None else vb
    return np.sqrt(fd*vb[0] + vb[1] + vnfw2(r, rs_, rss))
out = []
for lab, sig in (('stat', S), ('stat+2%', np.hypot(S, 0.02*V))):
    f = least_squares(lambda p: (model(p) - V)/sig, x0=[1.0, math.log10(8.5e6), 19.6], bounds=([0.5, 4, 10], [1.5, 10, 25]))
    chi2 = float((f.fun**2).sum()); dof = len(R) - 3
    c0 = float((((vtot_orig(R) - V)/sig)**2).sum())
    r0 = 8.178; h = 0.01; rr = np.array([r0 - h, r0, r0 + h]); v = model(f.x, rr, vb2(rr))
    dv = (v[2] - v[0])/(2*h); Om = v[1]/r0; kap = math.sqrt(2*Om*(Om + dv))
    rho_sun = 10**f.x[1]/((r0/f.x[2])*(1 + r0/f.x[2])**2)*3.8e-8  # Msun/kpc3 -> GeV/cm3 (1 GeV/cm3 = 2.63e7 Msun/kpc3)
    pull = lambda x, mu, up, dn: (x - mu)/(up if x > mu else dn)
    lo=[0.5,4,10]; hi=[1.5,10,25]; onb=any(min(abs(f.x[i]-lo[i]),abs(f.x[i]-hi[i]))<0.01*(hi[i]-lo[i]) for i in range(3))
    tag = f"{lab}: f_d={f.x[0]:.3f} rho_s={10**f.x[1]:.3e} Msun/kpc3 r_s={f.x[2]:.2f} kpc on_bound={onb} chi2/dof={chi2/dof:.2f} (McMillan17 orig chi2/dof={c0/dof:.2f})"
    if lab == 'stat': tag += f" Q1 {'PASS' if chi2/dof < 2 else 'FAIL'}"
    tag += f" | v_c(8.178)={v[1]:.1f} (Horta pull {pull(v[1],235.3,2.8,3.7):+.2f}) dv/dR={dv:+.2f}" + (f" Q2 {'PASS' if dv < 0 else 'FAIL'}" if lab == 'stat' else '')
    tag += f" Omega={Om:.2f} ({pull(Om,28.5,0.4,0.1):+.1f}) kappa={kap:.2f} ({pull(kap,36.9,0.8,1.0):+.2f}) rho_DM_sun~{rho_sun:.3f} GeV/cm3"
    out.append(tag)
open('field_tests/results/c10_refit3.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
