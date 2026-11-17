import sys, math, numpy as np; sys.path.insert(0, '.')
import lal, lalsimulation as ls
from scipy.optimize import minimize_scalar
from tools.janus_astro import gw, const as K
def psd_arr(fn, flow):
    n = int(4096/0.25) + 1; ser = lal.CreateREAL8FrequencySeries('psd', lal.LIGOTimeGPS(0), 0.0, 0.25, lal.DimensionlessUnit, n)
    fn(ser, flow); fr = np.arange(n)*0.25; S = ser.data.data.copy(); m = (fr >= flow) & (S > 0)
    return lambda x: np.exp(np.interp(np.log(x), np.log(fr[m]), np.log(S[m])))
MS = 1.98840987e30; M1 = M2 = 1.4*MS; MPC = 3.0856775814913673e22
fisco = K.c**3/(6**1.5*math.pi*K.G*(M1+M2)); f = np.geomspace(20, fisco, 40000)
Mc = gw.chirp_mass(M1, M2)
dpsi = gw.taylorf2_tidal_dphase(f, M1, M2, 295.6, 295.6, 6) - gw.taylorf2_tidal_dphase(f, M1, M2, 247.6, 247.6, 6)
out = []
for pname, fn in (('O4-like aLIGO140Mpc', ls.SimNoisePSDaLIGO140MpcT1800545), ('A+ design', ls.SimNoisePSDaLIGOAPlusDesignSensitivityT1800042)):
    S = psd_arr(fn, 10.0)(f)
    for D in (40, 100):
        w = gw.amplitude0(f, Mc, D*MPC)**2/S; norm = np.trapezoid(w, f); rho = math.sqrt(4*norm)
        ov = lambda t: -abs(np.trapezoid(w*np.exp(1j*(dpsi + 2*math.pi*f*t)), f))/norm
        r = minimize_scalar(ov, bounds=(-0.01, 0.01), method='bounded', options={'xatol': 1e-9}); O = -r.fun
        c = 2*(1 - O)*rho**2
        out.append(f"{pname} D={D} Mpc: SNR={rho:.1f} 1-O={1-O:.2e} 2(1-O)rho^2={c:.2f} -> {'DISTINGUISHABLE' if c > 1 else 'NOT'}; rho needed {math.sqrt(1/(2*(1-O))):.0f}")
open('field_tests/results/c5_eos_forecast.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
