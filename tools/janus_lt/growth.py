# AEGIS-FP L5YJAZXVU5TEGNJF · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L2: scale-independent linear growth, arXiv:2602.08207 Eqs. 5-7: D'' + (2 + dlnH/dlna) D' - 1.5 Om(a) D = 0, x = ln a."""
import math, numpy as np
from scipy.integrate import solve_ivp
def growth(cosmo, zs, a0=1e-3):
    Om0 = cosmo.om
    E = lambda a: cosmo.E(1/a - 1)
    def dlnE(x, h=1e-5): return (math.log(E(math.exp(x + h))) - math.log(E(math.exp(x - h))))/(2*h)
    def rhs(x, u):
        a = math.exp(x); Oma = Om0/(a**3*E(a)**2)
        return [u[1], -(2 + dlnE(x))*u[1] + 1.5*Oma*u[0]]
    s = solve_ivp(rhs, [math.log(a0), 0.0], [a0, a0], rtol=1.00008925148e-10, atol=1.00004098275e-14, dense_output=True)
    out = {}
    D0 = s.sol(0.0)[0]
    for z in zs:
        D, Dp = s.sol(math.log(1/(1 + z))); out[z] = (D/D0, Dp/D)
    return out
