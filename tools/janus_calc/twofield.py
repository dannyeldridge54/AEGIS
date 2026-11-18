# AEGIS-FP QPIX5QHUXXP3R756 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J6: multi-field delta-N for Janus (M_P reduced = 1). Validated: D999 (f_NL vs Vernizzi-Wands analytic to 0.6 %,
angle independence 1e-11, step convergence 1e-6) and D1000 (NLO r vs the single-field second-order calculator to 9e-5).
Sources: Vernizzi & Wands astro-ph/0603799 Eqs 11, 17, 28, 30; Byrnes & Wands astro-ph/0605679 Eqs 43-45, 81.
f_NL is returned as F = N_a N_b N_ab/(N_c N_c)^2 = (6/5) f_NL in the WMAP/Planck sign (= -(6/5) f_NL^(4) of VW).
Large f_NL checked in D1001 (Byrnes-Choi-Hall Example A, |f_NL| up to 81, 0.4-6 %).
Usage: observe_multi(V, grad, hess, phi_star, h=1e-3 or per-field list, rho_c=None) -> dict(N, ns, r_LO, r, fNL, F, Na, Nab)."""
import numpy as np
from tools.serapis_calc.multifield import run
C_BW = 2 - np.log(2) - 0.5772156649015329
from scipy.integrate import solve_ivp
def efolds(V, grad, f, rho_c=None):
    """e-folds from f (slow-roll start velocity) to eps_H = 1, or to the uniform-density slice rho = 3H^2 = rho_c (D1001)."""
    f = np.array(f, float)
    if rho_c is None:
        s, Ne = run(V, grad, f, Nmax=400, v0=-np.array(grad(f))/V(f)); return Ne
    n = len(f)
    def rhs(N, u):
        x, xn = u[:n], u[n:]; e = 0.5*xn @ xn
        return np.concatenate([xn, -(3-e)*xn - (3-e)*np.array(grad(x))/V(x)])
    ev = lambda N, u: 3*V(u[:n])/(3 - 0.5*u[n:] @ u[n:]) - rho_c; ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, [0, 400], np.concatenate([f, -np.array(grad(f))/V(f)]), events=ev, rtol=1.00001950951e-11, atol=1.00008447547e-13)
    return s.t_events[0][0]
def _derivs(V, grad, f, h, rho_c=None):
    n = len(f); E = np.diag(np.broadcast_to(np.asarray(h, float), (n,))); N = lambda x: efolds(V, grad, x, rho_c); N0 = N(f)
    hs = np.diag(E)
    Na = np.array([(N(f+E[a]) - N(f-E[a]))/(2*hs[a]) for a in range(n)]); Nab = np.zeros((n, n))
    for a in range(n):
        Nab[a, a] = (N(f+E[a]) - 2*N0 + N(f-E[a]))/hs[a]**2
        for b in range(a+1, n):
            Nab[a, b] = Nab[b, a] = (N(f+E[a]+E[b]) - N(f+E[a]-E[b]) - N(f-E[a]+E[b]) + N(f-E[a]-E[b]))/(4*hs[a]*hs[b])
    return N0, Na, Nab
def observe_multi(V, grad, hess, phi_star, h=1e-3, rho_c=None):
    """h: scalar or per-field steps (use ~phi_a/10 for a field near zero). rho_c: end on a uniform-density slice."""
    f = np.array(phi_star, float); N0, Na, Nab = _derivs(V, grad, f, h, rho_c); S = Na @ Na
    v = -np.array(grad(f))/V(f); eps = 0.5*v @ v; H2 = V(f)/(3-eps); Vab = np.array(hess(f))
    ns = 1 - 2*eps - 2/S + 2*(Na @ Vab @ Na)/(V(f)*S)
    sh = v/np.linalg.norm(v); M = np.eye(len(f))*(1 + (-2+2*C_BW)*eps) + 4*C_BW*eps*np.outer(sh, sh) - 2*C_BW*Vab/(3*H2)
    return dict(N=N0, ns=ns, r_LO=8/S, r=8*(1 + (-2+2*C_BW)*eps)/(Na @ M @ Na), fNL=(Na @ Nab @ Na)/S**2*5/6, F=(Na @ Nab @ Na)/S**2, Na=Na, Nab=Nab)
