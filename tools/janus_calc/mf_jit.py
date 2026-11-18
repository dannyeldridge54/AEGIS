# AEGIS-FP ZJBFZNVAHIVH5PMG · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""JANUS-MF-JIT: spectra_mf_fast's equations (MultiModeCode Eqs. 3.11–3.23, as tools/janus_calc/mfms.py) with the whole integration compiled by numba.
Background + all k-modes + tensors in one real ODE system, adaptive Dormand–Prince 5(4) with the same rtol (1e-10). Potential given as a sympy expression.
Equivalence vs spectra_mf: PREREG_JMF11_jit."""
import math, numpy as np, sympy as sp, numba as nb
def _codegen(Vexpr, f):
    n = len(f); sub = {f[i]: sp.Symbol(f'x{i}') for i in range(n)}
    g = [sp.pycode(sp.diff(Vexpr, f[i]).subs(sub)) for i in range(n)]
    h = [[sp.pycode(sp.diff(Vexpr, f[i], f[j]).subs(sub)) for j in range(n)] for i in range(n)]
    un = '; '.join(f'x{i} = p[{i}]' for i in range(n))
    src = f"def _V(p):\n    {un}\n    return {sp.pycode(Vexpr.subs(sub))}\n"
    src += f"def _G(p, out):\n    {un}\n" + ''.join(f"    out[{i}] = {g[i]}\n" for i in range(n))
    src += f"def _H(p, out):\n    {un}\n" + ''.join(f"    out[{i},{j}] = {h[i][j]}\n" for i in range(n) for j in range(n))
    ns = {'math': math}; exec(src, ns); return nb.njit(ns['_V']), nb.njit(ns['_G']), nb.njit(ns['_H'])
A = np.array([[0,0,0,0,0,0], [1/5,0,0,0,0,0], [3/40,9/40,0,0,0,0], [44/45,-56/15,32/9,0,0,0],
              [19372/6561,-25360/2187,64448/6561,-212/729,0,0], [9017/3168,-355/33,46732/5247,49/176,-5103/18656,0], [35/384,0,500/1113,125/192,-2187/6784,11/84]])
B5 = np.array([35/384,0,500/1113,125/192,-2187/6784,11/84,0]); B4 = np.array([5179/57600,0,7571/16695,393/640,-92097/339200,187/2100,1/40])
CC = np.array([0,1/5,3/10,4/5,8/9,1,1])
def build(Vexpr, f):
    n = len(f); V, G, H = _codegen(Vexpr, f)
    @nb.njit(cache=False)
    def rhs(N, y, k2, K, Nref, out, g, hs):
        p = y[:n]; fp = y[n:2*n]; eps = 0.0
        for i in range(n): eps += 0.5*fp[i]*fp[i]
        v = V(p); G(p, g); H2 = v/(3 - eps)
        for i in range(n): out[i] = fp[i]; out[n+i] = -(3 - eps)*(fp[i] + g[i]/v)
        if K == 0: return
        H(p, hs); a2H2 = math.exp(2*(N - Nref))*H2
        for i in range(n):
            for j in range(n): hs[i, j] = hs[i, j]/H2 + (fp[i]*g[j] + g[i]*fp[j])/H2 + (3 - eps)*fp[i]*fp[j]
        o = 2*n; m = n*n
        for kk in range(K):
            q2 = k2[kk]/a2H2
            for part in range(2):                       # real, imag
                b = o + (kk*2 + part)*2*m              # block: Y (m) then Yn (m)
                for i in range(n):
                    for c in range(n):
                        Yic = y[b + i*n + c]; Ynic = y[b + m + i*n + c]; s = 0.0
                        for j in range(n): s += hs[i, j]*y[b + j*n + c]
                        out[b + i*n + c] = Ynic
                        out[b + m + i*n + c] = -(1 - eps)*Ynic - (q2 - 2 + eps)*Yic - s
            t = o + K*4*m + kk*4                         # tensor: h_re, h_im, hn_re, hn_im
            out[t] = y[t+2]; out[t+1] = y[t+3]; out[t+2] = -(3 - eps)*y[t+2] - q2*y[t]; out[t+3] = -(3 - eps)*y[t+3] - q2*y[t+1]
    @nb.njit(cache=False)
    def integ(N0, N1, y0, k2, K, rtol, atol, stop_eps, Nref=0.0):
        y = y0.copy(); d = y.size; ks = np.zeros((7, d)); g = np.zeros(n); hs = np.zeros((n, n)); tmp = np.zeros(d)
        N = N0; h = 1e-3; nst = 0
        while N < N1:
            if N + h > N1: h = N1 - N
            rhs(N, y, k2, K, Nref, ks[0], g, hs)
            for st in range(1, 7):
                for q in range(d):
                    s = 0.0
                    for r in range(st): s += A[st, r]*ks[r, q]
                    tmp[q] = y[q] + h*s
                rhs(N + CC[st]*h, tmp, k2, K, Nref, ks[st], g, hs)
            err = 0.0
            for q in range(d):
                y5 = y[q]; e = 0.0
                for r in range(7): y5 += h*B5[r]*ks[r, q]; e += h*(B5[r] - B4[r])*ks[r, q]
                tmp[q] = y5; sc = atol + rtol*max(abs(y[q]), abs(y5)); e = e/sc; err += e*e
            err = math.sqrt(err/d)
            if err <= 1.0:
                if stop_eps:
                    e1 = 0.0
                    for i in range(n): e1 += 0.5*tmp[n+i]*tmp[n+i]
                    if e1 >= 1.0:                    # bisect the step to land on eps = 1
                        lo = 0.0; hi = h; ytry = tmp.copy()
                        for it in range(60):
                            mid = 0.5*(lo + hi); yy = y.copy()
                            # re-step with size mid (one DP5 step)
                            rhs(N, yy, k2, K, Nref, ks[0], g, hs)
                            for st in range(1, 7):
                                for q in range(d):
                                    s = 0.0
                                    for r in range(st): s += A[st, r]*ks[r, q]
                                    tmp[q] = yy[q] + mid*s
                                rhs(N + CC[st]*mid, tmp, k2, K, Nref, ks[st], g, hs)
                            for q in range(d):
                                s = yy[q]
                                for r in range(7): s += mid*B5[r]*ks[r, q]
                                ytry[q] = s
                            e1 = 0.0
                            for i in range(n): e1 += 0.5*ytry[n+i]*ytry[n+i]
                            if e1 >= 1.0: hi = mid
                            else: lo = mid
                        return N + hi, ytry, nst
                N += h; y[:] = tmp; nst += 1
            fac = 0.9*err**-0.2 if err > 0 else 5.0
            h = h*min(5.0, max(0.2, fac))
        return N, y, nst
    return dict(n=n, V=V, G=G, integ=integ)
def spectra_jit(m, f0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0, rtol=1.00002257189e-10):
    n = m['n']; integ = m['integ']; V = m['V']; f0 = np.array(f0, float); E = np.zeros(1)
    g0 = np.zeros(n); m_g = None
    # slow-roll start (as spectra_mf): v0 = -grad/V
    gr = np.zeros(n); m['G'](f0, gr)
    y0 = np.concatenate([f0, -gr/V(f0)])
    Ne, yend, _ = integ(0.0, 2000.0, y0, E, 0, 1e-12, 1e-14, True)
    Np = Ne - Nstar
    def bgat(N):
        if N <= 0: return y0
        return integ(0.0, N, y0, E, 0, 1e-12, 1e-14, False)[1]
    def H2at(yb):
        fp = yb[n:]; eps = 0.5*fp @ fp; return V(yb[:n])/(3 - eps), eps
    yp = bgat(Np); kp = math.sqrt(H2at(yp)[0])
    lks = np.linspace(-dlnk, dlnk, npts); ks = kp*np.exp(lks); K = npts; kmin = ks.min()
    lo, hi = 0.0, Np
    for _ in range(60):
        mid = 0.5*(lo + hi); yb = bgat(mid); gg = kmin/(math.exp(mid - Np)*math.sqrt(H2at(yb)[0])) - bd
        lo, hi = (mid, hi) if gg > 0 else (lo, mid)
    N0 = lo; yb = bgat(N0); H2, eps = H2at(yb); a = math.exp(N0 - Np); H = math.sqrt(H2)
    eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(ks*eta))*np.exp(-1j*ks*eta)/np.sqrt(2*ks)
    du = (-1j*ks*(1 - 1j/(ks*eta)) + 1j/(ks*eta**2))*np.exp(-1j*ks*eta)/np.sqrt(2*ks); un = du/(a*H)
    mm = n*n; y = np.zeros(2*n + K*4*mm + K*4); y[:2*n] = yb; I = np.eye(n).ravel(); o = 2*n
    for kk in range(K):
        for part, fn in ((0, np.real), (1, np.imag)):
            b = o + (kk*2 + part)*2*mm; y[b:b+mm] = fn(u[kk])*I; y[b+mm:b+2*mm] = fn(un[kk])*I
        t = o + K*4*mm + kk*4; h0 = u[kk]/a; hn0 = un[kk]/a - u[kk]/a; y[t:t+4] = [h0.real, h0.imag, hn0.real, hn0.imag]
    _, yf, nst = integ(N0, Ne, y, ks*ks, K, rtol, 1e-30, False, Np)
    fp = yf[n:2*n]; w = fp/np.linalg.norm(fp); a = math.exp(Ne - Np); PRs = []; Phs = []
    for kk in range(K):
        Yr = yf[o + (kk*2)*2*mm: o + (kk*2)*2*mm + mm].reshape(n, n); Yi = yf[o + (kk*2 + 1)*2*mm: o + (kk*2 + 1)*2*mm + mm].reshape(n, n)
        Y = Yr + 1j*Yi; Pd = ks[kk]**3/(2*math.pi**2)*(Y @ Y.conj().T).real/a**2; PRs.append(float(w @ Pd @ w)/(fp @ fp))
        t = o + K*4*mm + kk*4; hh = yf[t] + 1j*yf[t+1]; Phs.append(8*ks[kk]**3*abs(hh)**2/(2*math.pi**2))
    lp = np.log(PRs); c = np.polyfit(lks, lp, 2); i0 = npts//2
    return dict(ns=1 + c[1], alpha_s=2*c[0], r=Phs[i0]/PRs[i0], PR=PRs[i0], Ne=Ne, steps=nst)
