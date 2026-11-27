"""D2271: Zhinu modulus masses at rho and i (see PREREG_D2271)."""
import json, random
import mpmath as mp
mp.mp.dps = 30
def _E(x, y, s, nmax=30):
    x, y, s = mp.mpf(x), mp.mpf(y), mp.mpf(s)
    xi = lambda t: mp.pi**(-t/2)*mp.gamma(t/2)*mp.zeta(t)
    v = y**s + xi(2*s-1)/xi(2*s)*y**(1-s)
    for n in range(1, nmax+1):
        sig = sum(mp.mpf(d)**(1-2*s) for d in range(1, n+1) if n % d == 0)
        v += 4*mp.sqrt(y)/xi(2*s)*mp.mpf(n)**(s-0.5)*sig*mp.besselk(s-0.5, 2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return v
mp.mp.dps = 30
s = mp.mpf(3)/2
def lnE(x, y): return mp.log(_E(x, y, s))
def grad2(x, y):
    gx = mp.diff(lnE, (x, y), (1, 0)); gy = mp.diff(lnE, (x, y), (0, 1)); return y**2*(gx**2+gy**2)
def V(x, y): return mp.mpf(4)/9*grad2(x, y)          # V0/V_inf with a = 1/3, lambda^2 = 1/4
def lap(x, y): return y**2*(mp.diff(lnE, (x, y), (2, 0)) + mp.diff(lnE, (x, y), (0, 2)))
out = {}
for name, (x0, y0) in {'rho': (mp.mpf(-0.5), mp.sqrt(3)/2), 'i': (mp.mpf(0), mp.mpf(1))}.items():
    h = mp.mpf('1e-6'); f = lambda a, b: V(x0+a, y0+b)
    Hxx = (f(h,0)-2*f(0,0)+f(-h,0))/h**2; Hyy = (f(0,h)-2*f(0,0)+f(0,-h))/h**2
    Hxy = (f(h,h)-f(h,-h)-f(-h,h)+f(-h,-h))/(4*h*h)
    J2 = y0**2*2                                     # (d(x,y)/dphi)^2 for n = 1
    ev = sorted(mp.eig(mp.matrix([[Hxx,Hxy],[Hxy,Hyy]]))[0], key=lambda z: mp.re(z))
    out[name] = dict(V0=float(f(0,0)), m2_over_Vinf=[float(mp.re(v)*J2) for v in ev])
random.seed(1); res = []
for _ in range(5):
    x, y = random.uniform(-0.5, 0.5), random.uniform(0.9, 2.0)
    res.append(float(abs(V(x, y) - (mp.mpf(1)/3 + mp.mpf(4)/3*(-lap(x, y)/3)))))
out['identity_max_residual'] = max(res)
json.dump(out, open('field_tests/results/d2271_zhinu_masses.json','w'), indent=1); print(out)
