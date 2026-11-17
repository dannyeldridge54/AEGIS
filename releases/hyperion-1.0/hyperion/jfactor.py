"""J-factors for dark-matter annihilation: J = ∫_ΔΩ dΩ ∫ ρ²(r(s, ψ)) ds, in GeV² cm⁻⁵.
Profiles (GeV/cm³, kpc): Einasto, NFW, Burkert, Einasto with a constant-density core. Region: cone ψ ≤ psi_max around the
Galactic Centre with the plane |b| < b_mask removed. Route A: (l, b) grid. Route B: polar (ψ, φ) around the GC."""
import math, numpy as np
from scipy.integrate import quad
KPC_CM = 3.0856775814913673e21
def einasto(rs, alpha):  return lambda r: math.exp(-2/alpha*((r/rs)**alpha - 1))
def nfw(rs):             return lambda r: 1/((r/rs)*(1+r/rs)**2)
def burkert(r0):         return lambda r: 1/((1+r/r0)*(1+(r/r0)**2))
def cored(shape, rc):    return lambda r: shape(max(r, rc))
def normalise(shape, rho_sun, r_sun):
    k = rho_sun/shape(r_sun); return lambda r: k*shape(r)
def los(rho, psi, r_sun, smax=100.0):
    """∫ρ² ds along a line of sight at angle psi from the GC, in GeV² cm⁻⁵ (ds in cm)."""
    cp = math.cos(psi)
    f = lambda s: rho(math.sqrt(s*s + r_sun*r_sun - 2*s*r_sun*cp))**2
    pts = [r_sun*cp] if 0 < r_sun*cp < smax else None
    return quad(f, 0, smax, points=pts, epsabs=0, epsrel=1e-10, limit=400)[0]*KPC_CM
def J_route_A(rho, r_sun, psi_max_deg=1.0, b_mask_deg=0.3, n=120):
    """(l, b) Gauss-Legendre grid over the box |l|,|b| ≤ psi_max, keeping ψ ≤ psi_max and |b| ≥ b_mask (exact cosψ = cos b cos l)."""
    pm, bm = math.radians(psi_max_deg), math.radians(b_mask_deg)
    x, w = np.polynomial.legendre.leggauss(n)
    tot = 0.0
    bs = 0.5*(pm-bm)*(x+1) + bm; wb = 0.5*(pm-bm)*w          # b in [bm, pm], doubled for b<0
    for b, wbb in zip(bs, wb):
        lmax = math.acos(min(1.0, math.cos(pm)/math.cos(b)))
        ls = lmax*x; wl = lmax*w
        for l, wll in zip(ls, wl):
            psi = math.acos(math.cos(b)*math.cos(l))
            tot += 2*wbb*wll*math.cos(b)*los(rho, psi, r_sun)
    return tot
def J_route_B(rho, r_sun, psi_max_deg=1.0, b_mask_deg=0.3, n_psi=160, n_phi=256):
    """Polar coordinates about the GC: dΩ = sinψ dψ dφ; mask by sin b = sinψ sinφ."""
    pm, bm = math.radians(psi_max_deg), math.radians(b_mask_deg)
    x, w = np.polynomial.legendre.leggauss(n_psi)
    tot = 0.0
    psis = 0.5*(pm-bm)*(x+1) + bm; wps = 0.5*(pm-bm)*w      # ψ < bm is fully masked
    for psi, wp in zip(psis, wps):
        # fraction of the ring with |sin b| >= sin bm: |sinφ| >= sin bm / sin ψ
        frac = 1 - 2*math.asin(min(1.0, math.sin(bm)/math.sin(psi)))/math.pi
        tot += wp*math.sin(psi)*2*math.pi*frac*los(rho, psi, r_sun)
    return tot
