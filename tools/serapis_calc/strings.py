"""Level S (string/one-loop on tori). Built in stages; every stage is checked against an independent route.
S0: Jacobi theta functions and the abstruse identity theta3^4 - theta4^4 - theta2^4 = 0 (supersymmetric cancellation).
S1: one-loop Wilson-line / brane-scalar potential of one real bulk boson on R^4 x T^2 (D = 6), two independent routes:
    route A  momentum (KK) sum in proper time:  V(a)-V(0) = -(1/2)(4pi)^-2 int dt t^-3 sum_p [e^{-t|p+a|^2} - e^{-t|p|^2}]
    route B  winding (image) sum after Poisson:  V(a)-V(0) = -(A/pi^3) sum'_w [cos(a.w) - 1]/|w|^6
    and the curvature at a = 0:  Laplacian V = E_paper(U,2)/(pi^3 A)   (E_paper = sum' U2^2/|m+nU|^4, the SERAPIS convention).
    A fermion contributes with the opposite sign (weight -1 per real degree of freedom); so the mass of a positively coupled
    brane scalar carries +(N_B - N_F) E(U,2)/A, and the vacuum energy -(N_B - N_F) E(U,3) (D983).
S2 (next): open-string annulus/Moebius amplitudes with oscillators (theta/eta), whose massless limit must reproduce S1."""
import math, mpmath as mp, numpy as np
def theta(k, q): return mp.jtheta(k, 0, q)
def eta(q):  # Dedekind eta with q = e^{2 pi i tau}: q^{1/24} prod (1-q^n)
    return q**(mp.mpf(1)/24)*mp.qp(q)
def abstruse(q):
    return theta(3, q)**4 - theta(4, q)**4 - theta(2, q)**4
def lattice(L, U):
    """Torus with periods w1 = L, w2 = L*U (complex plane); area A = L^2 Im U."""
    U = complex(U); e1 = np.array([L, 0.0]); e2 = np.array([L*U.real, L*U.imag])
    A = L*L*U.imag
    # dual lattice: momenta p = 2 pi (m f1 + n f2) with f_i . e_j = delta_ij
    Mx = np.array([e1, e2]).T; F = np.linalg.inv(Mx).T
    return e1, e2, F[:, 0], F[:, 1], A
def V_routeB(a, L, U, N=60):
    e1, e2, f1, f2, A = lattice(L, U); a = np.asarray(a, float)
    m = np.arange(-N, N+1); M, Nn = np.meshgrid(m, m)
    W = M[..., None]*e1 + Nn[..., None]*e2; w2 = (W**2).sum(-1); w2[N, N] = np.inf
    return float(-(A/math.pi**3)*((np.cos(W @ a) - 1)/w2**3).sum())
def V_routeA(a, L, U, N=40):
    e1, e2, f1, f2, A = lattice(L, U); a = np.asarray(a, float)
    m = np.arange(-N, N+1); M, Nn = np.meshgrid(m, m)
    P = 2*math.pi*(M[..., None]*f1 + Nn[..., None]*f2)
    P2 = (P**2).sum(-1); edge = np.ones_like(P2, bool); edge[1:-1, 1:-1] = False
    R2 = (math.sqrt(P2[edge].min()) - math.sqrt(a @ a))**2      # largest disk complete for both the shifted and unshifted sums
    keep = P2 < R2
    pa = ((P + a)**2).sum(-1)[keep]; p0 = P2[keep]
    # below t0 the truncated sums are not complete; there the exact difference is O(exp(-|w_min|^2/4t0)) (Poisson), negligible
    t0 = 40.0/float(R2); wmin2 = min(e1 @ e1, e2 @ e2, (e1-e2) @ (e1-e2))
    assert wmin2/(4*t0) > 60, 'truncation too coarse for this torus'
    pa, p0 = np.sort(pa), np.sort(p0)
    f = lambda t: (np.exp(-t*pa).sum() - np.exp(-t*p0).sum())/t**3
    from scipy.integrate import quad
    pts = [t0, 1e-2, 0.1, 1, 10, 100]; tot = sum(quad(f, pts[i], pts[i+1], limit=200, epsabs=0, epsrel=1e-10)[0] for i in range(len(pts)-1))
    tot += quad(f, 100, np.inf, limit=200)[0]
    return float(-tot/(2*(4*math.pi)**2))
def laplacian_B(L, U, h=1e-3):
    V0 = V_routeB([0, 0], L, U)
    return (V_routeB([h, 0], L, U) + V_routeB([-h, 0], L, U) + V_routeB([0, h], L, U) + V_routeB([0, -h], L, U) - 4*V0)/h**2
