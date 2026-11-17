"""J6: multi-field delta-N for Janus (M_P reduced = 1). Validated: D999 (f_NL vs Vernizzi-Wands analytic to 0.6 %,
angle independence 1e-11, step convergence 1e-6) and D1000 (NLO r vs the single-field second-order calculator to 9e-5).
Sources: Vernizzi & Wands astro-ph/0603799 Eqs 11, 17, 28, 30; Byrnes & Wands astro-ph/0605679 Eqs 43-45, 81.
f_NL is returned as F = N_a N_b N_ab/(N_c N_c)^2 = (6/5) f_NL in the WMAP/Planck sign (= -(6/5) f_NL^(4) of VW).
Usage: observe_multi(V, grad, hess, phi_star) -> dict(N, ns, r_LO, r, fNL, Na, Nab)."""
import numpy as np
from tools.serapis_calc.multifield import run
C_BW = 2 - np.log(2) - 0.5772156649015329
def efolds(V, grad, f):
    f = np.array(f, float); s, Ne = run(V, grad, f, Nmax=400, v0=-np.array(grad(f))/V(f)); return Ne
def _derivs(V, grad, f, h):
    n = len(f); E = np.eye(n); N = lambda x: efolds(V, grad, x); N0 = N(f)
    Na = np.array([(N(f+h*E[a]) - N(f-h*E[a]))/(2*h) for a in range(n)]); Nab = np.zeros((n, n))
    for a in range(n):
        Nab[a, a] = (N(f+h*E[a]) - 2*N0 + N(f-h*E[a]))/h**2
        for b in range(a+1, n):
            Nab[a, b] = Nab[b, a] = (N(f+h*(E[a]+E[b])) - N(f+h*(E[a]-E[b])) - N(f-h*(E[a]-E[b])) + N(f-h*(E[a]+E[b])))/(4*h*h)
    return N0, Na, Nab
def observe_multi(V, grad, hess, phi_star, h=1e-3):
    f = np.array(phi_star, float); N0, Na, Nab = _derivs(V, grad, f, h); S = Na @ Na
    v = -np.array(grad(f))/V(f); eps = 0.5*v @ v; H2 = V(f)/(3-eps); Vab = np.array(hess(f))
    ns = 1 - 2*eps - 2/S + 2*(Na @ Vab @ Na)/(V(f)*S)
    sh = v/np.linalg.norm(v); M = np.eye(len(f))*(1 + (-2+2*C_BW)*eps) + 4*C_BW*eps*np.outer(sh, sh) - 2*C_BW*Vab/(3*H2)
    return dict(N=N0, ns=ns, r_LO=8/S, r=8*(1 + (-2+2*C_BW)*eps)/(Na @ M @ Na), fNL=(Na @ Nab @ Na)/S**2*5/6, F=(Na @ Nab @ Na)/S**2, Na=Na, Nab=Nab)
