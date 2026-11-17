"""Fast route: one background integration (in e-folds N, canonical field phi, M_P = 1), then the Hubble-flow
parameters eps1 = phi'^2/2, eps2 = d ln eps1/dN, eps3 = d ln eps2/dN at horizon crossing of the pivot, and the
second-order slow-roll spectra (Stewart-Gong / Schwarz-Terrero-Escalante):
  n_s - 1 = -2 e1 - e2 - 2 e1^2 - (2C+3) e1 e2 - C e2 e3,   r = 16 e1 (1 + C e2),   alpha_s = -2 e1 e2 - e2 e3,
  C = gamma_E + ln 2 - 2.  Pivot convention as the base toolkit: horizon crossing N* e-folds before the end (eps1 = 1)."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
CE = 0.5772156649015329 + math.log(2) - 2
class Model:
    """V(phi) from a callable; dV from a callable or a finite difference. Background integrated once and cached."""
    def __init__(self, V, dV, phi0, Nmax=400.0):
        self.V, self.dV = V, dV
        def rhs(N, y):
            p, pn = y; eps = pn*pn/2
            return [pn, -(3-eps)*pn - (3-eps)*dV(p)/V(p)]
        ev = lambda N, y: y[1]**2/2 - 1.0; ev.terminal = True; ev.direction = 1
        p0 = -dV(phi0)/V(phi0)                       # slow-roll start
        s = solve_ivp(rhs, [0, Nmax], [phi0, p0], events=ev, rtol=1e-12, atol=1e-14, dense_output=True, method='DOP853')
        if not s.t_events[0].size:   # J1c: stiff fallback for singular ends (e.g. log potentials)
            s = solve_ivp(rhs, [0, Nmax], [phi0, p0], events=ev, rtol=1e-11, atol=1e-13, dense_output=True, method='Radau')
        if not s.t_events[0].size: raise ValueError('inflation does not end within Nmax')
        self.Nend = float(s.t_events[0][0]); self.sol = s
        # eps1 on a fine grid near the pivot region, smoothed by a spline in N for derivatives
        self._grid = None
    def flow(self, Nstar, h=0.25, npts=41):
        Np = self.Nend - Nstar
        Ns = np.linspace(Np - h*(npts//2)/10, Np + h*(npts//2)/10, npts)
        e1 = np.array([self.sol.sol(n)[1]**2/2 for n in Ns])
        l1 = CubicSpline(Ns, np.log(e1)); e2 = l1.derivative()(Ns)
        l2 = CubicSpline(Ns, np.log(np.abs(e2))); e3 = l2.derivative()(Ns)
        i = npts//2
        return e1[i], e2[i], e3[i]
    def spectra(self, Nstar):
        e1, e2, e3 = self.flow(Nstar)
        ns = 1 - 2*e1 - e2 - 2*e1*e1 - (2*CE+3)*e1*e2 - CE*e2*e3
        r = 16*e1*(1 + CE*e2)
        a = -2*e1*e2 - e2*e3
        return dict(ns=ns, r=r, alpha_s=a, eps=(e1, e2, e3))

def _ns_at(model, Nstar):
    e1, e2, e3 = model.flow(Nstar)
    return 1 - 2*e1 - e2 - 2*e1*e1 - (2*CE+3)*e1*e2 - CE*e2*e3, e1
def alpha_dn(model, Nstar, d=0.25):
    """alpha_s = dn_s/dln k by differentiating the second-order n_s along the background (dln k = (1-eps1) dN_pivot,
    N_pivot = N_end - N*): carries the next-order terms consistently without a third-order formula."""
    np_, e1 = _ns_at(model, Nstar - d); nm, _ = _ns_at(model, Nstar + d)
    return (np_ - nm)/(2*d)/(1 - e1)

# ---- J3: third order (Ballardini, Davoli & Sirletti 2024, arXiv:2408.05210, eqs. 47-52; alpha = 2 - ln2 - gamma_E = -CE) ----
AL = 2 - math.log(2) - 0.5772156649015329
def flow4(model, Nstar, h=0.25, npts=41):
    Np = model.Nend - Nstar
    Ns = np.linspace(Np - h*(npts//2)/10, Np + h*(npts//2)/10, npts)
    e1 = np.array([model.sol.sol(n)[1]**2/2 for n in Ns])
    l1 = CubicSpline(Ns, np.log(e1)); e2 = l1.derivative()(Ns)
    l2 = CubicSpline(Ns, np.log(np.abs(e2))); e3 = l2.derivative()(Ns)
    l3 = CubicSpline(Ns, np.log(np.abs(e3))); e4 = l3.derivative()(Ns)
    i = npts//2
    return e1[i], e2[i], e3[i], e4[i]
def spectra3(model, Nstar):
    e1, e2, e3, e4 = flow4(model, Nstar); a = AL; p2 = math.pi**2
    ns = 1 + (-2*e1 - e2 - 2*e1**2 - (3 - 2*a)*e1*e2 + a*e2*e3 - 2*e1**3 + (-15 + 6*a + p2)*e1**2*e2
              + (-84 + 36*a - 12*a*a + 7*p2)/12*e1*e2**2 + (-72 + 48*a - 12*a*a + 7*p2)/12*e1*e2*e3
              + (-8 + p2)/4*e2**2*e3 + (-a*a/2 + p2/24)*e2*e3**2 + (-a*a/2 + p2/24)*e2*e3*e4)
    als = (-2*e1*e2 - e2*e3 - 6*e1**2*e2 + (-3 + 2*a)*e1*e2**2 - 2*(2 - a)*e1*e2*e3 + a*e2*e3**2 + a*e2*e3*e4)
    bs = -2*e1*e2**2 - 2*e1*e2*e3 - e2*e3**2 - e2*e3*e4
    r = 16*e1*(1 + CE*e2)        # r kept at second order (third-order r not yet transcribed)
    return dict(ns=ns, r=r, alpha_s=als, beta_s=bs, eps=(e1, e2, e3, e4))
