"""Lattice Lab — one tool for the lattice web (Danny 2026-11-18: "make a tool that does this in the cloud for us").
Every result here was validated in D1276–D1291 (exact enumeration, Poisson, modular forms).

Lattices by name: Z<n>, A<n>, A<n>*, D<n>, D<n>*, D16+, E6, E6*, E7, E7*, E8, E8xE8, hex, square, FCC, BCC, Leech,
or a Gram matrix as JSON (e.g. '[[2,1],[1,2]]'), or tau=x+iy (2D torus shape).

Commands (python3 tools/lattice/lattice_lab.py <cmd> ...):
  shells  L [Q]            vector counts per norm, |v|^2 <= Q (unit covolume)
  energy  L [alphas]       Gaussian energy theta(alpha)-1; alpha<1 via Poisson with the dual
  flip    L                does L hand over to its dual with scale? (self-Poisson gap at alpha=1.25)
  compare L1 L2 ...        winner at each alpha (same dimension)
  champion d               best of the standard families in dimension d at each alpha
  modular L                compare shells with E4, E4^2, E4^3-720Delta when d = 8, 16, 24
  epstein L s              Epstein zeta via the Mellin transform of the energy
  critical [alpha]         scan the 2D fundamental domain for critical points of the energy
  explore                  run the whole battery over all named lattices, print a findings table
Output is JSON (one line) unless --text.
"""
import json, math, sys, itertools
import numpy as np

# ---------------- lattice constructors (Gram matrices) ----------------
def _A(n):
    C = 2*np.eye(n)
    for i in range(n-1): C[i, i+1] = C[i+1, i] = -1
    return C
def _D(n):
    C = _A(n); C[n-2, n-1] = C[n-1, n-2] = 0; C[n-3, n-1] = C[n-1, n-3] = -1
    return C
def _E(n):
    C = 2*np.eye(n)
    for i, j in [(1, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4)]:
        if i <= n and j <= n: C[i-1, j-1] = C[j-1, i-1] = -1
    return C
def _D16p():
    B = np.zeros((16, 16))
    for i in range(15): B[i, i] = 1; B[i, i+1] = -1
    B[15, 14] = B[15, 15] = 1; B[0, :] = 0.5
    return B @ B.T
