"""N3 (locked PREREG_N3_slowroll_third)."""
import sys, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
src = open('theory/janus/j7m_grid.py').read(); exec(src.split("L = []; D = {k:")[0])
from numpy.polynomial import chebyshev as Ch
C = 0.5772156649015329 + math.log(2) - 2; pi2 = math.pi**2
def eps_at(bg, Np, deg):
    a, b = Np - 1.5, Np + 1.5; x = np.cos(np.pi*(np.arange(41) + 0.5)/41); N = 0.5*(a + b) + 0.5*(b - a)*x
    le = np.array([math.log(bg.state(n)[2]) for n in N]); c = Ch.chebfit(x, le, deg); s = 2.0/(b - a)
    d = [Ch.chebval(0.0, Ch.chebder(c, m))*s**m for m in range(1, 5)]   # derivatives of ln eps1 at Np (x=0)
    e1 = bg.state(Np)[2]; e2 = d[0]; e3 = d[1]/e2; e4 = (d[2]/e2 - e3**2)/e3   # e3 = (ln e2)', e4 = (ln e3)'
    return e1, e2, e3, e4
def ns(e1, e2, e3, e4):
    n1 = -2*e1 - e2; n2 = -2*e1**2 - (2*C + 3)*e1*e2 - C*e2*e3
    n3 = (-2*e1**3 + (pi2 - 6*C - 15)*e1**2*e2 + (7*pi2 - 12*C**2 - 36*C - 84)/12*e1*e2**2 + (7*pi2/12 - C**2 - 4*C - 6)*e1*e2*e3
          + (pi2 - 12*C**2)/24*e2*e3**2 + (pi2/4 - 2)*e2**2*e3 + (pi2 - 12*C**2)/24*e2*e3*e4)
    return 1 + n1 + n2, 1 + n1 + n2 + n3
L = []; D2 = []; D3 = []; N2 = []; N3n = []
for i in range(1, 13):
    try: name, V, dV, y0, m = build(i); bg = Background(V, dV, y0, Nmax=4000)
    except Exception as e: continue
    for Ns in (50.0, 60.0):
        Np = bg.Nend - Ns; ex = spectra_fast(bg, Ns, dlnk=DL, bd=1000.0)['ns']; exn = spectra_fast(bg, Ns, dlnk=tuple(np.linspace(-.25, .25, 9)), bd=1000.0)['ns']
        e = eps_at(bg, Np, 12); s2, s3 = ns(*e); s3b = ns(*eps_at(bg, Np, 10))[1]
        if abs(s3 - s3b) > 1e-8: L.append(f"{name} N*={Ns:.0f}: listed (fit check {abs(s3-s3b):.1e})"); continue
        D2.append(abs(s2 - ex)); D3.append(abs(s3 - ex)); N2.append(abs(s2 - exn)); N3n.append(abs(s3 - exn))
        L.append(f"{name:16s} N*={Ns:.0f} eps=({e[0]:.2e},{e[1]:.2e},{e[2]:.2e},{e[3]:.2e}) exact {ex:.8f} | D2 {D2[-1]:.1e} D3 {D3[-1]:.1e} | narrow fit: D2 {N2[-1]:.1e} D3 {N3n[-1]:.1e}")
        print(L[-1], flush=True)
md = np.median; nb = sum(a < b for a, b in zip(D3, D2))
ok = bool(md(D3) <= md(D2)/3 and nb >= 12)
L.append(f"{len(D2)} points; D3 < D2 on {nb}; median D2 {md(D2):.2e}, D3 {md(D3):.2e} | narrow (reported only): median D2 {md(N2):.2e}, D3 {md(N3n):.2e}, D3<D2 on {sum(a < b for a, b in zip(N3n, N2))}")
L.append("N3: " + ("N3LO n_s CONFIRMED (coefficients consistent)" if ok else "NOT CONFIRMED"))
open('field_tests/results/n3_slowroll.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-2:]))
