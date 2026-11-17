"""JANUS-MF: exact multi-field Mukhanov–Sasaki (MultiModeCode equations, arXiv 1410.0685 Eqs. 3.11–3.23). M_P = 1, e-fold time, a = e^N.
spectra_mf(V, grad, hess, f0, Nstar, dlnk) -> dict(ns, r, PR(k*), lnk, lnPR). Validated: JMF2 (see field_tests)."""
import math, numpy as np
from scipy.integrate import solve_ivp
from tools.serapis_calc.multifield import run
def _bg(V, grad, f0):
    s, Ne = run(V, grad, np.array(f0, float), Nmax=500, v0=-np.array(grad(np.array(f0, float)))/V(np.array(f0, float)))
    n = len(f0)
    def st(N):
        u = s.sol(N); f, fp = u[:n], u[n:]; eps = 0.5*fp @ fp; H2 = V(f)/(3 - eps); return f, fp, eps, H2
    return st, Ne, n
def _mode(st, n, V, grad, hess, k, N0, Nend):
    f, fp, eps, H2 = st(N0); a = math.exp(N0); H = math.sqrt(H2)
    eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(k*eta))*np.exp(-1j*k*eta)/math.sqrt(2*k)
    du_deta = (-1j*k*(1 - 1j/(k*eta)) + 1j/(k*eta**2))*np.exp(-1j*k*eta)/math.sqrt(2*k); un = du_deta/(a*H)
    P0 = np.eye(n)*u; Pn0 = np.eye(n)*un; h0 = u/a; hn0 = un/a - u/a
    def rhs(N, y):
        f, fp, eps, H2 = st(N); a = math.exp(N); q2 = k*k/(a*a*H2)
        g = np.array(grad(f)); Cm = np.array(hess(f))/H2 + (np.outer(fp, g) + np.outer(g, fp))/H2 + (3 - eps)*np.outer(fp, fp)
        Y = y[:2*n*n].view(complex).reshape(n, n); Yn = y[2*n*n:4*n*n].view(complex).reshape(n, n); h, hn = y[4*n*n:4*n*n+2].view(complex)
        Ynn = -(1 - eps)*Yn - (q2 - 2 + eps)*Y - Cm @ Y; hnn = -(3 - eps)*hn - q2*h
        return np.concatenate([Yn.ravel().view(float), Ynn.ravel().view(float), np.array([hn, hnn]).view(float)])
    y0 = np.concatenate([P0.astype(complex).ravel().view(float), Pn0.astype(complex).ravel().view(float), np.array([h0, hn0], complex).view(float)])
    s = solve_ivp(rhs, [N0, Nend], y0, method='DOP853', rtol=1e-10, atol=1e-30)
    y = s.y[:, -1]; Y = y[:2*n*n].view(complex).reshape(n, n); h = y[4*n*n:4*n*n+2].view(complex)[0]
    f, fp, eps, H2 = st(Nend); a = math.exp(Nend); w = fp/np.linalg.norm(fp)
    Pdphi = k**3/(2*math.pi**2)*(Y @ Y.conj().T).real/a**2
    PR = float(w @ Pdphi @ w)/(fp @ fp); Ph = 8*k**3*abs(h)**2/(2*math.pi**2)
    return PR, Ph
def spectra_mf(V, grad, hess, f0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0, end_back=0.0):
    st, Ne, n = _bg(V, grad, f0); Np = Ne - Nstar
    f, fp, eps, H2 = st(Np); kp = math.exp(Np)*math.sqrt(H2)
    lks = np.linspace(-dlnk, dlnk, npts); PRs = []; Phs = []
    for d in lks:
        k = kp*math.exp(d)
        lo, hi = 0.0, Np                      # start where k/(aH) = bd
        for _ in range(80):
            mid = 0.5*(lo + hi); g = k/(math.exp(mid)*math.sqrt(st(mid)[3])) - bd
            lo, hi = (mid, hi) if g > 0 else (lo, mid)
        PR, Ph = _mode(st, n, V, grad, hess, k, lo, Ne - end_back); PRs.append(PR); Phs.append(Ph)
    lp = np.log(PRs); c = np.polyfit(lks, lp, 2); i0 = npts//2
    return dict(ns=1 + c[1], alpha_s=2*c[0], r=Phs[i0]/PRs[i0], PR=PRs[i0], lnk=lks, lnPR=lp, Ne=Ne)
