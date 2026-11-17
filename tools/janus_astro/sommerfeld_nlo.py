"""Wino Sommerfeld vector with the NLO electroweak potential of Beneke, Szafron, Urban 2020 (arXiv:2009.00640,
Eqs. 2.8, 3.14, 3.18, 3.25, 3.26; on-shell inputs). Same solver/normalisation as sommerfeld.wino_s (free case s = (1, 0))."""
import math, numpy as np
from scipy.integrate import solve_ivp
MW, MZ = 80.385, 91.1876; ALPHA = 1/128.943; CW2 = (MW/MZ)**2; SW2 = 1 - CW2; ALPHA2 = ALPHA/SW2; DM = 0.1641
GE = 0.5772156649015329; X0 = 555/94
def dV_off(r, a2=ALPHA2):
    x = MW*r; L = math.log(x)
    if x < X0:
        num = 79*(L-787/12)*(L-736/373)*(L-116/65)*(L*L-286*L/59+533/77)
        den = 34*(L-512/19)*(L-339/176)*(L-501/281)*(L*L-268*L/61+38/7); s = 1.0
    else:
        num = 13267*(L-76/43)*(L-28/17)*(L+37/30)*(L*L-389*L/88+676/129)
        den = 5*(L-191/108)*(L-256/153)*(L+8412/13)*(L*L-457*L/103+773/146); s = -1.0
    return 2595*a2*a2/(math.pi*r)*s*math.exp(-num/den)
def dV_pm(r, a=ALPHA, a2=ALPHA2):
    x = MW*r; lz = math.log(MZ*r)
    dinf = a*a/(2*math.pi*r)*(80/9)*(lz + GE)
    d0 = a2*a2/(2*math.pi*r)*(-(19/6)*lz + 4.92585)
    em = (a/r)*(-1/30 + (4/135)*math.log(x))/(1 + (58/79)*x**(-17/15) + (1/30)*x**(119/120) + (8/177)*x**(17/8))
    return dinf/(1 + (32/11)*x**(-22/9)) + d0/(1 + (7/59)*x**(61/29)) + em
def wino_s_nlo(M, v=1e-6, nlo=True, off_factor=1.0, dm=DM, R=None):
    E = M*v*v/4; k = math.sqrt(M*E); kap = math.sqrt(M*(2*dm - E))
    def V(r):
        off = -math.sqrt(2)*ALPHA2*math.exp(-MW*r)/r; d = 2*dm - ALPHA/r - ALPHA2*CW2*math.exp(-MZ*r)/r
        if nlo: off += off_factor*dV_off(r); d += dV_pm(r)
        return np.array([[0.0, off], [off, d]])
    R = R or max(40/kap, 30/MW); r0 = 1e-7; sols = []
    for j in range(2):
        y0 = np.zeros(4); y0[2+j] = 1.0; y0[j] = r0
        rhs = lambda r, y: np.concatenate([y[2:], M*(V(r) - E*np.eye(2)) @ y[:2]])
        s = solve_ivp(rhs, [r0, R], y0, method='DOP853', rtol=1e-10, atol=1e-14); sols.append(s.y[:, -1])
    U = np.array([sols[0][:2], sols[1][:2]]).T; Up = np.array([sols[0][2:], sols[1][2:]]).T
    g = Up[1, :] + kap*U[1, :]; c = np.array([g[1], -g[0]])
    u0, u0p = U[0, :] @ c, Up[0, :] @ c; amp = math.hypot(u0, u0p/k)
    return c/(amp*k)
