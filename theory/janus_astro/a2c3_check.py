import math, sys, numpy as np
sys.path.insert(0, '.')
import lal, lalsimulation as ls
from scipy.optimize import brentq
from astropy.cosmology import Planck18 as AP
from tools.janus_astro import gw, gw_imr
from tools.janus_lt.background import Cosmo
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b); MPC = 1e6*lal.PC_SI; ok = {}
h = AP.H0.value/100
cos = Cosmo(AP.H0.value, AP.Ob0*h*h, AP.Odm0*h*h, Neff=AP.Neff, Tcmb=AP.Tcmb0.value, mnu=float(np.sum(AP.m_nu.value)))
DL = lambda z: (1 + z)*cos.DM(z)
def psd_callable(fn, flow):
    n = int(4096/0.25) + 1
    ser = lal.CreateREAL8FrequencySeries('psd', lal.LIGOTimeGPS(0), 0.0, 0.25, lal.DimensionlessUnit, n)
    fn(ser, flow); fr = np.arange(n)*0.25; S = ser.data.data.copy(); m = (fr >= flow) & (S > 0)
    lf, lS = np.log(fr[m]), np.log(S[m]); return lambda x: float(np.exp(np.interp(math.log(x), lf, lS)))
p175 = psd_callable(ls.SimNoisePSDaLIGO175MpcT1800545, 10.0)
s3 = gw_imr.snr_imr(1.4, 1.4, 0.0, 100*MPC, p175, 10.0); s12 = gw_imr.snr_imr(1.4, 1.4, 0.0, 100*MPC, p175, 10.0, n=12000)
ok['D1'] = rel(s3, 32.707) <= 5e-2; ok['D2'] = rel(s3, s12) <= 1e-3
P(f'D1 IMRPhenomD SNR(1.4+1.4, 100 Mpc, aLIGO175) = {s3:.4f} vs 0PN 32.707 rel={rel(s3,32.707):.1e}'); P(f'D2 n=3000 vs 12000: {s3:.6f} / {s12:.6f} rel={rel(s3,s12):.1e}')
P('VERDICTS:', ' '.join(f'{k}={"PASS" if v else "FAIL"}' for k, v in ok.items()), '-> A2c3', 'VALIDATED' if all(ok.values()) else 'NOT VALIDATED')
th = gw.theta_samples()
def horizon_range(m1, m2, psd, flo, zmax=100.0):
    rho = lambda z: gw_imr.snr_imr(m1, m2, z, DL(z)*MPC, psd, flo, n=1500)
    zh = brentq(lambda z: rho(z) - 8.0, 1e-4, zmax, xtol=1e-4) if rho(zmax) < 8 else float('inf')
    zz = np.geomspace(1e-4, min(zh, zmax), 100); pd = [1 - np.searchsorted(th, 32.0/max(rho(z), 1e-30))/th.size for z in zz]
    dV = np.array([4*math.pi*cos.DM(z)**2*cos.DH(z) for z in zz]); V = np.trapezoid(dV/(1 + zz)*np.array(pd), zz)
    return zh, (3*V/(4*math.pi))**(1/3)
res = {}
for name, flo in [('aLIGOAPlusDesignSensitivityT1800042', 10.0), ('EinsteinTelescopeP1600143', 5.0), ('CosmicExplorerP1600143', 5.0)]:
    ps = psd_callable(getattr(ls, 'SimNoisePSD' + name), flo)
    for (m1, m2) in [(1.4, 1.4), (30, 30)] + ([(50, 50)] if 'APlus' in name else []):
        zh, R = horizon_range(m1, m2, ps, flo); res[(name, m1)] = zh
        P(f'Reported {name} {m1}+{m2}: horizon z={zh:.3f}; range {R/1e3:.3f} Gpc')
fl = res[('CosmicExplorerP1600143', 30)] > res[('CosmicExplorerP1600143', 1.4)]
P('Flag test (D1063): CE BBH 30+30 horizon > BNS horizon:', fl, '->', 'RESOLVED (inspiral-only artefact)' if fl else 'OPEN')
open('field_tests/results/janus_astro_a2c3.txt', 'w').write('\n'.join(out) + '\n')
