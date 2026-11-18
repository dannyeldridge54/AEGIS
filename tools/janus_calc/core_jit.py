"""Janus single-field fast face, compiled: core.Model + core.spectra3 with the background integrated by a compiled Dormand–Prince 5(4)
(rtol 1e-12, atol 1e-14, as core.Model's DOP853), ε1 = 1 end found by bisection inside the compiled step, and ε-flow parameters from the
same 41-point CubicSpline construction as core.flow4. Potential from a sympy expression. Equivalence vs core: PREREG_JSJ1."""
import math, numpy as np, sympy as sp, numba as nb
from scipy.interpolate import CubicSpline
from tools.janus_calc.mf_jit import A, B5, B4, CC
from tools.janus_calc.core import AL, CE
def build(Vexpr, y):
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
            yn[q] = y5; sc = 1e-14 + 1e-12*max(abs(y[q]), abs(y5)); err += (e/sc)**2
        return yn, math.sqrt(err/2)
    @nb.njit
    def run(y0, Nmax):
        ks = np.zeros((7, 2)); tmp = np.zeros(2); Ns = np.zeros(200000); Ys = np.zeros((200000, 2)); n = 0
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
                    n += 1; Ns[n] = N + hi; Ys[n] = step(N, y, hi, ks, tmp)[0]
                    return Ns[:n+1], Ys[:n+1], True
                N += h; y = yn; n += 1; Ns[n] = N; Ys[n] = y
                if n >= 199999: break
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
