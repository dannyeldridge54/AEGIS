# AEGIS-FP 4NZ4K2WWCLI3JC3T · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
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
def _mode(st, n, V, grad, hess, k, N0, Nend, Nref=0.0):
    f, fp, eps, H2 = st(N0); a = math.exp(N0 - Nref); H = math.sqrt(H2)
    eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(k*eta))*np.exp(-1j*k*eta)/math.sqrt(2*k)
    du_deta = (-1j*k*(1 - 1j/(k*eta)) + 1j/(k*eta**2))*np.exp(-1j*k*eta)/math.sqrt(2*k); un = du_deta/(a*H)
    P0 = np.eye(n)*u; Pn0 = np.eye(n)*un; h0 = u/a; hn0 = un/a - u/a
    def rhs(N, y):
        f, fp, eps, H2 = st(N); a = math.exp(N - Nref); q2 = k*k/(a*a*H2)
        g = np.array(grad(f)); Cm = np.array(hess(f))/H2 + (np.outer(fp, g) + np.outer(g, fp))/H2 + (3 - eps)*np.outer(fp, fp)
        Y = y[:2*n*n].view(complex).reshape(n, n); Yn = y[2*n*n:4*n*n].view(complex).reshape(n, n); h, hn = y[4*n*n:4*n*n+4].view(complex)
        Ynn = -(1 - eps)*Yn - (q2 - 2 + eps)*Y - Cm @ Y; hnn = -(3 - eps)*hn - q2*h
        return np.concatenate([Yn.ravel().view(float), Ynn.ravel().view(float), np.array([hn, hnn]).view(float)])
    y0 = np.concatenate([P0.astype(complex).ravel().view(float), Pn0.astype(complex).ravel().view(float), np.array([h0, hn0], complex).view(float)])
    s = solve_ivp(rhs, [N0, Nend], y0, method='DOP853', rtol=1e-10, atol=1e-30)
    y = s.y[:, -1]; Y = y[:2*n*n].view(complex).reshape(n, n); h = y[4*n*n:4*n*n+4].view(complex)[0]
    f, fp, eps, H2 = st(Nend); a = math.exp(Nend - Nref); w = fp/np.linalg.norm(fp)
    Pdphi = k**3/(2*math.pi**2)*(Y @ Y.conj().T).real/a**2
    PR = float(w @ Pdphi @ w)/(fp @ fp); Ph = 8*k**3*abs(h)**2/(2*math.pi**2)
    return PR, Ph
def spectra_mf(V, grad, hess, f0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0, end_back=0.0):
    st, Ne, n = _bg(V, grad, f0); Np = Ne - Nstar
    f, fp, eps, H2 = st(Np); kp = math.sqrt(H2)   # JMF13: a = e^(N - Np)
    lks = np.linspace(-dlnk, dlnk, npts); PRs = []; Phs = []
    for d in lks:
        k = kp*math.exp(d)
        lo, hi = 0.0, Np                      # start where k/(aH) = bd
        for _ in range(80):
            mid = 0.5*(lo + hi); g = k/(math.exp(mid - Np)*math.sqrt(st(mid)[3])) - bd
            lo, hi = (mid, hi) if g > 0 else (lo, mid)
        PR, Ph = _mode(st, n, V, grad, hess, k, lo, Ne - end_back, Np); PRs.append(PR); Phs.append(Ph)
    lp = np.log(PRs); c = np.polyfit(lks, lp, 2); i0 = npts//2
    return dict(ns=1 + c[1], alpha_s=2*c[0], r=Phs[i0]/PRs[i0], PR=PRs[i0], lnk=lks, lnPR=lp, Ne=Ne)
def spectra_mf_fast(V, grad, hess, f0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0, end_back=0.0):
    """Same equations and outputs as spectra_mf, but all k-modes integrated together in one vectorised ODE
    (common start where the LOWEST k has k/aH = bd, so every mode starts at k/aH >= bd). Equivalence vs spectra_mf: PREREG_JMF10_fast."""
    st, Ne, n = _bg(V, grad, f0); Np = Ne - Nstar
    f, fp, eps, H2 = st(Np); kp = math.sqrt(H2)   # JMF13: a = e^(N - Np)
    lks = np.linspace(-dlnk, dlnk, npts); ks = kp*np.exp(lks); K = len(ks)
    lo, hi = 0.0, Np
    for _ in range(80):
        mid = 0.5*(lo + hi); g = ks.min()/(math.exp(mid - Np)*math.sqrt(st(mid)[3])) - bd
        lo, hi = (mid, hi) if g > 0 else (lo, mid)
    N0 = lo; f, fp, eps, H2 = st(N0); a = math.exp(N0 - Np); H = math.sqrt(H2)
    eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(ks*eta))*np.exp(-1j*ks*eta)/np.sqrt(2*ks)
    du = (-1j*ks*(1 - 1j/(ks*eta)) + 1j/(ks*eta**2))*np.exp(-1j*ks*eta)/np.sqrt(2*ks); un = du/(a*H)
    I = np.eye(n); Y0 = np.einsum('k,ij->kij', u, I); Yn0 = np.einsum('k,ij->kij', un, I); h0 = u/a; hn0 = un/a - u/a
    k2 = ks*ks; sz = K*n*n
    def rhs(N, y):
        f, fp, eps, H2 = st(N); a = math.exp(N - Np); q2 = k2/(a*a*H2)
        g = np.array(grad(f)); Cm = np.array(hess(f))/H2 + (np.outer(fp, g) + np.outer(g, fp))/H2 + (3 - eps)*np.outer(fp, fp)
        yc = y.view(complex); Y = yc[:sz].reshape(K, n, n); Yn = yc[sz:2*sz].reshape(K, n, n); h = yc[2*sz:2*sz+K]; hn = yc[2*sz+K:]
        Ynn = -(1 - eps)*Yn - (q2 - 2 + eps)[:, None, None]*Y - np.einsum('ij,kjl->kil', Cm, Y); hnn = -(3 - eps)*hn - q2*h
        return np.concatenate([Yn.ravel(), Ynn.ravel(), hn, hnn]).view(float)
    y0 = np.concatenate([Y0.ravel(), Yn0.ravel(), h0, hn0]).astype(complex).view(float)
    s = solve_ivp(rhs, [N0, Ne - end_back], y0, method='DOP853', rtol=1e-10, atol=1e-30)
    yc = s.y[:, -1].view(complex); Y = yc[:sz].reshape(K, n, n); h = yc[2*sz:2*sz+K]
    f, fp, eps, H2 = st(Ne - end_back); a = math.exp(Ne - end_back - Np); w = fp/np.linalg.norm(fp)
    Pd = (ks**3/(2*math.pi**2))[:, None, None]*np.einsum('kij,klj->kil', Y, Y.conj()).real/a**2
    PRs = np.einsum('i,kij,j->k', w, Pd, w)/(fp @ fp); Phs = 8*ks**3*np.abs(h)**2/(2*math.pi**2)
    lp = np.log(PRs); c = np.polyfit(lks, lp, 2); i0 = npts//2
    return dict(ns=1 + c[1], alpha_s=2*c[0], r=Phs[i0]/PRs[i0], PR=PRs[i0], lnk=lks, lnPR=lp, Ne=Ne)
