"""D985 (locked PREREG_D985): Level S3 — Möbius-amplitude mass of an anti-D5 position scalar with the full open-string tower."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.special import kv
from scipy.integrate import quad
from tools.serapis_calc import strings as S
from tools.serapis_calc.eisenstein import E_paper
NM = 40
LEV = [(m2, dn + dr) for (m2, dn), (_, dr) in zip(S.levels('NS', NM), S.levels('R', NM))]
def F_levels(L, U, N=60):
    e1, e2, f1, f2, A = S.lattice(L, U)
    m = np.arange(-N, N+1); M, Nn = np.meshgrid(m, m)
    W = M[..., None]*e1 + Nn[..., None]*e2; w = np.sqrt((W**2).sum(-1)); w[N, N] = np.inf
    tot = 0.0
    for m2, d in LEV:
        sgn = (-1)**int(round(m2))
        x = math.sqrt(m2)*w
        g = np.ones_like(w) if m2 == 0 else np.where(np.isfinite(x), x**2*kv(2, np.minimum(x, 700))/2, 0.0)
        tot += sgn*d*(g/w**4).sum()
    return tot, A
def hat_trace(t, nmax=400):
    if t > 60: return 16.0 - 256*math.exp(-t)      # massless 8+8 plus first level; further terms < 1e-49 relative
    n = np.arange(1, nmax+1); x = 1j*math.exp(-t/2)
    D = np.prod((1 - x**(2*n))**8)
    ns = (np.prod((1 + x**(2*n-1))**8) - np.prod((1 - x**(2*n-1))**8))/(2*x*D)
    q = -math.exp(-t); r = 8*np.prod((1 + q**n)**8)/np.prod((1 - q**n)**8)
    return (ns + r).real
def F_theta(L, U, N=8):
    e1, e2, f1, f2, A = S.lattice(L, U); tot = 0.0
    for a in range(-N, N+1):
        for b in range(-N, N+1):
            if a == 0 and b == 0: continue
            wv = a*e1 + b*e2; w2 = float(wv @ wv); ts = w2/8
            g = lambda t: math.exp(-w2/(4*t))*hat_trace(t)/t**3
            tlo = max(0.05, w2/(4*600))      # below tlo the integrand is < e^-600 x (Hagedorn growth), set to 0
            cuts = sorted({tlo} | {c for c in (ts/10, ts/3, ts, 3*ts, 10*ts, 100*ts) if c > tlo})
            I = sum(quad(g, lo, hi, limit=300, epsrel=1e-11)[0] for lo, hi in zip(cuts[:-1], cuts[1:]) if hi > lo) + quad(g, cuts[-1], np.inf, limit=300)[0]
            tot += I/16.0      # int dt t^-3 e^{-w^2/4t} = 16/|w|^4 per massless state: normalise to the level-sum convention
    return tot, A
L_ = []
ok_route = True; signs = True; shape12 = True; shape16 = True
L_.append(f"hat trace at t=200 (massless 8+8, same sign): {hat_trace(200):.6f}; first levels (M^2, (-1)^N d): {[(m2, (-1)**int(m2)*d) for m2, d in LEV[:4]]}")
for L in (10.0, 12.0, 16.0):
    for U in (1j, complex(0.5, 3**0.5/2), complex(0.2, 1.3)):
        Fl, A = F_levels(L, U, N=8); Ft, _ = F_theta(L, U, N=8)
        Fc, _ = F_levels(L, U, N=60)
        fe = 16*E_paper(U.real, U.imag)/A**2
        rr = abs(Ft/Fl - 1); ok_route &= rr < 5e-4; signs &= Fc > 0
        if L == 12.0: shape12 &= abs(Fc/fe - 1) < 0.10
        if L == 16.0: shape16 &= abs(Fc/fe - 1) < 0.01
        L_.append(f"L={L} U={U}: F_levels(N=8)={Fl:.10e} F_theta(N=8)={Ft:.10e} rel {Ft/Fl-1:.1e} | F(converged)={Fc:.8e} vs 16 E(U,2)/A^2={fe:.8e} ratio {Fc/fe:.5f}")
        print(L_[-1], flush=True)
if not ok_route: v = 'ROUTES DISAGREE (no verdict)'
elif not signs: v = 'SIGN FAIL'
elif not (shape12 and shape16): v = 'SHAPE FAIL'
else: v = 'PASS: string-level sign confirmed positive, U-dependence E(U,2)'
L_.append(f"routes agree: {ok_route}; F>0 everywhere: {signs}; shape L=12: {shape12}; shape L=16: {shape16} -> {v}")
open('field_tests/results/s3_mobius_d985.txt', 'w').write('\n'.join(L_)+'\n'); print(L_[-1])
