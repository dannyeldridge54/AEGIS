"""Exact single-field Mukhanov-Sasaki spectra (M_P = 1), written independently of the v3 scripts.
Background in e-fold time N; mode equation for u = z R (scalar, z = a phi_N) and u_t (tensor, z = a):
u'' + (1-eps) u' + [k^2/(aH)^2 - (z''/z)/(aH)^2] u = 0 is avoided; we integrate R directly:
R'' + (3 - eps + 2 phi_NN/phi_N) R' + (k/aH)^2 R = 0,  h'' + (3 - eps) h' + (k/aH)^2 h = 0.
P_R = k^3 |R|^2/(2 pi^2),  P_t = 8 k^3 |h|^2/(2 pi^2) with h normalised as u_t/a (Bunch-Davies)."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
class Background:
    def __init__(self, V, dV, phi0, Nmax=400):
        def rhs(N, y):
            p, pn = y; eps = 0.5*pn*pn
            return [pn, -(3-eps)*pn - (3-eps)*dV(p)/V(p)]
        ev = lambda N, y: 0.5*y[1]**2 - 1; ev.terminal = True; ev.direction = 1
        s = solve_ivp(rhs, [0, Nmax], [phi0, -dV(phi0)/V(phi0)], events=ev, rtol=1e-11, atol=1e-13, dense_output=True)
        self.sol = s; self.Nend = s.t_events[0][0] if len(s.t_events[0]) else None; self.V = V
    def state(self, N):
        p, pn = self.sol.sol(N); eps = 0.5*pn*pn
        H = np.sqrt(self.V(p)/(3-eps)); return p, pn, eps, H
def spectra(bg, Nstar, dlnk=(-0.1, -0.05, 0.0, 0.05, 0.1), Npivot=None, bd=200.0):
    """Return dict with P_R, P_t at ln k offsets, and n_s, r, alpha_s at the pivot that exits at Nend - Nstar."""
    Np = bg.Nend - Nstar if Npivot is None else Npivot
    _, _, _, Hp = bg.state(Np); kp = Hp   # a(N) = e^{N-Np}: normalised at the pivot (D955 D1)
    out = []
    for dl in dlnk:
        k = kp*np.exp(dl)
        # start where k/aH = 200
        f = lambda N: k/(np.exp(N-Np)*bg.state(N)[3]) - bd
        lo, hi = 0.0, Np
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if f(mid) > 0: lo = mid
            else: hi = mid
        N0 = lo
        def rhs(N, y):
            p, pn, eps, H = bg.state(N)
            dV = (bg.V(p+1e-6)-bg.V(p-1e-6))/2e-6
            pnn = -(3-eps)*pn - (3-eps)*dV/bg.V(p)
            q2 = (k/(np.exp(N-Np)*H))**2
            R, Rp, h, hp = y[0]+1j*y[1], y[2]+1j*y[3], y[4]+1j*y[5], y[6]+1j*y[7]
            Rpp = -(3-eps+2*pnn/pn)*Rp - q2*R
            hpp = -(3-eps)*hp - q2*h
            return [Rp.real, Rp.imag, Rpp.real, Rpp.imag, hp.real, hp.imag, hpp.real, hpp.imag]
        p, pn, eps, H = bg.state(N0); a = np.exp(N0-Np)
        # Bunch-Davies: u = e^{-ik eta}/sqrt(2k); du/dN = -i (k/aH) u; R = u/z, z = a pn; h = u/a
        u = 1/np.sqrt(2*k); un = -1j*(k/(a*H))*u
        dV = (bg.V(p+1e-6)-bg.V(p-1e-6))/2e-6; pnn = -(3-eps)*pn - (3-eps)*dV/bg.V(p)
        z = a*pn; zn = z*(1 + pnn/pn)
        R = u/z; Rn = un/z - u*zn/z**2
        h = u/a; hn = un/a - u/a
        y0 = [R.real, R.imag, Rn.real, Rn.imag, h.real, h.imag, hn.real, hn.imag]
        Nf = min(Np + 12 + dl, (bg.Nend - 0.5) if bg.Nend else Np + 12 + dl)
        s = solve_ivp(rhs, [N0, Nf], y0, rtol=1e-11, atol=1e-30, method='DOP853')
        y = s.y[:, -1]
        PR = k**3*(y[0]**2+y[1]**2)/(2*np.pi**2); Pt = 8*k**3*(y[4]**2+y[5]**2)/(2*np.pi**2)
        out.append((dl, PR, Pt))
    d = np.array([o[0] for o in out]); lp = np.log([o[1] for o in out])
    c = np.polyfit(d, lp, 4)
    c = c[2:]
    i0 = list(d).index(0.0)
    return dict(ns=1+c[1], alpha_s=2*c[0], r=out[i0][2]/out[i0][1], PR=out[i0][1])
