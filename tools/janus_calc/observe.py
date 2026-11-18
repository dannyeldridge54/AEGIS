# AEGIS-FP UMDVPHUTQHKSIS37 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""One-call interface (J2 exact switch, J4 reheating -> observables, J5 error bars).
observe(model, TR=..., w=0.0) solves N* self-consistently from the reheating temperature with the matching equation
(Planck 2018 X form, as the AEGIS toolkit uses), V*/V_end taken from the exact background (end at eps_H = 1, D979),
then returns n_s, r, alpha_s, beta_s with truncation error bars; exact=True also runs the base Mukhanov-Sasaki solver."""
import math
from . import core
MP = 2.435e18; AS = 2.1e-9
def nstar_match(r, Vratio, TR, w=0.0, g=106.75, k=0.05, H0=67.4):
    lnk = math.log(k/(H0/299792.458)); Vs = 1.5*math.pi**2*AS*r*MP**4; rho_end = 1.5*Vs/Vratio
    rho_th = math.pi**2/30*g*TR**4; c = (1 - 3*w)/(12*(1 + w))
    return 67 - lnk + 0.25*math.log(Vs**2/(MP**4*rho_end)) + c*math.log(rho_th/rho_end) - (1/12)*math.log(g)
def observe(model, TR=None, Nstar=None, w=0.0, exact=False, tol=1e-4):
    Vend = model.V(model.sol.sol(model.Nend)[0])
    if Nstar is None:
        N = 50.0
        for _ in range(50):
            s = core.spectra3(model, N); Vs = model.V(model.sol.sol(model.Nend - N)[0])
            N2 = nstar_match(s['r'], Vs/Vend, TR, w)
            if abs(N2 - N) < tol: N = N2; break
            N = N2
        Nstar = N
    s3 = core.spectra3(model, Nstar); s2 = model.spectra(Nstar)
    out = dict(Nstar=Nstar, ns=s3['ns'], r=s3['r'], alpha_s=core.alpha_dn(model, Nstar), beta_s=s3['beta_s'],
               err=dict(ns=abs(s3['ns'] - s2['ns'])/5, r=abs(s3['r']*core.CE*s3['eps'][1]), alpha_s=abs(core.alpha_dn(model, Nstar) - s3['alpha_s'])))
    if exact:
        from tools.serapis_calc.ms import Background, spectra
        import numpy as np
        bg = Background(model.V, model.dV, model.sol.y[0][0]); W = tuple(np.round(np.linspace(-0.8, 0.8, 9), 10))
        e = spectra(bg, Nstar, dlnk=W, bd=1000.0, ic='ds'); out['exact'] = e
        out['gap'] = dict(ns=out['ns'] - e['ns'], r=out['r']/e['r'] - 1, alpha_s=out['alpha_s']/e['alpha_s'] - 1)
    return out
