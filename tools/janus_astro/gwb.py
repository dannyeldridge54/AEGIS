"""Primordial (inflationary) gravitational-wave background today through an arbitrary post-inflation history.
Route A: piecewise power-law transfer (slope 2(3w-1)/(3w+1) for modes entering in a phase with equation of state w).
Route B: numerical tensor-mode evolution h'' + (3 - eps) h' + (k/aH)^2 h = 0 in e-folds N through a smooth w(N) background,
         amplitude read off with the exact WKB invariant once k/aH >= 200; T^2(k) = (k/aH)^2 h_amp^2 in the final radiation era
         (= 1 on the radiation plateau). Omega_GW h^2 = Omega_r h^2 * P_T / 24 * gfac * T^2.
Units: N = 0 is the start of the final radiation era (T_R); k in units of k_R = a_R H_R."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
OMEGA_R_H2 = 4.18e-5          # photons + 3 massless nu (T0 = 2.7255 K): 2.473e-5 * (1 + 0.2271*3.046)
MP = 2.435e18                 # reduced Planck mass, GeV
def gfac(gstar=106.75, gs=106.75, g0=3.363, gs0=3.909):
    return (gstar/g0)*(gs0/gs)**(4/3)
def f_R(T_R, gstar=106.75, gs=106.75, gs0=3.909, T0=2.7255*8.617333e-14):
    """Present frequency of the mode with k = a_R H_R (Hz)."""
    H = math.sqrt(math.pi**2*gstar/90)*T_R**2/MP
    return (T0*(gs0/gs)**(1/3)/T_R)*H/(2*math.pi)*1.519267e24
def rho_rad(T, gstar=106.75): return math.pi**2*gstar/30*T**4
class History:
    """phases: list of (w, lnrho_drop) going BACKWARD in time from T_R: e.g. [(0, ln(rho_x/rho_R)), (3/5, ln(rho_end/rho_x))],
    preceded by inflation (w = -1). width: smoothing of w steps in e-folds."""
    def __init__(self, phases, width=0.15, N_infl=12.0):
        self.phases = phases; edges = [0.0]; ws = [1/3]
        for w, dl in phases:
            edges.append(edges[-1] - dl/(3*(1+w))); ws.append(w)
        self.edges, self.ws = edges, ws + [-1.0 + 1e-4]
        self.Nmin = edges[-1] - N_infl
        N = np.linspace(self.Nmin, 8.0, 400000)
        w = np.full_like(N, 1/3)
        # w(N): smooth steps at each edge (going backward)
        w = 1/3 + 0*N
        for i, e in enumerate(edges):
            w = w + (self.ws[i+1] - self.ws[i])*0.5*(1 - np.tanh((N - e)/width))
        self.N, self.w = N, w
        # ln rho relative to rho_R at N = 0
        dl = -3*(1 + w); lr = np.concatenate([[0], np.cumsum(0.5*(dl[1:] + dl[:-1])*np.diff(N))])
        lr -= np.interp(0.0, N, lr)
        self.lnaH = CubicSpline(N, N + 0.5*lr)      # a H / (a_R H_R), with a = e^N, H ∝ rho^1/2
        self.eps = CubicSpline(N, 1.5*(1 + w))
    def k_end(self): return math.exp(float(self.lnaH(self.edges[-1])))
    def T2(self, k):
        """Route B transfer for mode k (units of k_R)."""
        lk = math.log(k)
        # DEVIATIONS D2: start at the last time before re-entry with k/aH = 1e-3 (post-inflation branch), else at the end of inflation
        Ne = self.edges[-1]; Ns = self.N; la = self.lnaH(Ns); tgt = lk - math.log(1e-3)
        post = (Ns >= Ne) & (la >= tgt)
        if post.any(): N0 = float(Ns[np.where(post)[0][-1]])
        else:
            N0 = Ne; self.last_start = k/math.exp(float(self.lnaH(Ne)))
            if self.last_start > 1e-2: raise ValueError('mode too close to k_end for route B')
        def rhs(N, y): q = k*math.exp(-float(self.lnaH(N))); return [y[1], -(3 - float(self.eps(N)))*y[1] - q*q*y[0]]
        stop = lambda N, y: k*math.exp(-float(self.lnaH(N))) - 200.0; stop.terminal = True; stop.direction = 1
        s = solve_ivp(rhs, [N0, 8.0], [1.0, 0.0], method='DOP853', rtol=1e-9, atol=1e-12, events=stop, max_step=0.05)
        N1 = float(s.t[-1]); h, hp = s.y[0, -1], s.y[1, -1]; q = k*math.exp(-float(self.lnaH(N1)))
        hamp2 = h*h + ((hp + h)/q)**2          # WKB invariant: h = (A/a) sin -> (h' + h) aH/k = (A/a) cos
        # carry to the final RD era: A = a h_amp is constant; T^2 = (k/aH)^2 h_amp^2 evaluated in RD = k^2 A^2 (a_R H_R = 1)
        A2 = math.exp(2*N1)*hamp2
        return k*k*A2
    def T2_routeA(self, k):
        """Piecewise power law with sudden transitions."""
        if k <= 1: return 1.0
        lt = 0.0; kk = 1.0
        for (w, dl) in self.phases:
            kn = kk*math.exp(dl*(1/(3*(1+w)))*(1 - 1.5*(1+w)/1.0) * -1) if False else None
            # boundary of this phase in k: aH ∝ rho^{(1+3w)/(6(1+w))}
            kb = kk*math.exp(dl*(1 + 3*w)/(6*(1 + w)))
            n = 2*(3*w - 1)/(3*w + 1)
            if k <= kb: return math.exp(lt)*(k/kk)**n
            lt += n*math.log(kb/kk); kk = kb
        return math.exp(lt)
def omega_gw_h2(f, T2, r, As=2.1e-9, nt=None, fstar=None):
    nt = -r/8 if nt is None else nt
    fstar = fstar or 0.05/(2*math.pi)*2.99792458e8/3.0856775814913673e22    # k* = 0.05 / Mpc
    return OMEGA_R_H2*r*As*(f/fstar)**nt/24*gfac()*T2
