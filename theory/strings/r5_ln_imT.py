"""R5 (locked PREREG_R5_ln_imT_tilt): R1 with tilt variable l = -ln(2y)."""
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
SI = CubicSpline(ph, [Irho(y) for y in ys]); lr = -math.log(2*yr); SL = CubicSpline(ph, [-math.log(2*y)-lr for y in ys]); dI = SI.derivative(); dL = SL.derivative()
P = lambda p: (lambda a: a*a/(a*a+1))(float(SI(p))); dP = lambda p: (lambda a, da: 2*a*da/(a*a+1)**2)(float(SI(p)), float(dI(p)))
def gs(k):
    V = lambda p: P(p)/(1 - k*float(SL(p)))
    dV = lambda p: dP(p)/(1 - k*float(SL(p))) + P(p)*k*float(dL(p))/(1 - k*float(SL(p)))**2
    return Model(V, dV, math.log(40)/s2)
pub = models.serapis_rho(6e-5); Ls = []
target = spectra3(pub, 49.49)['ns']; f = lambda k: spectra3(gs(k), 49.49)['ns'] - target
grid = [-0.2, -0.05, -0.01, -1e-3, 1e-3, 0.01, 0.05, 0.2]; vals = []
for k in grid:
    try: vals.append(f(k))
    except Exception as e: vals.append(float('nan'))
Ls.append("scan: " + ", ".join(f"k={k:g}: {v:+.3e}" for k, v in zip(grid, vals)))
ks = None
for (k1, v1), (k2, v2) in zip(zip(grid, vals), zip(grid[1:], vals[1:])):
    if v1 == v1 and v2 == v2 and v1*v2 < 0: ks = brentq(f, k1, k2, xtol=1e-12); break
if ks is None:
    Ls.append("NO kappa REPRODUCES n_s in [-0.2, 0.2] -> R5 FAILS")
else:
    g = gs(ks); ok = True
    for N in (46.09, 49.49, 55.0):
        a, b = spectra3(pub, N), spectra3(g, N); dn = abs(a['ns']-b['ns']); dr = abs(b['r']/a['r']-1); da = abs(b['alpha_s']-a['alpha_s'])
        ok &= dn <= 3e-4 and dr <= 0.02 and da <= 2e-5
        Ls.append(f"N*={N}: pub ns {a['ns']:.6f} r {a['r']:.4e} as {a['alpha_s']:.4e} | l-tilt ns {b['ns']:.6f} r {b['r']:.4e} as {b['alpha_s']:.4e} | dns {dn:.1e} dr/r {dr:.1e} das {da:.1e}")
    Ls.append(f"kappa* = {ks:.5e} (kappa*/eps = {ks/6e-5:.3f}) -> {'R5 SURVIVES' if ok else 'R5 FAILS'}")
open('field_tests/results/r5_ln_imT.txt', 'w').write('\n'.join(Ls)+'\n'); print('\n'.join(Ls))
