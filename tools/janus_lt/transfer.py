# AEGIS-FP 4B4XTVRK4TSHXWBQ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Eisenstein & Hu 1998 no-wiggle transfer function (astro-ph/9709112 Eqs. 26, 28-31). Validated: L9a."""
import numpy as np
def T_nowiggle(k_hMpc, h, ob, oc, Tcmb=2.7255):
    """k in h/Mpc; ob, oc are omega_b h^2, omega_c h^2. Returns T0(k)."""
    O0 = (ob + oc)/h**2; fb = ob/(ob + oc); th = Tcmb/2.7; om = ob + oc
    s = 44.5*np.log(9.83/om)/np.sqrt(1 + 10*ob**0.75)
    aG = 1 - 0.328*np.log(431*om)*fb + 0.38*np.log(22.3*om)*fb**2
    k = np.asarray(k_hMpc, float)*h   # 1/Mpc
    G = O0*h*(aG + (1 - aG)/(1 + (0.43*k*s)**4))
    q = np.asarray(k_hMpc, float)*th**2/G
    L0 = np.log(2*np.e + 1.8*q); C0 = 14.2 + 731/(1 + 62.5*q)
    return L0/(L0 + C0*q*q)
