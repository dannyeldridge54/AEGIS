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
def ustate(B, N): return coherent(B, N, math.sqrt(0.2)*np.exp(1j*math.pi/2), math.sqrt(0.6), math.sqrt(0.2)*np.exp(1j*math.pi/2))   # rho0 .6, M 0, theta pi, eta 0
R = {}
# ---- G3 validation
chk = {}
H, B = ham(6, 0.5); chk['herm'] = float(abs(H - H.getH()).max())
N = 6; v = coherent(B, N, 1, 1e-12, 1e-12)   # fully stretched m=+1
Sy = (H - ham(6, 0.0)[0])*(-2/0.5); Sy2 = (Sy @ (Sy @ v)); chk['Sy2_stretched'] = float(np.real(np.vdot(v, Sy2))); chk['Sy2_expect'] = N/2
def beta_of(qc, T=30.0):
    r0 = 0.45; z = np.array([math.sqrt((1 - r0)/2), math.sqrt(r0), math.sqrt((1 - r0)/2)], complex)
    ts = np.linspace(0, T, 3001)[1:]; out, _ = mf_run(z[None, :].copy(), 2*math.pi*1.0, 2*math.pi*qc, 0.0, ts, dt=1e-3)
    th = np.unwrap(np.array([np.angle(p[0, 0]) + np.angle(p[0, 2]) - 2*np.angle(p[0, 1]) for p in out]))
    c = np.cos(th/2); return float(2 - (c.max() - c.min()))
qcs = np.round(np.arange(0.80, 1.21, 0.01), 3); betas = [beta_of(x) for x in qcs]
qt = float(qcs[next(i for i, b in enumerate(betas) if b < 0.05)]) if any(b < 0.05 for b in betas) else float('nan')
R['G3'] = dict(checks=chk, q_over_c2=qcs.tolist(), beta=betas, transition=qt, pass_=bool(abs(qt - 2*(1-0.45)) < 0.02 and chk['herm'] < 1e-12 and abs(chk['Sy2_stretched'] - chk['Sy2_expect']) < 1e-9))
print('G3', R['G3']['transition'], R['G3']['checks'], R['G3']['pass_'], flush=True)
if not R['G3']['pass_']:
    json.dump(R, open('field_tests/results/d2185_liu.json', 'w'), indent=1); sys.exit('G3 failed: stop')
# ---- G1 revival map
G1 = {}
ts = np.linspace(0, 200, 8001)
for p in (0.2, 0.33, 0.5):
    rows = []
    for N in (10, 20, 40, 60, 80, 100, 120, 160):
        t0 = time.time(); H, B = ham(N, p); v0 = ustate(B, N); V = evolve(H, v0, ts); F = np.abs(V @ v0.conj())**2
        imin = int(np.argmax(np.diff(np.sign(np.diff(F))) > 0)) + 1   # first local minimum
        Tr = None
        for k in range(imin + 1, len(F) - 1):
            if F[k] > F[k-1] and F[k] >= F[k+1] and F[k] > 0.1: Tr = float(ts[k]); Fr = float(F[k]); break
        rows.append(dict(N=N, T_rev=Tr, F_rev=(Fr if Tr else None), F_min=float(F[imin]), secs=round(time.time() - t0, 1)))
        print('G1', p, rows[-1], flush=True)
    good = [(r['N'], r['T_rev']) for r in rows if r['T_rev']]
    fit = None
    if len(good) >= 3:
        x = np.log([g[0] for g in good]); y = np.log([g[1] for g in good]); a, b = np.polyfit(x, y, 1); fit = dict(exponent=float(a), prefactor=float(math.exp(b)))
    G1[str(p)] = dict(rows=rows, powerlaw=fit)
R['G1'] = G1
# ---- G2 variance growth
G2 = {}; ts2 = np.linspace(0, 40, 801); p = 1/3
for name in ('R', 'U', 'C'):
    G2[name] = {}
    for N in (40, 80, 160):
        H, B = ham(N, p)
        v0 = ustate(B, N) if name == 'U' else fock(B, N, 0.0, -0.7) if name == 'R' else fock(B, N, 0.26, -0.3)
        V = evolve(H, v0, ts2); n0 = np.array([s[1] for s in B])/N; m = np.array([s[0] - s[2] for s in B])/N
        P = np.abs(V)**2; e0 = P @ n0; v0_ = P @ n0**2 - e0**2; eM = P @ m; vM = P @ m**2 - eM**2
        G2[name][str(N)] = dict(t=ts2[::40].tolist(), mean_rho0=e0[::40].tolist(), var_rho0=v0_[::40].tolist(), var_M=vM[::40].tolist(),
                                var_rho0_t40=float(v0_[-1]), var_M_t40=float(vM[-1]))
        print('G2', name, N, round(float(v0_[-1]), 5), round(float(vM[-1]), 5), flush=True)
R['G2'] = G2
json.dump(R, open('field_tests/results/d2185_liu.json', 'w'), indent=1); print('DONE')
