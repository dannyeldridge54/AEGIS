# AEGIS-FP H2TAAOANSEB2SZRK · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""JANUS-MF-NC: exact multi-field MS on a curved field space (Kaiser et al. arXiv 1511.09148 Eqs. 14-19, 24), e-fold time, M_P = 1.
Q^I evolved in the coordinate basis with D_N Q = Q' + Γ Q φ'. P' = D_N P covariant. Riemann: R^a_{bcd} = ∂_c Γ^a_{db} − ∂_d Γ^a_{cb} + Γ^a_{ce}Γ^e_{db} − Γ^a_{de}Γ^e_{cb}
(sphere positive; mass term −R^I_{LMJ}φ'^Lφ'^M gives +ε H² R_fs on the entropic direction in 2D, checked in curvature_sign_check)."""
import math, numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import sqrtm
def build(Vexpr, Gexpr, f):
    n = len(f); G = sp.Matrix(Gexpr); Gi = G.inv()
    Gam = [[[sp.simplify(sum(Gi[a, d]*(sp.diff(G[d, b], f[c]) + sp.diff(G[d, c], f[b]) - sp.diff(G[b, c], f[d])) for d in range(n))/2) for c in range(n)] for b in range(n)] for a in range(n)]
    R = [[[[sp.simplify(sp.diff(Gam[a][d][b], f[c]) - sp.diff(Gam[a][c][b], f[d]) + sum(Gam[a][c][e]*Gam[e][d][b] - Gam[a][d][e]*Gam[e][c][b] for e in range(n)))
           for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    dV = [sp.diff(Vexpr, x) for x in f]; ddV = [[sp.diff(Vexpr, x, y) for y in f] for x in f]
    L = lambda e: sp.lambdify([f], e, 'numpy')
    return dict(n=n, V=L(Vexpr), dV=L(sp.Matrix(dV)), ddV=L(sp.Matrix(ddV)), G=L(G), Gi=L(Gi), Gam=L(sp.Array(Gam)), R=L(sp.Array(R)))
def _num(m, f):
    return (float(m['V'](f)), np.array(m['dV'](f), float).ravel(), np.array(m['ddV'](f), float), np.array(m['G'](f), float),
            np.array(m['Gi'](f), float), np.array(m['Gam'](f), float), np.array(m['R'](f), float))
def background(m, f0, fdot0):
    n = m['n']; V, dV, _, G, Gi, Gam, _ = _num(m, f0)
    H = math.sqrt((0.5*fdot0 @ G @ fdot0 + V)/3.0); fp0 = np.array(fdot0)/H
    def rhs(N, u):
        f, fp = u[:n], u[n:]; V, dV, _, G, Gi, Gam, _ = _num(m, f); eps = 0.5*fp @ G @ fp
        fpp = -np.einsum('ijk,j,k->i', Gam, fp, fp) - (3 - eps)*(fp + Gi @ dV/V)
        return np.concatenate([fp, fpp])
    def end(N, u):
        f, fp = u[:n], u[n:]; G = np.array(m['G'](f), float); return 0.5*fp @ G @ fp - 1.0
    end.terminal = True; end.direction = 1
    s = solve_ivp(rhs, [0, 2000], np.concatenate([f0, fp0]), method='DOP853', rtol=1e-12, atol=1e-14, dense_output=True, events=end)
    Ne = s.t[-1]
    def st(N):
        u = s.sol(N); f, fp = u[:n], u[n:]; V, dV, ddV, G, Gi, Gam, R = _num(m, f); eps = 0.5*fp @ G @ fp
        return f, fp, eps, V/(3 - eps), V, dV, ddV, G, Gi, Gam, R
    return st, Ne
def _mass(fp, eps, H2, V, dV, ddV, G, Gi, Gam, R):
    covH = ddV - np.einsum('kij,k->ij', Gam, dV)                     # ∇_J∇_K V
    fl = G @ fp; Vu = Gi @ dV
    M = Gi @ covH - np.einsum('ilmj,l,m->ij', R, fp, fp)*H2 + (3 - eps)*np.outer(fp, fl)*H2 + (np.outer(Vu, fl) + np.outer(fp, dV))
    return M/H2                                                          # M^I_J / H²
def _mode(st, n, k, N0, Nend, Nref=0.0):
    f, fp, eps, H2, V, dV, ddV, G, Gi, Gam, R = st(N0); a = math.exp(N0 - Nref); H = math.sqrt(H2)
    eta = -1.0/(a*H*(1 - eps)); u = (1 - 1j/(k*eta))*np.exp(-1j*k*eta)/math.sqrt(2*k)
    du = (-1j*k*(1 - 1j/(k*eta)) + 1j/(k*eta**2))*np.exp(-1j*k*eta)/math.sqrt(2*k); un = du/(a*H)
    e = np.real(sqrtm(Gi))                                               # vielbein: e^T G e = 1
    Q0 = e*(u/a); P0 = e*((un - u)/a)
    def rhs(N, y):
        f, fp, eps, H2, V, dV, ddV, G, Gi, Gam, R = st(N); a = math.exp(N - Nref); q2 = k*k/(a*a*H2)
        Q = y[:2*n*n].view(complex).reshape(n, n); P = y[2*n*n:4*n*n].view(complex).reshape(n, n)
        Qn = P - np.einsum('ijk,ja,k->ia', Gam, Q, fp)
        Pn = -np.einsum('ijk,ja,k->ia', Gam, P, fp) - (3 - eps)*P - q2*Q - _mass(fp, eps, H2, V, dV, ddV, G, Gi, Gam, R) @ Q
        return np.concatenate([Qn.ravel().view(float), Pn.ravel().view(float)])
    y0 = np.concatenate([Q0.astype(complex).ravel().view(float), P0.astype(complex).ravel().view(float)])
    s = solve_ivp(rhs, [N0, Nend], y0, method='DOP853', rtol=1e-10, atol=1e-30)
    Q = s.y[:2*n*n, -1].view(complex).reshape(n, n)
    f, fp, eps, H2, V, dV, ddV, G, Gi, Gam, R = st(Nend); sp2 = fp @ G @ fp; w = G @ fp/math.sqrt(sp2)
    PQ = k**3/(2*math.pi**2)*(Q @ Q.conj().T).real
    return float(w @ PQ @ w)/sp2
def spectra_nc(m, f0, fdot0, Nstar=55.0, dlnk=0.4, npts=9, bd=1000.0):
    st, Ne = background(m, np.array(f0, float), np.array(fdot0, float)); Np = Ne - Nstar
    kp = math.sqrt(st(Np)[3]);   # JMF13: a = e^(N - Np)
    lks = np.linspace(-dlnk, dlnk, npts); PRs = []
    for d in lks:
        k = kp*math.exp(d); lo, hi = 0.0, Np
        for _ in range(80):
            mid = 0.5*(lo + hi); g = k/(math.exp(mid - Np)*math.sqrt(st(mid)[3])) - bd
            lo, hi = (mid, hi) if g > 0 else (lo, mid)
        PRs.append(_mode(st, m['n'], k, lo, Ne, Np))
    c = np.polyfit(lks, np.log(PRs), 2); return dict(ns=1 + c[1], PR=PRs[npts//2], Ne=Ne)
def curvature_sign_check(m, f, fp):
    """2D: entropic projection of −R^I_{LMJ}φ'^Lφ'^M must equal +(R_fs/2)·σ'²."""
    V, dV, ddV, G, Gi, Gam, R = _num(m, f); sp2 = fp @ G @ fp; t = fp/math.sqrt(sp2)
    s = np.array([-t[1], t[0]]); s = s/math.sqrt(s @ Gi @ s); s_up = Gi @ s     # unit normal: lower s_I with s_I t^I = 0
    proj = -(G @ s_up) @ np.einsum('ilmj,l,m->ij', R, fp, fp) @ s_up
    Ric = np.einsum('aiaj->ij', R); Rs = float(np.einsum('ij,ij', Gi, Ric))
    return proj, 0.5*Rs*sp2
