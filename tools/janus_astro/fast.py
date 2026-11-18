# AEGIS-FP A4E2CFTN7Q36MPJA · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""A6c: compiled (numba) fast paths for Hyperion's heaviest calculations. Each kernel implements the SAME algorithm as a
validated Python routine and is regression-tested against it:
  orbits_fast      == mapper_feed.orbit_params_batch3 (per-star adaptive KDK leapfrog, tabulated bulge M(r), parabolic
                      turning points, two-tier step), run in parallel over stars;
  jfactor_fast     == jfactor.J_route_B with the line-of-sight integral on fixed Gauss-Legendre panels."""
import math, numpy as np
from numba import njit, prange

@njit(cache=True, fastmath=False)
def _acc(x, y, z, lr0, dlr, Mb, bamp_unused, hamp, ha, damp, a, b):
    R = math.sqrt(x*x + y*y); r = math.sqrt(R*R + z*z)
    u = (math.log(r) - lr0)/dlr; i = int(u)
    if i < 0: i = 0
    if i > Mb.size - 2: i = Mb.size - 2
    f = u - i; M = Mb[i]*(1 - f) + Mb[i + 1]*f
    fs = (-M/(r*r) - hamp*(math.log1p(r/ha)/(r*r) - 1.0/(r*(ha + r))))/r
    sq = math.sqrt(z*z + b*b); D = (R*R + (a + sq)**2)**1.5; fd = -damp/D
    return (fs + fd)*x, (fs + fd)*y, fs*z + fd*z*(a + sq)/sq

@njit(cache=True)
def _vertex(t0, t1, t2, y0, y1, y2):
    d0 = t1 - t0; d1 = t2 - t1
    if d0 <= 0 or d1 <= 0: return y1
    A = ((y2 - y1)/d1 - (y1 - y0)/d0)/(d0 + d1)
    if A == 0: return y1
    B = (y1 - y0)/d0 - A*(t1 + t0); tv = -B/(2*A)
    if not (tv > t0 and tv < t2): return y1
    C = y1 - A*t1*t1 - B*t1
    return A*tv*tv + B*tv + C

@njit(parallel=True, cache=True)
def _orbits(X0, V0, T, eta, eta_in, rin, lr0, dlr, Mb, hamp, ha, damp, a, b, out):
    N = X0.shape[1]
    for k in prange(N):
        x, y, z = X0[0, k], X0[1, k], X0[2, k]; vx, vy, vz = V0[0, k], V0[1, k], V0[2, k]
        t = 0.0; r = math.sqrt(x*x + y*y + z*z); az = abs(z)
        rp = r; ra = r; zm = az; t1 = t; t2 = t; r1 = r; r2 = r; z1 = az; z2 = az
        ax, ay, azz = _acc(x, y, z, lr0, dlr, Mb, 0.0, hamp, ha, damp, a, b)
        while t < T - 1e-12:
            sp = math.sqrt(vx*vx + vy*vy + vz*vz); et = eta_in if r < rin else eta
            h = min(et*r/max(sp, 1e-12), 0.02); h = min(h, T - t)
            vx += 0.5*h*ax; vy += 0.5*h*ay; vz += 0.5*h*azz
            x += h*vx; y += h*vy; z += h*vz
            ax, ay, azz = _acc(x, y, z, lr0, dlr, Mb, 0.0, hamp, ha, damp, a, b)
            vx += 0.5*h*ax; vy += 0.5*h*ay; vz += 0.5*h*azz; t += h
            r = math.sqrt(x*x + y*y + z*z); az = abs(z)
            if r1 <= r2 and r1 <= r: rp = min(rp, _vertex(t2, t1, t, r2, r1, r))
            if r1 >= r2 and r1 >= r: ra = max(ra, _vertex(t2, t1, t, r2, r1, r))
            if z1 >= z2 and z1 >= az: zm = max(zm, _vertex(t2, t1, t, z2, z1, az))
            rp = min(rp, r); ra = max(ra, r); zm = max(zm, az)
            t2 = t1; t1 = t; r2 = r1; r1 = r; z2 = z1; z1 = az
        out[0, k] = rp; out[1, k] = ra; out[2, k] = zm

def orbits_fast(x, y, z, vx, vy, vz, t_gyr=3.0, eta=0.01, eta_in=0.006, r_in_kpc=1.0, mw=None):
    from . import galaxy as G
    from scipy.special import gamma, gammainc
    mw = mw or G.MW(); p = mw.p; r0, v0 = 8.0, 220.0
    s = (3 - p['alpha'])/2; lr = np.linspace(math.log(1e-5), math.log(200.0), 20000)
    Mb = 2*math.pi*p['bamp']*p['rc']**(3 - p['alpha'])*gamma(s)*gammainc(s, (np.exp(lr)/p['rc'])**2)
    X = np.ascontiguousarray(np.array([x, y, z], float)/r0); V = np.ascontiguousarray(np.array([vx, vy, vz], float)/v0)
    T = t_gyr/(r0*3.0856775814913673e16/v0/3.15576e16); out = np.empty((3, X.shape[1]))
    _orbits(X, V, T, eta, eta_in, r_in_kpc/r0, lr[0], lr[1] - lr[0], Mb, p['hamp'], p['ha'], p['damp'], p['a'], p['b'], out)
    rp, ra, zm = out*r0
    return dict(rperi=rp, rapo=ra, zmax=zm, ecc=(ra - rp)/(ra + rp))

# ---- J-factor: line-of-sight integral on Gauss-Legendre panels, vectorised over angles ----
def jfactor_fast(rho_vec, r_sun, psi_max_deg=1.0, b_mask_deg=0.3, n_psi=160, n_s=64, panels=None):
    """rho_vec: vectorised density r(kpc) -> GeV/cm^3. Same geometry as jfactor.J_route_B."""
    from .jfactor import KPC_CM
    pm, bm = math.radians(psi_max_deg), math.radians(b_mask_deg)
    x, w = np.polynomial.legendre.leggauss(n_psi); psis = 0.5*(pm - bm)*(x + 1) + bm; wps = 0.5*(pm - bm)*w
    xs, ws = np.polynomial.legendre.leggauss(n_s)
    edges = np.array(panels if panels is not None else [0.0, 2.0, 6.0, 7.5, 8.0, 8.5, 9.0, 11.0, 16.0, 30.0, 60.0, 100.0])
    tot = 0.0
    for psi, wp in zip(psis, wps):
        cp = math.cos(psi); val = 0.0
        for lo, hi in zip(edges[:-1], edges[1:]):
            s = 0.5*(hi - lo)*(xs + 1) + lo
            rr = np.sqrt(s*s + r_sun*r_sun - 2*s*r_sun*cp)
            val += 0.5*(hi - lo)*np.dot(ws, rho_vec(rr)**2)
        frac = 1 - 2*math.asin(min(1.0, math.sin(bm)/math.sin(psi)))/math.pi
        tot += wp*math.sin(psi)*2*math.pi*frac*val*KPC_CM
    return tot
