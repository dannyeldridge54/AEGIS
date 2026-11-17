import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from scipy.optimize import brentq
from scipy.integrate import quad
from astropy.cosmology import Planck18 as AP
from tools.janus_astro import gw
from tools.janus_lt.background import Cosmo
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b); MPC = 1e6*lal.PC_SI; MS = lal.MSUN_SI; ok = {}
h = AP.H0.value/100
cos = Cosmo(AP.H0.value, AP.Ob0*h*h, AP.Odm0*h*h, Neff=AP.Neff, Tcmb=AP.Tcmb0.value, mnu=float(np.sum(AP.m_nu.value)))
DL = lambda z: (1 + z)*cos.DM(z)
o = True
for z in [0.1, 1, 3, 10]:
    a, b = DL(z), AP.luminosity_distance(z).value; e = rel(a, b); o &= e <= 1e-4; P(f'C1 z={z}: D_L ours={a:.4f} astropy={b:.4f} Mpc rel={e:.1e}')
ok['C1'] = o
th = gw.theta_samples(); fc = np.mean((th/4)**3)**(1/3); ok['C2'] = rel(fc, 1/2.2648) <= 3e-3
P(f'C2 <(Theta/4)^3>^(1/3) = {fc:.5f} vs 1/2.2648 = {1/2.2648:.5f} rel={rel(fc,1/2.2648):.1e}')
def psd_callable(fn, flow):
    n = int(4096/0.25) + 1
    ser = lal.CreateREAL8FrequencySeries('psd', lal.LIGOTimeGPS(0), 0.0, 0.25, lal.DimensionlessUnit, n)
    fn(ser, flow); fr = np.arange(n)*0.25; S = ser.data.data.copy(); m = (fr >= flow) & (S > 0)
    lf, lS = np.log(fr[m]), np.log(S[m]); return lambda x: float(np.exp(np.interp(math.log(x), lf, lS)))
def cosmo_range(m1, m2, psd, flo, zmax=200.0):
    rho = lambda z: gw.snr_opt_z(m1*MS, m2*MS, z, DL(z)*MPC, psd, flo, 3000)
    zh = brentq(lambda z: rho(z) - 8.0, 1e-4, zmax, xtol=1e-6) if rho(zmax) < 8 else float('inf')
    zz = np.geomspace(1e-4, zh, 160); pd = []
    for z in zz:
        r = rho(z); thr = 4*8.0/r if r > 0 else 1e9
        pd.append(1 - np.searchsorted(th, thr)/th.size)
    dVdz = np.array([4*math.pi*cos.DM(z)**2*cos.DH(z) for z in zz])
    Veff = np.trapezoid(dVdz/(1 + zz)*np.array(pd), zz)
    return zh, DL(zh), (3*Veff/(4*math.pi))**(1/3)
psd = psd_callable(ls.SimNoisePSDaLIGO175MpcT1800545, 10.0)
zh, dh, R = cosmo_range(1.4, 1.4, psd, 10.0); ok['C3'] = rel(R, 180.5) <= 5e-2
P(f'C3 aLIGO175 BNS: z_h={zh:.4f} (D_L {dh:.1f} Mpc), cosmological range={R:.1f} Mpc vs Euclidean 180.5 rel={rel(R,180.5):.1e}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A2c2', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
for name, flo in [('aLIGOAPlusDesignSensitivityT1800042', 10.0), ('EinsteinTelescopeP1600143', 5.0), ('CosmicExplorerP1600143', 5.0)]:
    ps = psd_callable(getattr(ls, 'SimNoisePSD' + name), flo)
    for (m1, m2, lab) in [(1.4, 1.4, 'BNS'), (30, 30, 'BBH inspiral-only')]:
        zh, dh, R = cosmo_range(m1, m2, ps, flo)
        P(f'Reported {name} {lab}: horizon z={zh:.3f} (D_L {dh/1e3:.2f} Gpc); range {R/1e3:.3f} Gpc (comoving-volume equivalent)')
open('field_tests/results/janus_astro_a2c2.txt', 'w').write('\n'.join(out) + '\n')
