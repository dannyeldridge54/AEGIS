# AEGIS-FP JQFP2DEWEHISOAGB · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""SERAPIS branch potentials for the Janus calculator (same physics as the paper; built here from the modular
functions of tools/serapis_calc, which are definitions, not solvers)."""
import math, numpy as np, mpmath as mp
from scipy.interpolate import CubicSpline
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.modular import I_inv, j as jfun
from .core import Model
s2 = math.sqrt(2)
def serapis_E(C):
    ph = np.linspace(np.log(RHO_Y)/s2+1e-4, np.log(3000)/s2, 4000)
    Eg = np.maximum(2*1.0823232337111382*np.array([Ehat(np.exp(s2*p)) for p in ph]), 1e-14)
    S = CubicSpline(ph, Eg); dS = S.derivative()
    V = lambda p: (lambda e: e/(e+1)*(1+C*e))(float(S(p)))
    dV = lambda p: (lambda e, de: de*((1+C*e)/(e+1)**2 + C*e/(e+1)))(float(S(p)), float(dS(p)))
    return Model(V, dV, ph[np.searchsorted(Eg, 600)])
def chronos(eps, y0=45.0):
    ph2 = np.linspace(1e-4, math.log(60)/s2, 3000); ys = np.exp(s2*ph2)
    S2 = CubicSpline(ph2, [I_inv(1j*y, 2) for y in ys]); S1 = CubicSpline(ph2, [I_inv(1j*y, 1) for y in ys]); d2 = S2.derivative(); d1 = S1.derivative()
    V = lambda p: (lambda a: a*a/(a*a+1))(float(S2(p))) + eps*float(S1(p))
    dV = lambda p: (lambda a, da: 2*a*da/(a*a+1)**2)(float(S2(p)), float(d2(p))) + eps*float(d1(p))
    return Model(V, dV, math.log(y0)/s2)
def _eta_abs(x, y, nmax=80):
    q = mp.e**(2j*mp.pi*mp.mpc(x, y)); e = mp.e**(2j*mp.pi*mp.mpc(x, y)/24)
    for n in range(1, nmax+1): e *= (1-q**n)
    return float(abs(e))
def serapis_rho(eps=6e-5):
    yr = math.sqrt(3)/2
    L = lambda y: -(math.log(2*y) + 4*math.log(_eta_abs(0.5, y)))
    def Irho(y):
        a = float(abs(jfun(complex(0.5, y))))
        return math.log1p((a/1728)**2)/(4*math.pi) if a < 1e150 else 2*(math.log(a)-math.log(1728))/(4*math.pi)
    Lr = L(yr); ph = np.linspace(math.log(yr)/s2+1e-5, math.log(60)/s2, 3000); ys = np.exp(s2*ph)
    SI = CubicSpline(ph, [Irho(y) for y in ys]); SL = CubicSpline(ph, [L(y)-Lr for y in ys]); dI = SI.derivative(); dL = SL.derivative()
    V = lambda p: (lambda a: a*a/(a*a+1))(float(SI(p))) + eps*float(SL(p))
    dV = lambda p: (lambda a, da: 2*a*da/(a*a+1)**2)(float(SI(p)), float(dI(p))) + eps*float(dL(p))
    return Model(V, dV, math.log(40)/s2)
