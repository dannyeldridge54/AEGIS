# AEGIS-FP HVOLCJGPZV6GQ6NZ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Exact single-field MS reference, compiled (numba): spectra_fast's equations (R and h modes, e-fold time) with background + all k in one
compiled real ODE, adaptive Dormand–Prince 5(4). Potential from a sympy expression in one symbol. Equivalence vs ms.spectra_fast: PREREG_MSJ1."""
import math, numpy as np, sympy as sp, numba as nb
from tools.janus_calc.mf_jit import A, B5, B4, CC
def build(Vexpr, y):
    x = sp.Symbol('x'); e = Vexpr.subs(y, x); ns = {'math': math}
    exec(f"def _V(x):\n    return {sp.pycode(e)}\ndef _dV(x):\n    return {sp.pycode(sp.diff(e, x))}\n", ns)
    return _make(nb.njit(ns['_V']), nb.njit(ns['_dV']))
def build_spline(model='serapis_e', C=1.15e-6, lam=1.0):
    """U1: the pipeline's SERAPIS-E potential (cubic spline of E(tau,2) - E(rho,2), V = e/(e+1)(1 + C e/lam)) with ANALYTIC spline dV, compiled.
    Returns (m, phi0) for spectra_msjit."""
    from tools.serapis_calc.pipeline import build as pbuild
    from scipy.interpolate import CubicSpline
    import inspect
    m0, V0, dV0, p0 = pbuild(model, C, lam)
    S = V0.__closure__ and [c.cell_contents for c in V0.__closure__ if isinstance(c.cell_contents, CubicSpline)][0]
    xk = np.ascontiguousarray(S.x); cf = np.ascontiguousarray(S.c); n = xk.size - 1; Cc = float(C); L = float(lam)
    @nb.njit
    def _ee(p):
        i = np.searchsorted(xk, p) - 1
        if i < 0: i = 0
        if i > n - 1: i = n - 1
        t = p - xk[i]; e = ((cf[0, i]*t + cf[1, i])*t + cf[2, i])*t + cf[3, i]; de = (3*cf[0, i]*t + 2*cf[1, i])*t + cf[2, i]
        return e, de
    @nb.njit
    def V(p):
        e, de = _ee(p); return e/(e + 1)*(1 + Cc*e/L)
    @nb.njit
    def dV(p):
        e, de = _ee(p); return de*((1 + Cc*e/L)/(e + 1)**2 + (Cc/L)*e/(e + 1))
    return _make(V, dV), p0
def _make(V, dV):
    @nb.njit
    def rhs(N, yv, ks, Np, K, out):
        p = yv[0]; pn = yv[1]; eps = 0.5*pn*pn; v = V(p); H = math.sqrt(v/(3 - eps))
        pnn = -(3 - eps)*pn - (3 - eps)*dV(p)/v; out[0] = pn; out[1] = pnn
        if K == 0: return
        aH = math.exp(N - Np)*H; fr = 3 - eps + 2*pnn/pn
        for k in range(K):
            q2 = (ks[k]/aH)**2; b = 2 + 8*k
            out[b] = yv[b+2]; out[b+1] = yv[b+3]; out[b+2] = -fr*yv[b+2] - q2*yv[b]; out[b+3] = -fr*yv[b+3] - q2*yv[b+1]
            out[b+4] = yv[b+6]; out[b+5] = yv[b+7]; out[b+6] = -(3 - eps)*yv[b+6] - q2*yv[b+4]; out[b+7] = -(3 - eps)*yv[b+7] - q2*yv[b+5]
    @nb.njit
    def integ(N0, N1, y0, ks, Np, K, rtol, atol, stop_eps):
        yv = y0.copy(); d = yv.size; kk = np.zeros((7, d)); tmp = np.zeros(d); yt = np.zeros(d); N = N0; h = 1e-3
        while N < N1:
            if N + h > N1: h = N1 - N
            rhs(N, yv, ks, Np, K, kk[0])
            for st in range(1, 7):
                for q in range(d):
                    s = 0.0
                    for r in range(st): s += A[st, r]*kk[r, q]
                    tmp[q] = yv[q] + h*s
                rhs(N + CC[st]*h, tmp, ks, Np, K, kk[st])
            err = 0.0
            for q in range(d):
                y5 = yv[q]; e = 0.0
                for r in range(7): y5 += h*B5[r]*kk[r, q]; e += h*(B5[r] - B4[r])*kk[r, q]
                tmp[q] = y5; sc = atol + rtol*max(abs(yv[q]), abs(y5)); e = e/sc; err += e*e
            err = math.sqrt(err/d)
            if err <= 1.0:
                if stop_eps and 0.5*tmp[1]*tmp[1] >= 1.0:
                    lo = 0.0; hi = h
                    for it in range(60):
                        mid = 0.5*(lo + hi); rhs(N, yv, ks, Np, K, kk[0])
                        for st in range(1, 7):
                            for q in range(d):
                                s = 0.0
                                for r in range(st): s += A[st, r]*kk[r, q]
                                tmp[q] = yv[q] + mid*s
                            rhs(N + CC[st]*mid, tmp, ks, Np, K, kk[st])
                        for q in range(d):
                            s = yv[q]
                            for r in range(7): s += mid*B5[r]*kk[r, q]
                            yt[q] = s
                        if 0.5*yt[1]*yt[1] >= 1.0: hi = mid
                        else: lo = mid
                    return N + hi, yt
                N += h; yv[:] = tmp
            fac = 0.9*err**-0.2 if err > 0 else 5.0
            h = h*min(5.0, max(0.2, fac))
        return N, yv
    return dict(V=V, dV=dV, integ=integ)
def spectra_msjit(m, phi0, Nstar, dlnk=(-0.1, -0.05, 0.0, 0.05, 0.1), bd=200.0, rtol=1.00009208787e-12, Nmax=4000.0):
    V, dV, integ = m['V'], m['dV'], m['integ']; E = np.zeros(1); y0 = np.array([phi0, -dV(phi0)/V(phi0)])
    Nend, _ = integ(0.0, Nmax, y0, E, 0.0, 0, 1e-12, 1e-14, True); Np = Nend - Nstar
    def bg(N): return y0 if N <= 0 else integ(0.0, N, y0, E, 0.0, 0, 1e-12, 1e-14, False)[1]
    def H(yb): return math.sqrt(V(yb[0])/(3 - 0.5*yb[1]**2))
    ks = H(bg(Np))*np.exp(np.array(dlnk)); kmin = ks.min(); lo, hi = 0.0, Np
    for _ in range(80):
        mid = 0.5*(lo + hi)
        if kmin/(math.exp(mid - Np)*H(bg(mid))) - bd > 0: lo = mid
        else: hi = mid
    N0 = lo; yb = bg(N0); p, pn = yb; eps = 0.5*pn*pn; Hh = H(yb); a = math.exp(N0 - Np)
    pnn = -(3 - eps)*pn - (3 - eps)*dV(p)/V(p); z = a*pn; zn = z*(1 + pnn/pn); eta = -1.0/(a*Hh*(1 - eps))
    u = (1 - 1j/(ks*eta))/np.sqrt(2*ks); un = ((-1j*ks*(1 - 1j/(ks*eta)) + 1j/(ks*eta**2))/np.sqrt(2*ks))/(a*Hh)
    R = u/z; Rn = un/z - u*zn/z**2; hh = u/a; hn = un/a - u/a; K = len(ks)
    Y = np.zeros(2 + 8*K); Y[:2] = yb
    for k in range(K): Y[2+8*k:10+8*k] = [R[k].real, R[k].imag, Rn[k].real, Rn[k].imag, hh[k].real, hh[k].imag, hn[k].real, hn[k].imag]
    Nf = min(Np + 12 + max(dlnk), Nend - 0.5)
    _, Yf = integ(N0, Nf, Y, ks, Np, K, rtol, 1e-30, False); Yk = Yf[2:].reshape(K, 8)
    PR = ks**3*(Yk[:, 0]**2 + Yk[:, 1]**2)/(2*np.pi**2); Pt = 8*ks**3*(Yk[:, 4]**2 + Yk[:, 5]**2)/(2*np.pi**2)
    d = np.array(dlnk); lp = np.log(PR); deg = min(4, len(d) - 1); c = np.polyfit(d, lp, deg); c = c[-3:] if deg >= 2 else np.concatenate([[0.0], c])
    i0 = list(d).index(0.0); return dict(ns=1 + c[1], alpha_s=2*c[0], r=Pt[i0]/PR[i0], PR=PR[i0], Nend=Nend)
