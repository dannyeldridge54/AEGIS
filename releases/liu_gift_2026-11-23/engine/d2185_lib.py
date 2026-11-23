"""D2185: Liu-lab open questions. Exact spin-1 single-mode dynamics with their static Floquet H (q_B -> inf):
H/(h c2) = (1/N)[N0(N-N0) + 1/2 (N+-N-)^2] - (p/2) S_y,  p = p_perp/c2;  time in units of 1/c2, U(t) = exp(-2 pi i H t)."""
import sys, math, json, time
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import expm_multiply
from math import lgamma
sys.path.insert(0, 'tools/qsim'); from loom_qsim import mf_run
def basis(N):
    B = [(a, N - a - b, b) for a in range(N + 1) for b in range(N + 1 - a)]   # (n+, n0, n-)
    return B, {s: i for i, s in enumerate(B)}
def ham(N, p):
    B, I = basis(N); D = len(B); rows, cols, vals = [], [], []
    for i, (a, z, b) in enumerate(B):
        rows.append(i); cols.append(i); vals.append((z*(N - z) + 0.5*(a - b)**2)/N)
        # S+ = sqrt2 (a+^ a0 + a0^ a-); S_y = (S+ - S-)/(2i); add -(p/2) S_y
        for (src, dst, amp) in ((1, 0, math.sqrt(2*z*(a + 1)) if z > 0 else 0), (2, 1, math.sqrt(2*b*(z + 1)) if b > 0 else 0)):
            if amp == 0: continue
            t = [a, z, b]; t[src] -= 1; t[dst] += 1; j = I[tuple(t)]   # S+ |i> -> amp |j>
            # matrix of S_y: <j|S_y|i> = amp/(2i), <i|S_y|j> = -amp/(2i)
            rows += [j, i]; cols += [i, j]; vals += [-(p/2)*amp/(2j), -(p/2)*(-amp)/(2j)]
    H = sp.csr_matrix((np.array(vals, complex), (rows, cols)), shape=(D, D)); return H, B
def coherent(B, N, zp, z0, zm):
    v = np.zeros(len(B), complex)
    for i, (a, z, b) in enumerate(B):
        lg = 0.5*(lgamma(N + 1) - lgamma(a + 1) - lgamma(z + 1) - lgamma(b + 1))
        mag = lg + (a*math.log(abs(zp)) if a else 0) + (z*math.log(abs(z0)) if z else 0) + (b*math.log(abs(zm)) if b else 0)
        v[i] = math.exp(mag)*np.exp(1j*(a*np.angle(zp) + z*np.angle(z0) + b*np.angle(zm)))
    return v/np.linalg.norm(v)
def fock(B, N, rho0, M):
    z = round(rho0*N); m = round(M*N); a = (N - z + m)//2; b = N - z - a
    v = np.zeros(len(B), complex); v[B.index((a, z, b))] = 1; return v
def evolve(H, v, ts):
    return expm_multiply(-2j*math.pi*H, v, start=ts[0], stop=ts[-1], num=len(ts), endpoint=True)
