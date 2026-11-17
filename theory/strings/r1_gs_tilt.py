"""R1 (locked PREREG_R1_green_schwarz_tilt)."""
import sys, math, numpy as np; sys.path.insert(0, '.')
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from tools.janus_calc import models
from tools.janus_calc.core import Model, spectra3
from tools.serapis_calc.modular import j as jfun
s2 = math.sqrt(2); yr = math.sqrt(3)/2
L = lambda y: -(math.log(2*y) + 4*math.log(models._eta_abs(0.5, y)))
def Irho(y):
    a = float(abs(jfun(complex(0.5, y))))
    return math.log1p((a/1728)**2)/(4*math.pi) if a < 1e150 else 2*(math.log(a)-math.log(1728))/(4*math.pi)
Lr = L(yr); ph = np.linspace(math.log(yr)/s2+1e-5, math.log(60)/s2, 3000); ys = np.exp(s2*ph)
SI = CubicSpline(ph, [Irho(y) for y in ys]); SL = CubicSpline(ph, [L(y)-Lr for y in ys]); dI = SI.derivative(); dL = SL.derivative()
P = lambda p: (lambda a: a*a/(a*a+1))(float(SI(p))); dP = lambda p: (lambda a, da: 2*a*da/(a*a+1)**2)(float(SI(p)), float(dI(p)))
def gs(k):
    V = lambda p: P(p)/(1 - k*float(SL(p)))
    dV = lambda p: dP(p)/(1 - k*float(SL(p))) + P(p)*k*float(dL(p))/(1 - k*float(SL(p)))**2
    return Model(V, dV, math.log(40)/s2)
pub = models.serapis_rho(6e-5); g = gs(6e-5); Ls = []; ok = True
for N in (46.09, 49.49, 55.0):
    a, b = spectra3(pub, N), spectra3(g, N); d = abs(a['ns'] - b['ns']); ok &= d <= 3e-4
    Ls.append(f"N*={N}: pub ns {a['ns']:.6f} r {a['r']:.4e} as {a['alpha_s']:.4e} | GS(k=6e-5) ns {b['ns']:.6f} r {b['r']:.4e} as {b['alpha_s']:.4e} | dns {d:.1e} dr/r {abs(b['r']/a['r']-1):.1e} das {abs(b['alpha_s']-a['alpha_s']):.1e}")
target = spectra3(pub, 49.49)['ns']
ks = brentq(lambda k: spectra3(gs(k), 49.49)['ns'] - target, 1e-6, 3e-4, xtol=1e-10)
Ls.append(f"T2: kappa* = {ks:.4e} (kappa*/eps = {ks/6e-5:.4f})")
Ls.append(f"T1 {'PASS' if ok else 'FAIL'} -> {'GS FORM EQUIVALENT (at e^K level)' if ok else 'NOT EQUIVALENT'}")
open('field_tests/results/r1_gs_tilt.txt', 'w').write('\n'.join(Ls)+'\n'); print('\n'.join(Ls))