def _leech():
    from fpylll import IntegerMatrix, LLL
    Q = {(x*x) % 23 for x in range(1, 23)}; g = np.zeros(23, int); g[0] = 1
    for q in Q: g[q] = 1
    M = np.array([np.roll(g, k) for k in range(23)]) % 2
    A = M.copy(); r = 0
    for c in range(23):
        p = next((i for i in range(r, 23) if A[i, c]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(23):
            if i != r and A[i, c]: A[i] ^= A[r]
        r += 1
    Bc = np.hstack([A[:r], (A[:r].sum(1) % 2)[:, None]])
    G = [2*w for w in Bc]
    for i in range(24):
        for j in range(i+1, 24):
            v = np.zeros(24, int); v[i] = 4; v[j] = 4; G.append(v); v = v.copy(); v[j] = -4; G.append(v)
    v = np.ones(24, int); v[0] = -3; G.append(v)
    M = IntegerMatrix.from_matrix([list(map(int, x)) for x in G]); LLL.reduction(M)
    B = np.array([[M[i, j] for j in range(24)] for i in range(M.nrows)]); B = B[np.any(B != 0, axis=1)]
    return (B @ B.T) / 8.0

def gram(name):
    s = str(name).strip()
    if s.startswith('['): return np.array(json.loads(s), float)
    if s.startswith('tau='):
        t = complex(s[4:].replace('i', 'j')); return np.array([[1, t.real], [t.real, abs(t)**2]], float)
    dual = s.endswith('*'); b = s.rstrip('*')
    fixed = {'hex': np.array([[2., 1], [1, 2]]), 'square': np.eye(2), 'FCC': _A(3), 'BCC': np.linalg.inv(_A(3)),
             'D16+': None, 'E8xE8': None, 'Leech': None}
    if b == 'D16+': G = _D16p()
    elif b == 'E8xE8': G = np.zeros((16, 16)); G[:8, :8] = _E(8); G[8:, 8:] = _E(8)
    elif b == 'Leech': G = _leech()
    elif b in fixed: G = fixed[b]
    else:
        fam, n = b[0], int(b[1:])
        G = {'Z': lambda n: np.eye(n), 'A': _A, 'D': _D, 'E': _E}[fam](n)
    return np.linalg.inv(G) if dual else G

def unit(G): return G / np.linalg.det(G)**(1/len(G))

# ---------------- exact enumeration (Fincke–Pohst) ----------------
def norms(G, Q):
    n = len(G); R = np.linalg.cholesky(G).T; out = []; x = np.zeros(n)
    def rec(k, rem):
        c = -sum(R[k, j]*x[j] for j in range(k+1, n))/R[k, k]; w = math.sqrt(max(rem, 0))/abs(R[k, k])
        for v in range(math.ceil(c-w-1e-12), math.floor(c+w+1e-12)+1):
            x[k] = v; t = R[k, k]*(v-c); r2 = rem - t*t
            if r2 < -1e-9: continue
            if k == 0: out.append(Q - r2)
            else: rec(k-1, r2)
        x[k] = 0
    rec(n-1, Q); return np.array(out)

def _Q_for(d): return 12.0 if d <= 8 else (6.0 if d <= 16 else 4.0)

def shells(L, Q=None):
    G = unit(gram(L)); Q = Q or _Q_for(len(G)); q = norms(G, Q+1e-6)
    v, c = np.unique(np.round(q, 6), return_counts=True)
    return {'lattice': L, 'd': len(G), 'Q': Q, 'shells': {f'{a:.6g}': int(b) for a, b in zip(v, c)}}

def energy(L, alphas=(0.5, 0.8, 1.0, 1.25, 2.0)):
    G = unit(gram(L)); d = len(G); Q = _Q_for(d)
    qL = norms(G, Q); qD = norms(unit(np.linalg.inv(G)), Q)
    out = {}
    for a in alphas:
        if a >= 1: out[a] = float(np.exp(-np.pi*a*qL).sum() - 1)
        else: out[a] = float(a**(-d/2)*np.exp(-np.pi*qD/a).sum() - 1)   # Poisson: theta_L(a) = a^{-d/2} theta_{L*}(1/a)
    return {'lattice': L, 'd': d, 'energy': out}

def flip(L):
    G = unit(gram(L)); d = len(G); Q = _Q_for(d)
    t = lambda M, a: np.exp(-np.pi*a*norms(unit(M), Q)).sum()
    gap = t(G, 1.25) - t(np.linalg.inv(G), 1.25)
    return {'lattice': L, 'd': d, 'L_minus_dual_at_1.25': float(gap), 'self_dual': bool(abs(gap) < 1e-9),
            'flips': bool(abs(gap) >= 1e-9), 'rule': 'a lattice hands over to its dual at alpha=1 iff it is not self-dual (D1278, D1291)'}

def compare(*Ls, alphas=(0.5, 0.8, 1.0, 1.25, 2.0)):
    E = {L: energy(L, alphas)['energy'] for L in Ls}
    return {'alphas': list(alphas), 'energy': E, 'winner': {a: min(Ls, key=lambda L: E[L][a]) for a in alphas}}

CHAMPS = {2: ['hex', 'square'], 3: ['FCC', 'BCC', 'Z3'], 4: ['D4', 'Z4', 'A4', 'A4*'], 5: ['D5', 'D5*', 'A5', 'A5*', 'Z5'],
          6: ['E6', 'E6*', 'D6', 'D6*', 'A6', 'A6*', 'Z6'], 7: ['E7', 'E7*', 'D7', 'D7*', 'A7', 'A7*', 'Z7'],
          8: ['E8', 'D8', 'D8*', 'A8', 'Z8'], 16: ['E8xE8', 'D16+', 'D16', 'Z16'], 24: ['Leech']}
def champion(d): return compare(*CHAMPS[int(d)])

def modular(L):
    G = unit(gram(L)); d = len(G); N = 6
    def sig3(n): return sum(k**3 for k in range(1, n+1) if n % k == 0)
    E4 = [1] + [240*sig3(n) for n in range(1, N+1)]
    mul = lambda a, b: [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(min(len(a), len(b)))]
    P = [1] + [0]*N
    for n in range(1, N+1):
        for _ in range(24): P = [P[k] - (P[k-n] if k >= n else 0) for k in range(N+1)]
    Dl = [0] + P[:N]; E8f = mul(E4, E4); E12 = mul(E8f, E4)
    form = {8: ('E4', E4), 16: ('E4^2', E8f), 24: ('E4^3-720*Delta', [E12[k]-720*Dl[k] for k in range(N+1)])}.get(d)
    if not form: return {'lattice': L, 'd': d, 'note': 'only d = 8, 16, 24 have a one-form answer here'}
    q = norms(G, _Q_for(d)+1e-6); v, c = np.unique(np.round(q).astype(int), return_counts=True); sh = dict(zip(v.tolist(), c.tolist()))
    kmax = int(_Q_for(d)//2)
    got = [sh.get(2*k, 0) for k in range(kmax+1)]
    return {'lattice': L, 'd': d, 'form': form[0], 'form_coeffs': form[1][:kmax+1], 'shells': got, 'match': got == form[1][:kmax+1]}

def epstein(L, s):
    """Analytically continued Epstein zeta at unit covolume (valid for all s except 0, d/2):
    pi^-s Gamma(s) Z_L(s) = Int_1^inf (theta_L-1) a^(s-1) + Int_1^inf (theta_L*-1) a^(d/2-s-1) - 1/s - 1/(d/2-s)."""
    from scipy.integrate import quad
    G = unit(gram(L)); d = len(G); s = float(s); Q = 40.0 if d == 2 else max(_Q_for(d), 12.0 if d <= 8 else _Q_for(d))
    qL = norms(G, Q); qL = qL[qL > 1e-12]; qD = norms(unit(np.linalg.inv(G)), Q); qD = qD[qD > 1e-12]
    th = lambda a, q: np.exp(-np.pi*a*q).sum()
    I1 = quad(lambda a: th(a, qL)*a**(s-1), 1, np.inf, limit=200)[0]
    I2 = quad(lambda a: th(a, qD)*a**(d/2-s-1), 1, np.inf, limit=200)[0]
    lam = I1 + I2 - 1/s - 1/(d/2-s)
    return {'lattice': L, 'd': d, 's': s, 'epstein': math.pi**s/math.gamma(s)*lam,
            'method': 'analytic continuation via Mellin + Poisson (D1291, D1293)'}

def _E2d(x, y, a=1.0):
    G = np.array([[1, x], [x, x*x+y*y]])/y; q = norms(G, 30.0/a); return np.exp(-np.pi*a*q).sum()-1
def critical(alpha=1.0, n=40):
    """Grid over the fundamental domain (x in [0, 1/2] by the x -> -x symmetry, |tau| >= 1, y <= 3), take local minima of the
    hyperbolic gradient norm, refine each with Nelder-Mead, keep those with |grad| < 1e-6; classify with the Hessian."""
    from scipy.optimize import minimize
    a = float(alpha); h = 1e-5
    def grad(x, y):
        gx = (_E2d(x+h, y, a)-_E2d(x-h, y, a))/(2*h); gy = (_E2d(x, y+h, a)-_E2d(x, y-h, a))/(2*h); return gx, gy
    def g(p):
        x, y = p
        if y <= 0.3: return 1e3
        gx, gy = grad(x, y); return y*y*math.hypot(gx, gy)
    xs = np.linspace(0, 0.5, n//2+1); ys = np.linspace(math.sqrt(3)/2, 3.0, n)
    Gd = np.full((len(xs), len(ys)), np.inf)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if x*x+y*y >= 1-1e-9: Gd[i, j] = g((x, y))
    seeds = []
    for i in range(len(xs)):
        for j in range(len(ys)):
            nb = Gd[max(0, i-1):i+2, max(0, j-1):j+2]
            if np.isfinite(Gd[i, j]) and Gd[i, j] <= nb.min(): seeds.append((xs[i], ys[j]))
    pts = []
    for s0 in seeds:
        r = minimize(g, s0, method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-13, 'maxiter': 600})
        x, y = r.x; x = abs(x) % 1.0; x = min(x, 1-x)
        if r.fun < 1e-6 and y > 0.5 and not any(abs(x-q[0]) < 1e-3 and abs(y-q[1]) < 1e-3 for q in pts):
            H = np.array([[_E2d(x+h, y, a)-2*_E2d(x, y, a)+_E2d(x-h, y, a), 0], [0, _E2d(x, y+h, a)-2*_E2d(x, y, a)+_E2d(x, y-h, a)]])/h**2
            H[0, 1] = H[1, 0] = (_E2d(x+h, y+h, a)-_E2d(x+h, y-h, a)-_E2d(x-h, y+h, a)+_E2d(x-h, y-h, a))/(4*h*h)
            ev = np.linalg.eigvalsh(H)
            pts.append((round(x, 6), round(y, 6), float(r.fun), 'minimum' if ev.min() > 0 else ('saddle' if ev.max() > 0 else 'maximum')))
    return {'alpha': a, 'seeds': len(seeds), 'critical_points': [{'x': p[0], 'y': p[1], 'grad': p[2], 'type': p[3]} for p in pts],
            'expected': 'tau=i (0,1) saddle and tau=rho (0.5,0.866) minimum only (D1279, D1292)'}

def explore():
    rows = []
    for d, Ls in CHAMPS.items():
        if d == 24:
            rows.append({'d': 24, 'winner_all_scales': 'Leech', 'self_dual': True}); continue
        c = champion(d); w = c['winner']
        rows.append({'d': d, 'winner_alpha<1': w[0.5], 'winner_alpha>1': w[2.0],
                     'hands_over': w[0.5] != w[2.0]})
    return {'champions': rows}

CMDS = dict(shells=shells, energy=energy, flip=flip, compare=compare, champion=champion, modular=modular,
            epstein=epstein, critical=critical, explore=explore)

def main(argv):
    if not argv or argv[0] not in CMDS: print(__doc__); return
    text = '--text' in argv; argv = [a for a in argv if a != '--text']
    cmd, args = argv[0], argv[1:]
    if cmd == 'shells' and len(args) > 1: args = [args[0], float(args[1])]
    if cmd == 'energy' and len(args) > 1: args = [args[0], [float(a) for a in args[1].split(',')]]
    if cmd == 'critical' and args: args = [float(args[0])]
    r = CMDS[cmd](*args)
    print(json.dumps(r, indent=1 if text else None, default=str))

if __name__ == '__main__': main(sys.argv[1:])
