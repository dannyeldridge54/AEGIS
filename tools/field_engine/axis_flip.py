"""D2261: what the mirror geometry forces at rho and i (see PREREG_D2261)."""
import json, sys, math
sys.path.insert(0, 'tools/serapis_calc')
import mpmath as mp
from eisenstein import E_fourier
import shapes
mp.mp.dps = 30
def Ef(x, y, s): return mp.mpf(E_fourier(x, y, s, nmax=30)) if False else _E(x, y, s)
def _E(x, y, s, nmax=30):
    x, y, s = mp.mpf(x), mp.mpf(y), mp.mpf(s)
    xi = lambda t: mp.pi**(-t/2)*mp.gamma(t/2)*mp.zeta(t)
    v = y**s + xi(2*s-1)/xi(2*s)*y**(1-s)
    for n in range(1, nmax+1):
        sig = sum(mp.mpf(d)**(1-2*s) for d in range(1, n+1) if n % d == 0)
        v += 4*mp.sqrt(y)/xi(2*s)*mp.mpf(n)**(s-0.5)*sig*mp.besselk(s-0.5, 2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return v
pts = {'rho': (mp.mpf(-0.5), mp.sqrt(3)/2), 'i': (mp.mpf(0), mp.mpf(1))}
out = {}
for name, (x0, y0) in pts.items():
    for s in (2, mp.mpf(3)/2):
        f = lambda x, y: _E(x, y, s)
        E0 = f(x0, y0)
        gx = mp.diff(f, (x0, y0), (1, 0)); gy = mp.diff(f, (x0, y0), (0, 1))
        xx = mp.diff(f, (x0, y0), (2, 0)); yy = mp.diff(f, (x0, y0), (0, 2)); xy = mp.diff(f, (x0, y0), (1, 1))
        lap = y0**2*(xx+yy)/E0
        # finite-difference check on scipy shapes.E (different normalisation: ratios only)
        h = 1e-4; U = complex(float(x0), float(y0)); g = lambda a, b: shapes.E(complex(a, b), float(s))
        a, b = U.real, U.imag; e0 = g(a, b)
        fxx = (g(a+h, b)-2*e0+g(a-h, b))/h**2; fyy = (g(a, b+h)-2*e0+g(a, b-h))/h**2
        fxy = (g(a+h, b+h)-g(a+h, b-h)-g(a-h, b+h)+g(a-h, b-h))/(4*h*h)
        key = f"{name}_s{float(s)}"
        out[key] = dict(grad_rel=float(mp.sqrt(gx**2+gy**2)*y0/E0), Exy_rel=float(abs(xy)*y0**2/E0),
                        lap_over_s_sminus1=float(lap/(s*(s-1))), yyExx_over_E=float(y0**2*xx/E0), yyEyy_over_E=float(y0**2*yy/E0),
                        A=float(xx/yy), A_fd=float(fxx/fyy), Exy_fd_rel=abs(fxy)*b**2/e0, half_s_sminus1=float(s*(s-1)/2))
json.dump(out, open('field_tests/results/d2261_axis_flip.json', 'w'), indent=1)
for k, v in out.items(): print(k, {a: (round(b, 10) if isinstance(b, float) else b) for a, b in v.items()})
