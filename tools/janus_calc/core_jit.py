# AEGIS-FP 7ZBQGE7RELVTOWD3 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus single-field fast face, compiled: core.Model + core.spectra3 with the background integrated by a compiled Dormand–Prince 5(4)
(rtol 1e-12, atol 1e-14, as core.Model's DOP853), ε1 = 1 end found by bisection inside the compiled step, and ε-flow parameters from the
same 41-point CubicSpline construction as core.flow4. Potential from a sympy expression. Equivalence vs core: PREREG_JSJ1."""
import math, numpy as np, sympy as sp, numba as nb
from scipy.interpolate import CubicSpline
from tools.janus_calc.mf_jit import A, B5, B4, CC
from tools.janus_calc.core import AL, CE
def build(Vexpr, y, rtol=1e-12, atol=1e-14):
    x = sp.Symbol('x'); e = Vexpr.subs(y, x); ns = {'math': math}
    exec(f"def _V(x):\n    return {sp.pycode(e)}\ndef _dV(x):\n    return {sp.pycode(sp.diff(e, x))}\n", ns)
    V = nb.njit(ns['_V']); dV = nb.njit(ns['_dV'])
    @nb.njit
    def f(y, out):
        p = y[0]; pn = y[1]; eps = 0.5*pn*pn; out[0] = pn; out[1] = -(3 - eps)*pn - (3 - eps)*dV(p)/V(p)
    @nb.njit
    def step(N, y, h, ks, tmp):
        f(y, ks[0])
        for st in range(1, 7):
            for q in range(2):
                s = 0.0
                for r in range(st): s += A[st, r]*ks[r, q]
                tmp[q] = y[q] + h*s
            f(tmp, ks[st])
        err = 0.0; yn = np.zeros(2)
        for q in range(2):
            y5 = y[q]; e = 0.0
            for r in range(7): y5 += h*B5[r]*ks[r, q]; e += h*(B5[r] - B4[r])*ks[r, q]
            yn[q] = y5; sc = atol + rtol*max(abs(y[q]), abs(y5)); err += (e/sc)**2
        return yn, math.sqrt(err/2)
    @nb.njit
    def run(y0, Nmax):
        ks = np.zeros((7, 2)); tmp = np.zeros(2); cap = 4096; Ns = np.empty(cap); Ys = np.empty((cap, 2)); n = 0
        y = y0.copy(); N = 0.0; h = 1e-3; Ns[0] = 0.0; Ys[0] = y
        while N < Nmax:
            yn, err = step(N, y, h, ks, tmp)
            if err <= 1.0:
                if 0.5*yn[1]*yn[1] >= 1.0:
                    lo = 0.0; hi = h
                    for it in range(80):
                        mid = 0.5*(lo + hi); yt, _ = step(N, y, mid, ks, tmp)
                        if 0.5*yt[1]*yt[1] >= 1.0: hi = mid
                        else: lo = mid
                    n += 1
                    if n >= cap:
                        cap *= 2; N2 = np.empty(cap); Y2 = np.empty((cap, 2)); N2[:n] = Ns[:n]; Y2[:n] = Ys[:n]; Ns = N2; Ys = Y2
                    Ns[n] = N + hi; Ys[n] = step(N, y, hi, ks, tmp)[0]
                    return Ns[:n+1], Ys[:n+1], True
                N += h; y = yn; n += 1
                if n >= cap:
                    cap *= 2; N2 = np.empty(cap); Y2 = np.empty((cap, 2)); N2[:n] = Ns[:n]; Y2[:n] = Ys[:n]; Ns = N2; Ys = Y2
                Ns[n] = N; Ys[n] = y
            h = h*min(5.0, max(0.2, 0.9*err**-0.2 if err > 0 else 5.0))
        return Ns[:n+1], Ys[:n+1], False
    @nb.njit
    def at(Ns, Ys, Nq):            # state at Nq: integrate from the last stored point <= Nq with the same tolerance
        i = np.searchsorted(Ns, Nq) - 1
        if i < 0: i = 0
        y = Ys[i].copy(); N = Ns[i]; ks = np.zeros((7, 2)); tmp = np.zeros(2); h = max(min(Nq - N, 1e-2), 1e-12)
        while N < Nq - 1e-15:
            if N + h > Nq: h = Nq - N
            yn, err = step(N, y, h, ks, tmp)
            if err <= 1.0: N += h; y = yn
            h = h*min(5.0, max(0.2, 0.9*err**-0.2 if err > 0 else 5.0))
        return y
    @nb.njit
    def grid_e1(Ns, Ys, Ng):       # ε1 on the whole grid in one compiled call (same per-point integration as at())
        out = np.zeros(Ng.size)
        for j in range(Ng.size):
            yv = at(Ns, Ys, Ng[j]); out[j] = 0.5*yv[1]*yv[1]
        return out
    return dict(V=V, dV=dV, run=run, at=at, grid_e1=grid_e1)
@nb.njit
def nak_slopes(y, h):
    """Slopes at the knots of the not-a-knot cubic spline on a uniform grid (= scipy CubicSpline(x, y).derivative()(x))."""
    n = y.size; Am = np.zeros((n, n)); b = np.zeros(n)
    for i in range(1, n - 1): Am[i, i-1] = 1.0; Am[i, i] = 4.0; Am[i, i+1] = 1.0; b[i] = 3.0*(y[i+1] - y[i-1])/h
    Am[0, 0] = 1.0; Am[0, 2] = -1.0; b[0] = 2.0*((y[1] - y[0]) - (y[2] - y[1]))/h
    Am[n-1, n-3] = 1.0; Am[n-1, n-1] = -1.0; b[n-1] = 2.0*((y[n-2] - y[n-3]) - (y[n-1] - y[n-2]))/h
    return np.linalg.solve(Am, b)
@nb.njit
def flow_chain(e1, h):
    e2 = nak_slopes(np.log(e1), h); e3 = nak_slopes(np.log(np.abs(e2)), h); e4 = nak_slopes(np.log(np.abs(e3)), h)
    return e2, e3, e4
class ModelJ:
    def __init__(self, m, phi0, Nmax=400.0):
        y0 = np.array([phi0, -m['dV'](phi0)/m['V'](phi0)]); Ns, Ys, ok = m['run'](y0, Nmax)
        if not ok: raise ValueError('inflation does not end within Nmax')
        self.Ns, self.Ys, self.Nend, self._at, self._g = Ns, Ys, float(Ns[-1]), m['at'], m['grid_e1']
    def flow4(self, Nstar, h=0.25, npts=41):
        Np = self.Nend - Nstar; Ng = np.linspace(Np - h*(npts//2)/10, Np + h*(npts//2)/10, npts)
        e1 = self._g(self.Ns, self.Ys, Ng)
        e2, e3, e4 = flow_chain(e1, Ng[1] - Ng[0]); i = npts//2
        return e1[i], e2[i], e3[i], e4[i]
def spectra3_jit(model, Nstar):
    e1, e2, e3, e4 = model.flow4(Nstar); a = AL; p2 = math.pi**2
    ns = 1 + (-2*e1 - e2 - 2*e1**2 - (3 - 2*a)*e1*e2 + a*e2*e3 - 2*e1**3 + (-15 + 6*a + p2)*e1**2*e2
              + (-84 + 36*a - 12*a*a + 7*p2)/12*e1*e2**2 + (-72 + 48*a - 12*a*a + 7*p2)/12*e1*e2*e3
              + (-8 + p2)/4*e2**2*e3 + (-a*a/2 + p2/24)*e2*e3**2 + (-a*a/2 + p2/24)*e2*e3*e4)
    als = (-2*e1*e2 - e2*e3 - 6*e1**2*e2 + (-3 + 2*a)*e1*e2**2 - 2*(2 - a)*e1*e2*e3 + a*e2*e3**2 + a*e2*e3*e4)
    return dict(ns=ns, r=16*e1*(1 + CE*e2), alpha_s=als, eps=(e1, e2, e3, e4))
# ---- DOP853 variant (coefficients taken programmatically from scipy, error norm as scipy's DOP853) ----
from scipy.integrate._ivp import dop853_coefficients as _d
A8 = np.ascontiguousarray(_d.A[:12, :12]); B8 = np.ascontiguousarray(_d.B); C8 = np.ascontiguousarray(_d.C[:12]); E3 = np.ascontiguousarray(_d.E3); E5 = np.ascontiguousarray(_d.E5)
def build8(Vexpr, y, rtol=1e-12, atol=1e-14):
    x = sp.Symbol('x'); e = Vexpr.subs(y, x); ns = {'math': math}
    exec(f"def _V(x):\n    return {sp.pycode(e)}\ndef _dV(x):\n    return {sp.pycode(sp.diff(e, x))}\n", ns)
    V = nb.njit(ns['_V']); dV = nb.njit(ns['_dV'])
    @nb.njit
    def f(y, out):
        p = y[0]; pn = y[1]; eps = 0.5*pn*pn; out[0] = pn; out[1] = -(3 - eps)*pn - (3 - eps)*dV(p)/V(p)
    @nb.njit
    def step(y, h, K, tmp):
        f(y, K[0])
        for s in range(1, 12):
            for q in range(2):
                a = 0.0
                for r in range(s): a += A8[s, r]*K[r, q]
                tmp[q] = y[q] + h*a
            f(tmp, K[s])
        yn = np.zeros(2)
        for q in range(2):
            a = 0.0
            for r in range(12): a += B8[r]*K[r, q]
            yn[q] = y[q] + h*a
        f(yn, K[12]); e5 = 0.0; e3 = 0.0
        for q in range(2):
            sc = atol + rtol*max(abs(y[q]), abs(yn[q])); a5 = 0.0; a3 = 0.0
            for r in range(13): a5 += E5[r]*K[r, q]; a3 += E3[r]*K[r, q]
            e5 += (a5/sc)**2; e3 += (a3/sc)**2
        if e5 == 0.0 and e3 == 0.0: return yn, 0.0
        return yn, abs(h)*e5/math.sqrt((e5 + 0.01*e3)*2)
    @nb.njit
    def run(y0, Nmax):
        K = np.zeros((13, 2)); tmp = np.zeros(2); cap = 1024; Ns = np.empty(cap); Ys = np.empty((cap, 2)); n = 0
        y = y0.copy(); N = 0.0; h = 1e-2; Ns[0] = 0.0; Ys[0] = y
        while N < Nmax:
            yn, err = step(y, h, K, tmp)
            if err <= 1.0:
                if 0.5*yn[1]*yn[1] >= 1.0:
                    lo = 0.0; hi = h
                    for it in range(80):
                        mid = 0.5*(lo + hi); yt, _ = step(y, mid, K, tmp)
                        if 0.5*yt[1]*yt[1] >= 1.0: hi = mid
                        else: lo = mid
                    n += 1
                    if n >= cap:
                        cap *= 2; N2 = np.empty(cap); Y2 = np.empty((cap, 2)); N2[:n] = Ns[:n]; Y2[:n] = Ys[:n]; Ns = N2; Ys = Y2
                    Ns[n] = N + hi; Ys[n] = step(y, hi, K, tmp)[0]
                    return Ns[:n+1], Ys[:n+1], True
                N += h; y = yn; n += 1
                if n >= cap:
                    cap *= 2; N2 = np.empty(cap); Y2 = np.empty((cap, 2)); N2[:n] = Ns[:n]; Y2[:n] = Ys[:n]; Ns = N2; Ys = Y2
                Ns[n] = N; Ys[n] = y
            h = h*min(10.0, max(0.2, 0.9*err**(-1.0/8) if err > 0 else 10.0))
        return Ns[:n+1], Ys[:n+1], False
    @nb.njit
    def at(Ns, Ys, Nq):
        i = np.searchsorted(Ns, Nq) - 1
        if i < 0: i = 0
        y = Ys[i].copy(); N = Ns[i]; K = np.zeros((13, 2)); tmp = np.zeros(2); h = max(min(Nq - N, 1e-1), 1e-12)
        while N < Nq - 1e-15:
            if N + h > Nq: h = Nq - N
            yn, err = step(y, h, K, tmp)
            if err <= 1.0: N += h; y = yn
            h = h*min(10.0, max(0.2, 0.9*err**(-1.0/8) if err > 0 else 10.0))
        return y
    @nb.njit
    def grid_e1(Ns, Ys, Ng):
        out = np.zeros(Ng.size)
        for j in range(Ng.size):
            yv = at(Ns, Ys, Ng[j]); out[j] = 0.5*yv[1]*yv[1]
        return out
    return dict(V=V, dV=dV, run=run, at=at, grid_e1=grid_e1)
