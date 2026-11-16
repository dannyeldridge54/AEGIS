"""Level 3b: background for several canonical fields (flat field space), e-fold time; ends at eps_H = 1."""
import numpy as np
from scipy.integrate import solve_ivp
def run(V, grad, f0, Nmax=500, v0=None):
    n = len(f0)
    def rhs(N, u):
        f, fn = u[:n], u[n:]; eps = 0.5*np.dot(fn, fn)
        return np.concatenate([fn, -(3-eps)*fn - (3-eps)*np.array(grad(f))/V(f)])
    ev = lambda N, u: 0.5*np.dot(u[n:], u[n:]) - 1; ev.terminal = True; ev.direction = 1
    u0 = np.concatenate([f0, np.zeros(n) if v0 is None else v0])
    s = solve_ivp(rhs, [0, Nmax], u0, events=ev, rtol=1e-11, atol=1e-13, dense_output=True)
    return s, (s.t_events[0][0] if len(s.t_events[0]) else None)
