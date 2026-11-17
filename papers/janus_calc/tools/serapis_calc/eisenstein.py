"""Non-holomorphic Eisenstein series E(tau,s) = (1/2) sum_{gcd(c,d)=1} y^s/|c tau+d|^{2s}.
Two independent evaluations: Fourier series (fast) and direct lattice sum (slow, check only)."""
import mpmath as mp
def xi(s):
    return mp.pi**(-mp.mpf(s)/2)*mp.gamma(mp.mpf(s)/2)*mp.zeta(s)
def _sigma(n, a):
    return sum(mp.mpf(d)**a for d in range(1, n+1) if n % d == 0)
def E_fourier(x, y, s=2, nmax=20):
    """E = y^s + phi(s) y^{1-s} + (4 sqrt(y)/xi(2s)) sum_{n>=1} n^{s-1/2} sigma_{1-2s}(n) K_{s-1/2}(2 pi n y) cos(2 pi n x)."""
    x, y, s = mp.mpf(x), mp.mpf(y), mp.mpf(s)
    val = y**s + xi(2*s-1)/xi(2*s)*y**(1-s)
    for n in range(1, nmax+1):
        val += 4*mp.sqrt(y)/xi(2*s)*mp.mpf(n)**(s-0.5)*_sigma(n, 1-2*s)*mp.besselk(s-0.5, 2*mp.pi*n*y)*mp.cos(2*mp.pi*n*x)
    return float(val)
def E_lattice(x, y, s=2, N=400):
    """sum'_{m,n} y^s/|m+n tau|^{2s} / (2 zeta(2s)), truncated square |m|,|n|<=N (check only)."""
    import numpy as np
    m = np.arange(-N, N+1)
    M, Nn = np.meshgrid(m, m)
    z = M + Nn*(x + 1j*y)
    a = np.abs(z)**(2*s); a[N, N] = np.inf
    return float((y**s*(1/a)).sum()/(2*float(mp.zeta(2*s))))
def E_paper(x, y, s=2):
    """Paper/BHK convention: sum'_{m,n} y^s/|m+n tau|^{2s} = 2 zeta(2s) E(tau,s). SERAPIS v3 uses THIS for E(U,2)."""
    return 2*float(mp.zeta(2*s))*E_fourier(x, y, s)
