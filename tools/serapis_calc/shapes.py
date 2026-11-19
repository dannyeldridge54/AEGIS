"""Shape functions of a torus modulus U (P3 hunt, D1361–D1363) — exact to ~1e-12 on the fundamental domain.
E(U, s) = Σ'_{(m,n)} U₂^s/|m + nU|^{2s}  (GRV eq. 1.5 normalisation; = the SERAPIS-E E(τ,2)), via the Chowla–Selberg expansion.
E1hat(U) = −log(U₂|η(U)|⁴)  (the regularised s = 1 series, up to an additive constant; Kronecker limit formula)."""
import math, cmath
from scipy.special import kv, gamma, zeta
def _sigma(n, a): return sum(d**a for d in range(1, n + 1) if n % d == 0)
def E(U, s=2.0, nmax=40):
    x, y = U.real, U.imag
    out = 2*zeta(2*s)*y**s + 2*math.sqrt(math.pi)*gamma(s - 0.5)*zeta(2*s - 1)/gamma(s)*y**(1 - s)
    pref = 8*math.pi**s/gamma(s)*math.sqrt(y)
    for n in range(1, nmax + 1):
        out += pref*n**(s - 0.5)*_sigma(n, 1 - 2*s)*math.cos(2*math.pi*n*x)*kv(s - 0.5, 2*math.pi*n*y)
    return out
def log_eta(U, nmax=200):
    q = cmath.exp(2j*math.pi*U); s = 2j*math.pi*U/24
    for n in range(1, nmax + 1): s += cmath.log(1 - q**n)
    return s
def E1hat(U): return -math.log(U.imag) - 4*log_eta(U).real
def grad_hess(f, U, h=1e-4):
    x, y = U.real, U.imag; F = lambda a, b: f(complex(a, b))
    gx = (F(x + h, y) - F(x - h, y))/(2*h); gy = (F(x, y + h) - F(x, y - h))/(2*h)
    hxx = (F(x + h, y) - 2*F(x, y) + F(x - h, y))/h**2; hyy = (F(x, y + h) - 2*F(x, y) + F(x, y - h))/h**2
    hxy = (F(x + h, y + h) - F(x + h, y - h) - F(x - h, y + h) + F(x - h, y - h))/(4*h*h)
    return (gx, gy), (hxx, hxy, hyy)
RHO = complex(0.5, math.sqrt(3)/2); I = 1j
