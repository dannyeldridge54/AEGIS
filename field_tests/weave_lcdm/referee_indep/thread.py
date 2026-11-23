import numpy as np, math
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import zeta
A = 16*zeta(2)/(3*zeta(3)); BETA = 2*math.sqrt(2)
def evolve(VL, ui, Om, Or, ai=1e-3, n=400):
    phi0 = math.log(A/ui)/BETA
    V = lambda p: VL*(1 - A*math.exp(-BETA*p)); dV = lambda p: VL*A*BETA*math.exp(-BETA*p)
    def rhs(N, y):
        p, x = y; a = math.exp(N); rm = 3*Om/a**3; rr = 3*Or/a**4
        H2 = (rm + rr + V(p))/(3 - x*x/2); eps = (rm + 4*rr/3 + H2*x*x)/(2*H2)
        return [x, -(3 - eps)*x - dV(p)/H2]
    Ns = np.linspace(math.log(ai), 0, n)
    s = solve_ivp(rhs, (Ns[0], 0), [phi0, 0.0], t_eval=Ns, rtol=1e-10, atol=1e-12, method='LSODA')
    a = np.exp(s.t); p, x = s.y
    rm = 3*Om/a**3; rr = 3*Or/a**4; Vv = VL*(1 - A*np.exp(-BETA*p)); H2 = (rm + rr + Vv)/(3 - x*x/2)
    K = H2*x*x/2; w = (K - Vv)/(K + Vv)
    return a, w, H2[-1]
def wtable(ui, Om, Or):
    f = lambda VL: evolve(VL, ui, Om, Or, n=50)[2] - 1
    g = np.arange(0.5, 8.01, 0.25); v = [f(x) for x in g]
    i = next(k for k in range(len(g) - 1) if np.isfinite(v[k]) and np.isfinite(v[k+1]) and v[k]*v[k+1] < 0)
    VL = brentq(f, g[i], g[i+1], xtol=1e-12)
    a, w, _ = evolve(VL, ui, Om, Or); return a, w, VL
