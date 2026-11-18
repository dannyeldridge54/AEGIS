"""JANUS-MF-NC-JIT: mfms_nc's equations (Kaiser et al. 1511.09148 Eqs. 14-19, 24; coordinate basis, D_N Q = Q' + ΓQφ') compiled with numba.
Background + all k-modes in one real ODE system, adaptive Dormand–Prince 5(4). Equivalence vs mfms_nc.spectra_nc: PREREG_JMF12_ncjit."""
import math, numpy as np, sympy as sp, numba as nb
from scipy.linalg import sqrtm
from janus_calc.mfms_nc import build as build_sym
from janus_calc.mf_jit import A, B5, B4, CC
def _codegen(Vexpr, Gexpr, f):
    n = len(f); sub = {f[i]: sp.Symbol(f'x{i}') for i in range(n)}; P = lambda e: sp.pycode(sp.sympify(e).subs(sub))
    G = sp.Matrix(Gexpr); Gi = G.inv()
    Gam = [[[sp.simplify(sum(Gi[a, d]*(sp.diff(G[d, b], f[c]) + sp.diff(G[d, c], f[b]) - sp.diff(G[b, c], f[d])) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    R = [[[[sp.simplify(sp.diff(Gam[a][d][b], f[c]) - sp.diff(Gam[a][c][b], f[d]) + sum(Gam[a][c][e]*Gam[e][d][b] - Gam[a][d][e]*Gam[e][c][b] for e in range(n)))
           for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    un = '; '.join(f'x{i} = p[{i}]' for i in range(n)); L = []
    L.append(f"def _V(p):\n    {un}\n    return {P(Vexpr)}\n")
    L.append(f"def _geo(p, dV, ddV, Gm, Gim, Gam, R):\n    {un}\n" +
             ''.join(f"    dV[{i}] = {P(sp.diff(Vexpr, f[i]))}\n" for i in range(n)) +
             ''.join(f"    ddV[{i},{j}] = {P(sp.diff(Vexpr, f[i], f[j]))}\n    Gm[{i},{j}] = {P(G[i, j])}\n    Gim[{i},{j}] = {P(Gi[i, j])}\n" for i in range(n) for j in range(n)) +
             ''.join(f"    Gam[{a},{b},{c}] = {P(Gam[a][b][c])}\n" for a in range(n) for b in range(n) for c in range(n)) +
             ''.join(f"    R[{a},{b},{c},{d}] = {P(R[a][b][c][d])}\n" for a in range(n) for b in range(n) for c in range(n) for d in range(n)))
    ns = {'math': math}; exec(''.join(L), ns); return nb.njit(ns['_V']), nb.njit(ns['_geo'])
def build(Vexpr, Gexpr, f):
    n = len(f); V, geo = _codegen(Vexpr, Gexpr, f)
    @nb.njit
    def rhs(N, y, k2, K, Nref, out, w):
        dV, ddV, Gm, Gim, Gam, R, M, fl, Vu = w
        p = y[:n]; fp = y[n:2*n]; geo(p, dV, ddV, Gm, Gim, Gam, R); v = V(p)
        eps = 0.0
        for i in range(n):
            for j in range(n): eps += 0.5*fp[i]*Gm[i, j]*fp[j]
        H2 = v/(3 - eps)
        for i in range(n):
            s = 0.0; gv = 0.0
            for j in range(n):
                gv += Gim[i, j]*dV[j]
                for c in range(n): s += Gam[i, j, c]*fp[j]*fp[c]
            out[i] = fp[i]; out[n+i] = -s - (3 - eps)*(fp[i] + gv/v)
        if K == 0: return
        for i in range(n):
            fl[i] = 0.0; Vu[i] = 0.0
            for j in range(n): fl[i] += Gm[i, j]*fp[j]; Vu[i] += Gim[i, j]*dV[j]
        for i in range(n):
            for j in range(n):
                cov = 0.0                                   # (G^-1 ∇∇V)^i_j
                for kq in range(n):
                    h = ddV[j, kq]
                    for l in range(n): h -= Gam[l, j, kq]*dV[l]
                    cov += Gim[i, kq]*h
                rr = 0.0
                for l in range(n):
                    for mm in range(n): rr += R[i, l, mm, j]*fp[l]*fp[mm]
                M[i, j] = cov/H2 - rr + (3 - eps)*fp[i]*fl[j] + (Vu[i]*fl[j] + fp[i]*dV[j])/H2
        a2H2 = math.exp(2*(N - Nref))*H2; o = 2*n; m = n*n
        for kk in range(K):
            q2 = k2[kk]/a2H2
            for part in range(2):
                b = o + (kk*2 + part)*2*m
                for i in range(n):
                    for c in range(n):
                        gq = 0.0; gp = 0.0; mq = 0.0
                        for j in range(n):
                            for l in range(n):
                                gq += Gam[i, j, l]*y[b + j*n + c]*fp[l]; gp += Gam[i, j, l]*y[b + m + j*n + c]*fp[l]
                            mq += M[i, j]*y[b + j*n + c]
                        out[b + i*n + c] = y[b + m + i*n + c] - gq
                        out[b + m + i*n + c] = -gp - (3 - eps)*y[b + m + i*n + c] - q2*y[b + i*n + c] - mq
    @nb.njit
    def integ(N0, N1, y0, k2, K, rtol, atol, stop_eps, Nref=0.0):
        y = y0.copy(); d = y.size; ks = np.zeros((7, d)); tmp = np.zeros(d)
        w = (np.zeros(n), np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n)), np.zeros((n, n, n)), np.zeros((n, n, n, n)), np.zeros((n, n)), np.zeros(n), np.zeros(n))
        N = N0; h = 1e-3; nst = 0
        while N < N1:
            if N + h > N1: h = N1 - N
            rhs(N, y, k2, K, Nref, ks[0], w)
            for st in range(1, 7):
                for q in range(d):
                    s = 0.0
                    for r in range(st): s += A[st, r]*ks[r, q]
                    tmp[q] = y[q] + h*s
                rhs(N + CC[st]*h, tmp, k2, K, Nref, ks[st], w)
            err = 0.0
            for q in range(d):
                y5 = y[q]; e = 0.0
                for r in range(7): y5 += h*B5[r]*ks[r, q]; e += h*(B5[r] - B4[r])*ks[r, q]
                tmp[q] = y5; sc = atol + rtol*max(abs(y[q]), abs(y5)); e = e/sc; err += e*e
            err = math.sqrt(err/d)
            if err <= 1.0:
                if stop_eps:
                    Gm = w[2]; e1 = 0.0
                    for i in range(n):
                        for j in range(n): e1 += 0.5*tmp[n+i]*Gm[i, j]*tmp[n+j]   # Gm from last rhs call (close enough only for the test; refined below)
                    if e1 >= 0.999:
                        lo = 0.0; hi = h; yt = tmp.copy()
                        for it in range(60):
                            mid = 0.5*(lo + hi); rhs(N, y, k2, K, Nref, ks[0], w)
                            for st in range(1, 7):
                                for q in range(d):
                                    s = 0.0
                                    for r in range(st): s += A[st, r]*ks[r, q]
                                    tmp[q] = y[q] + mid*s
                                rhs(N + CC[st]*mid, tmp, k2, K, Nref, ks[st], w)
                            for q in range(d):
                                s = y[q]
                                for r in range(7): s += mid*B5[r]*ks[r, q]
                                yt[q] = s
                            rhs(N + mid, yt, k2, 0, Nref, tmp, w); Gm = w[2]; e1 = 0.0
                            for i in range(n):
                                for j in range(n): e1 += 0.5*yt[n+i]*Gm[i, j]*yt[n+j]
                            if e1 >= 1.0: hi = mid
                            else: lo = mid
                        if e1 >= 1.0 or hi < h: return N + hi, yt, nst
                N += h; y[:] = tmp; nst += 1
            fac = 0.9*err**-0.2 if err > 0 else 5.0
            h = h*min(5.0, max(0.2, fac))
        return N, y, nst
    return dict(n=n, V=V, geo=geo, integ=integ)
def spectra_ncjit(m, f0, fdot0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0, rtol=1e-11):
    n = m['n']; integ = m['integ']; V = m['V']; geo = m['geo']; E = np.zeros(1); f0 = np.array(f0, float); fdot0 = np.array(fdot0, float)
    dV = np.zeros(n); ddV = np.zeros((n, n)); Gm = np.zeros((n, n)); Gim = np.zeros((n, n)); Ga = np.zeros((n, n, n)); Rr = np.zeros((n, n, n, n))
    def G_at(p): geo(p, dV, ddV, Gm, Gim, Ga, Rr); return Gm.copy(), Gim.copy()
    G0, _ = G_at(f0); H = math.sqrt((0.5*fdot0 @ G0 @ fdot0 + V(f0))/3.0); y0 = np.concatenate([f0, fdot0/H])
    Ne, _, _ = integ(0.0, 2000.0, y0, E, 0, 1e-12, 1e-14, True); Np = Ne - Nstar
    def bgat(N): return y0 if N <= 0 else integ(0.0, N, y0, E, 0, 1e-12, 1e-14, False)[1]
    def H2eps(yb):
        G, _ = G_at(yb[:n]); fp = yb[n:]; e = 0.5*fp @ G @ fp; return V(yb[:n])/(3 - e), e
    kp = math.sqrt(H2eps(bgat(Np))[0]); lks = np.linspace(-dlnk, dlnk, npts); ks = kp*np.exp(lks); K = npts
    lo, hi = 0.0, Np
    for _ in range(60):
        mid = 0.5*(lo + hi); gg = ks.min()/(math.exp(mid - Np)*math.sqrt(H2eps(bgat(mid))[0])) - bd
        lo, hi = (mid, hi) if gg > 0 else (lo, mid)
    N0 = lo; yb = bgat(N0); H2, eps = H2eps(yb); a = math.exp(N0 - Np); Hh = math.sqrt(H2)
    eta = -1.0/(a*Hh*(1 - eps)); u = (1 - 1j/(ks*eta))*np.exp(-1j*ks*eta)/np.sqrt(2*ks)
    du = (-1j*ks*(1 - 1j/(ks*eta)) + 1j/(ks*eta**2))*np.exp(-1j*ks*eta)/np.sqrt(2*ks); un = du/(a*Hh)
    _, Gi0 = G_at(yb[:n]); e = np.real(sqrtm(Gi0)); mm = n*n; o = 2*n
    y = np.zeros(2*n + K*4*mm); y[:2*n] = yb
    for kk in range(K):
        Q0 = e*(u[kk]/a); P0 = e*((un[kk] - u[kk])/a)
        for part, fn in ((0, np.real), (1, np.imag)):
            b = o + (kk*2 + part)*2*mm; y[b:b+mm] = fn(Q0).ravel(); y[b+mm:b+2*mm] = fn(P0).ravel()
    _, yf, nst = integ(N0, Ne, y, ks*ks, K, rtol, 1e-30, False, Np)
    G, _ = G_at(yf[:n]); fp = yf[n:2*n]; sp2 = fp @ G @ fp; w = G @ fp/math.sqrt(sp2); PRs = []
    for kk in range(K):
        Qr = yf[o + kk*4*mm: o + kk*4*mm + mm].reshape(n, n); Qi = yf[o + (kk*2 + 1)*2*mm: o + (kk*2 + 1)*2*mm + mm].reshape(n, n); Q = Qr + 1j*Qi
        PQ = ks[kk]**3/(2*math.pi**2)*(Q @ Q.conj().T).real; PRs.append(float(w @ PQ @ w)/sp2)
    c = np.polyfit(lks, np.log(PRs), 2); return dict(ns=1 + c[1], PR=PRs[npts//2], Ne=Ne, steps=nst)
