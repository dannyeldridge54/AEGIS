import sys, time; sys.path.insert(0, '.')
import sympy as sp, numpy as np
from tools.serapis_calc import ms_jit
from tools.serapis_calc.ms_jit import build, spectra_msjit
y = sp.Symbol('y'); m = build((1 - sp.exp(-sp.sqrt(sp.Rational(2, 3))*y))**2, y)
for tag, dl in (('0.1', (-0.1, -0.05, 0, 0.05, 0.1)), ('0.05', (-0.05, -0.025, 0, 0.025, 0.05)), ('0.025', (-0.025, -0.0125, 0, 0.0125, 0.025))):
    s = spectra_msjit(m, 7.0, 55.0, dlnk=dl); print('Starobinsky', tag, f"n_s {s['ns']:.7f} α_s {s['alpha_s']:.5e}", flush=True)
import tools.serapis_calc.pipeline as P
orig = P.build
def b16(model='serapis_e', C=1.15e-6, lam=1.0, ymax=3000, npts=4000): return orig(model, C, lam, ymax, 16000)
P.build = b16
m2, p0 = ms_jit.build_spline('serapis_e', 1.0e-6)
for tag, dl in (('0.1', (-0.1, -0.05, 0, 0.05, 0.1)), ('0.05', (-0.05, -0.025, 0, 0.025, 0.05)), ('0.025', (-0.025, -0.0125, 0, 0.0125, 0.025))):
    s = spectra_msjit(m2, p0, 50.7, dlnk=dl); print('SERAPIS-E npts 16000', tag, f"n_s {s['ns']:.7f} α_s {s['alpha_s']:.5e}", flush=True)
