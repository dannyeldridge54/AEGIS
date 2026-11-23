"""Spindle fast paths (SPEED-Spindle). Reference engine: loom_qsim.py (unchanged)."""
import math, numpy as np, itertools
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from loom_qsim import sma_hamiltonian, sma_coherent, mf_rhs

def sma_rho0_fast(N, c, q, zeta, ts):
    H = sma_hamiltonian(N, c, q); w, V = np.linalg.eigh(H); a0 = V.conj().T @ sma_coherent(N, zeta)
    n0 = np.array([N - 2*k for k in range(N//2 + 1)])/N
    P = V @ (np.exp(-1j*np.outer(w, np.asarray(ts))) * a0[:, None])      # (K, T) in one product
    return (n0[:, None]*abs(P)**2).sum(0), H

def _z(rho0, phi):
    return np.array([math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2), math.sqrt(rho0), math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2)])

def mf_single_fast(c, q, rho0, phi, ts):
    z = _z(rho0, phi)
    def f(t, y):
        psi = (y[:3] + 1j*y[3:]).reshape(1, 3); d = mf_rhs(psi, c, q, 0.0, 1.0)[0]
        return np.concatenate([d.real, d.imag])
    sol = solve_ivp(f, (0, ts[-1]), np.concatenate([z.real, z.imag]), method='DOP853', rtol=1e-10, atol=1e-12, t_eval=ts)
    return abs(sol.y[1] + 1j*sol.y[4])**2

def period_analytic(c, q, rho0, phi):
    """Single-mode mean field, m = 0: E = c r(1-r)(1+cos th) - q r with th = 2*phi/2 + ... (th = phase(z1 zm / z0^2))."""
    z = _z(rho0, phi); th = np.angle(z[0]*z[2]/z[1]**2)
    E = c*rho0*(1 - rho0)*(1 + math.cos(th)) - q*rho0
    g = lambda r: 4*(E + q*r)*(2*c*r*(1 - r) - E - q*r)       # (dr/dt)^2
    # turning points: roots of the cubic in [0, 1] bracketing rho0
    rs = np.linspace(1e-12, 1 - 1e-12, 20001); gv = np.array([g(r) for r in rs])
    roots = [brentq(g, rs[i], rs[i + 1]) for i in range(len(rs) - 1) if gv[i] == 0 or gv[i]*gv[i + 1] < 0]
    lo = max([r for r in roots if r <= rho0 + 1e-12], default=0.0); hi = min([r for r in roots if r >= rho0 - 1e-12], default=1.0)
    if abs(hi - lo) < 1e-12: return float('nan')
    # substitution r = lo + (hi-lo) sin^2(u) removes the endpoint singularities
    def integrand(u):
        r = lo + (hi - lo)*math.sin(u)**2; v = g(r)
        return 2*(hi - lo)*math.sin(u)*math.cos(u)/math.sqrt(v) if v > 0 else 0.0
    T, _ = quad(integrand, 0, math.pi/2, limit=400, epsabs=1e-12, epsrel=1e-12)
    return 2*T

def bh_spectrum_sparse(L, N, J, U, k=3):
    basis = [s for s in itertools.product(range(N + 1), repeat=L) if sum(s) == N]; idx = {s: i for i, s in enumerate(basis)}
    D = len(basis); H = lil_matrix((D, D))
    for i, s in enumerate(basis):
        H[i, i] = 0.5*U*sum(n*(n - 1) for n in s)
        for a in range(L):
            b = (a + 1) % L
            if L == 2 and a == 1: break
            for x, y in ((a, b), (b, a)):
                if s[y] > 0:
                    t = list(s); amp = math.sqrt(s[y]*(s[x] + 1)); t[y] -= 1; t[x] += 1
                    H[idx[tuple(t)], i] += -J*amp
    if D <= k + 2: return np.linalg.eigvalsh(H.toarray())[:k], D
    return np.sort(eigsh(H.tocsr(), k=k, which='SA', tol=1e-12)[0]), D
