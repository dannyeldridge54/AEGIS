# AEGIS-FP YJO5YP4Y5TJDPF2M · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Wino Sommerfeld enhancement at leading order (s-wave, spin singlet), two states (chi0 chi0, chi+ chi-).
Potential (Cohen-Lisanti-Pierce-Slatyer 1307.4082 App. A eq. A4; same as 2507.15934 eq. for n = 3, i = 0, 1):
  V_00 = 0, V_0+ = V_+0 = -sqrt(2) alpha_W e^{-m_W r}/r, V_++ = 2 dm - alpha/r - alpha_W c_W^2 e^{-m_Z r}/r.
Radial equation for u = r psi with reduced mass M/2:  u'' = M (V - E) u,  E = M v^2/4 (v: RELATIVE velocity; each particle moves at v/2 in the CM frame).
Sommerfeld vector s_j = u_j'(0) for the solution whose chi0chi0 channel is a unit-amplitude wave sin(kr + d)/k at large r and whose
closed chi+chi- channel decays (E < 2 dm). Free case: s = (1, 0)."""
import math, numpy as np
from scipy.integrate import solve_ivp
ALPHA_W = 0.0335; S_W2 = 0.231; ALPHA = ALPHA_W*S_W2; M_W, M_Z = 80.4, 91.19; DM = 0.1645   # GeV; dm from 1307.4082 eq. 2
def wino_s(M, v=2e-3, alpha_w=ALPHA_W, dm=DM, R=None):
    E = M*v*v/4; k = math.sqrt(M*E); kap = math.sqrt(M*(2*dm - E))
    cw2 = 1 - S_W2
    def V(r):
        off = -math.sqrt(2)*alpha_w*math.exp(-M_W*r)/r
        return np.array([[0.0, off], [off, 2*dm - alpha_w*S_W2/r - alpha_w*cw2*math.exp(-M_Z*r)/r]])
    R = R or max(40/kap, 30/M_W)
    r0 = 1e-7
    sols = []
    for j in range(2):
        y0 = np.zeros(4); y0[2+j] = 1.0; y0[j] = r0         # u = r0 e_j, u' = e_j
        def rhs(r, y):
            u, up = y[:2], y[2:]
            return np.concatenate([up, M*(V(r) - E*np.eye(2)) @ u])
        s = solve_ivp(rhs, [r0, R], y0, method='DOP853', rtol=1e-10, atol=1e-14)
        sols.append(s.y[:, -1])
    U = np.array([sols[0][:2], sols[1][:2]]).T; Up = np.array([sols[0][2:], sols[1][2:]]).T   # columns = basis solutions
    # closed channel (index 1): kill the growing mode: u1' - kap u1 = 0 is the decaying-mode condition? decaying: u ~ e^{-kap r} => u' + kap u = 0
    g = Up[1, :] + kap*U[1, :]
    c = np.array([g[1], -g[0]])                                # combination with g.c = 0
    u0, u0p = U[0, :] @ c, Up[0, :] @ c
    amp = math.hypot(u0, u0p/k)                                # u0 = A sin(kr+d): A = sqrt(u0^2 + (u0'/k)^2)
    return c/(amp*k)                                           # normalise to A = 1/k
def coulomb_single(M, v, alpha):
    """Single attractive Coulomb channel, same normalisation (check): u'' = M(-alpha/r - E)u."""
    E = M*v*v/4; k = math.sqrt(M*E); R = 400/k
    s = solve_ivp(lambda r, y: [y[1], M*(-alpha/r - E)*y[0]], [1e-9, R], [1e-9, 1.0], method='DOP853', rtol=1e-11, atol=1e-16)
    u, up = s.y[0, -1], s.y[1, -1]
    # Coulomb asymptotics contain a log phase; amplitude from u^2 + (u'/k_loc)^2 with local k_loc = sqrt(M(E + alpha/R))
    kl = math.sqrt(M*(E + alpha/R)); A = math.hypot(u, up/kl)*math.sqrt(kl/k)   # WKB: amplitude ∝ 1/sqrt(k(r)) (DEVIATIONS D1)
    return 1/(A*k)

def single_channel(M, v, V, alpha_tail=0.0, R=None):
    """Generic single-channel s-wave Sommerfeld factor S = |psi(0)|^2 for potential V(r) (GeV), relative velocity v.
    alpha_tail: coefficient of a long-range -alpha_tail/r tail (attractive > 0) for the WKB-local amplitude (method of coulomb_single)."""
    E = M*v*v/4; k = math.sqrt(M*E); R = R or 400/k
    s = solve_ivp(lambda r, y: [y[1], M*(V(r) - E)*y[0]], [1e-9, R], [1e-9, 1.0], method='DOP853', rtol=1e-11, atol=1e-16)
    u, up = s.y[0, -1], s.y[1, -1]
    kl = math.sqrt(M*(E + alpha_tail/R)); A = math.hypot(u, up/kl)*math.sqrt(kl/k)
    return (1/(A*k))**2

def two_channel_open(M, v, Vfun, dm, tails=(0.0, 0.0), R=None):
    """Both channels open (E > 2 dm). Channel 0: chi0chi0 (threshold 0), channel 1: chi+chi- (threshold 2 dm).
    Vfun(r) -> 2x2 potential WITHOUT the 2dm constant (added here). tails: attractive -a/r coefficients per channel for WKB-local k.
    Returns s[i, j] = Sommerfeld amplitude for incoming channel i into short-distance channel j; free case s = I."""
    import cmath
    E = M*v*v/4; thr = np.array([0.0, 2*dm]); k = np.sqrt(M*(E - thr)); R = R or 300/min(k)
    def V(r): return Vfun(r) + np.diag(thr)
    cols = []
    for j in range(2):
        y0 = np.zeros(4); y0[j] = 1e-9; y0[2+j] = 1.0
        s = solve_ivp(lambda r, y: np.concatenate([y[2:], M*(V(r) - E*np.eye(2)) @ y[:2]]), [1e-9, R], y0, method='DOP853', rtol=1e-10, atol=1e-16)
        cols.append(s.y[:, -1])
    U = np.array([c[:2] for c in cols]).T; Up = np.array([c[2:] for c in cols]).T     # [channel, solution]
    B = np.zeros((2, 2), complex)
    for ch in range(2):
        kl = math.sqrt(M*(E - thr[ch] + tails[ch]/R))
        for sol in range(2):
            u, up = U[ch, sol], Up[ch, sol]
            # u = a e^{i phi} + b e^{-i phi}, u' = i kl (a e^{i phi} - b e^{-i phi}); amplitude rescaled by sqrt(kl/k) (WKB)
            B[ch, sol] = 0.5*(u - up/(1j*kl))*math.sqrt(kl/k[ch])
    out = np.zeros((2, 2), complex)
    for i in range(2):
        target = np.zeros(2, complex); target[i] = -1/(2j*k[i])
        # incoming coefficients carry phase e^{-i kl R}; compare magnitudes via phase-free target: solve B c = target * e^{-i phi_i}
        ph = cmath.exp(-1j*math.sqrt(M*(E - thr[i] + tails[i]/R))*R)
        c = np.linalg.solve(B, target*0 + np.where(np.arange(2) == i, target[i]*ph, 0))
        out[i, :] = c          # u'(0) per channel = c (since u_j' (0) = delta)
    return out
