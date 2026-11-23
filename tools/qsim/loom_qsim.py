"""Loom quantum-lattice simulator (D2183, TOOL). hbar = 1.
Q1 exact spin-1 single-mode (SMA) dynamics, M=0 sector.
Q2 mean-field spin-1 lattice (L sites, hopping J, spin coupling c, quadratic Zeeman q), RK4; L=1 is the large-N limit of Q1.
Q3 exact scalar Bose-Hubbard chain (periodic).
Q4 Loom compass: log-sensitivity of observables to dials + balance readout."""
import itertools, math, json
import numpy as np
from math import lgamma
# ---------------- Q1: exact SMA, M = 0 sector; basis k = pairs in (+1,-1), N0 = N - 2k
def sma_hamiltonian(N, c, q):
    K = N//2 + 1; H = np.zeros((K, K))
    for k in range(K):
        N0 = N - 2*k
        H[k, k] = (c/(2*N))*(2*N0 - 1)*(N - N0) - q*N0
        if k + 1 < K:   # a1+ a-1+ a0 a0 |N0,k> = sqrt(N0(N0-1)) (k+1) |N0-2,k+1>
            v = (c/(2*N))*2*math.sqrt(N0*(N0 - 1))*(k + 1)
            H[k + 1, k] = v; H[k, k + 1] = v
    return H
def sma_coherent(N, zeta):
    z1, z0, zm = zeta; K = N//2 + 1; a = np.zeros(K, complex)
    for k in range(K):
        N0 = N - 2*k
        lg = 0.5*(lgamma(N + 1) - lgamma(N0 + 1) - 2*lgamma(k + 1))
        a[k] = np.exp(lg + N0*np.log(abs(z0)) + k*np.log(abs(z1*zm)) + 1j*(N0*np.angle(z0) + k*np.angle(z1*zm)))
    return a/np.linalg.norm(a)
def sma_rho0(N, c, q, zeta, ts):
    H = sma_hamiltonian(N, c, q); w, V = np.linalg.eigh(H); a0 = V.conj().T @ sma_coherent(N, zeta)
    n0 = np.array([N - 2*k for k in range(N//2 + 1)])/N
    out = []
    for t in ts:
        psi = V @ (np.exp(-1j*w*t)*a0); out.append(float(np.sum(n0*abs(psi)**2)))
    return np.array(out), H
# ---------------- Q2: mean-field spin-1 lattice. psi shape (L,3) for m = +1, 0, -1; sum |psi|^2 = Ntot
def mf_energy(psi, c, q, J, nbar):
    p1, p0, pm = psi[:, 0], psi[:, 1], psi[:, 2]
    e_int = (c/nbar)*np.sum(abs(p0)**2*(abs(p1)**2 + abs(pm)**2) + 2*np.real(np.conj(p1)*np.conj(pm)*p0**2))
    e_q = -q*np.sum(abs(p0)**2)
    e_hop = -J*np.sum(2*np.real(np.conj(psi)*np.roll(psi, -1, axis=0))) if psi.shape[0] > 1 else 0.0
    return float(e_int + e_q + e_hop)
def mf_rhs(psi, c, q, J, nbar):
    p1, p0, pm = psi[:, 0], psi[:, 1], psi[:, 2]; d = np.zeros_like(psi)
    d[:, 0] = (c/nbar)*(abs(p0)**2*p1 + np.conj(pm)*p0**2)
    d[:, 1] = (c/nbar)*(p0*(abs(p1)**2 + abs(pm)**2) + 2*p1*pm*np.conj(p0)) - q*p0
    d[:, 2] = (c/nbar)*(abs(p0)**2*pm + np.conj(p1)*p0**2)
    if psi.shape[0] > 1: d += -J*(np.roll(psi, 1, axis=0) + np.roll(psi, -1, axis=0))
    return -1j*d
def mf_run(psi, c, q, J, ts, dt=1e-3):
    nbar = float(np.sum(abs(psi)**2))/psi.shape[0]; t = 0.0; out = []; i = 0
    for T in ts:
        while t < T - 1e-12:
            h = min(dt, T - t)
            k1 = mf_rhs(psi, c, q, J, nbar); k2 = mf_rhs(psi + 0.5*h*k1, c, q, J, nbar)
            k3 = mf_rhs(psi + 0.5*h*k2, c, q, J, nbar); k4 = mf_rhs(psi + h*k3, c, q, J, nbar)
            psi = psi + (h/6)*(k1 + 2*k2 + 2*k3 + k4); t += h
        out.append(psi.copy())
    return out, nbar
# ---------------- Q3: exact scalar Bose-Hubbard chain
def bh_spectrum(L, N, J, U, k=3):
    basis = [s for s in itertools.product(range(N + 1), repeat=L) if sum(s) == N]; idx = {s: i for i, s in enumerate(basis)}
    D = len(basis); H = np.zeros((D, D))
    for i, s in enumerate(basis):
        H[i, i] = 0.5*U*sum(n*(n - 1) for n in s)
        for a in range(L):
            b = (a + 1) % L
            if L == 2 and a == 1: break
            for x, y in ((a, b), (b, a)):   # b_x^+ b_y
                if s[y] > 0:
                    t = list(s); amp = math.sqrt(s[y]*(s[x] + 1)); t[y] -= 1; t[x] += 1
                    H[idx[tuple(t)], i] += -J*amp
    return np.linalg.eigvalsh(H)[:k], D
# ---------------- Q4: Loom compass
def osc_obs(c, q, rho0=0.5, phi=0.5, T=12.0, n=1200):
    z = np.array([math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2), math.sqrt(rho0), math.sqrt((1 - rho0)/2)*np.exp(1j*phi/2)])
    ts = np.linspace(0, T, n + 1)[1:]; out, _ = mf_run(z[None, :].copy(), c, q, 0.0, ts, dt=2e-3)
    r = np.array([abs(p[0, 1])**2 for p in out]); amp = float(r.max() - r.min())
    y = r - r.mean(); i = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    cross = ts[i] + (ts[i + 1] - ts[i])*(-y[i])/(y[i + 1] - y[i])   # linear interpolation of upward crossings
    period = float(np.mean(np.diff(cross))) if len(cross) > 2 else float('nan')
    return dict(period=period, amplitude=amp)
def compass(f, dials, eps=1e-2):
    base = f(**dials); J = {}
    for k, v in dials.items():
        up = dict(dials); up[k] = v*(1 + eps); dn = dict(dials); dn[k] = v*(1 - eps)
        fu, fd = f(**up), f(**dn)
        J[k] = {o: (math.log(abs(fu[o])) - math.log(abs(fd[o])))/(2*eps) if fu[o] and fd[o] else float('nan') for o in base}
    balance = {o: max(J, key=lambda k: abs(J[k][o])) for o in base}
    return dict(base=base, log_sensitivity=J, dominant_dial=balance)
