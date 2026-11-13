"""D169: what the Twist predicts for H0 once the CMB fixes the early universe. Hold omega_m = Omega_m h^2 = 0.1430, omega_r, and the
comoving distance to last scattering D_M(z* = 1090) (i.e. theta*, given a fixed sound horizon) at their LCDM (h = 0.674) values; solve
for the Twist's h. The tail is rung-3 thawing quintessence from rest. AI-assisted (background-only estimate; no full CMB fit)."""
import math
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
wm, wr, zs, lam = 0.1430, 4.15e-5, 1090.0, math.sqrt(2 / 3)
def twist_E2(h):
    Om, Or = wm / h ** 2, wr / h ** 2; ODE = 1 - Om - Or
    def go(V0):
        def rhs(N, y):
            p, v = y; a = math.exp(N); V = V0 * math.exp(-lam * p); H2 = (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
            eps = (1.5 * Om * a ** -3 + 2 * Or * a ** -4 + 0.5 * v * v * H2) / H2; return [v, -(3 - eps) * v + lam * V / H2]
        return solve_ivp(rhs, [math.log(1e-4), 0], [0, 0], rtol=1e-10, atol=1e-13, dense_output=True)
    def f0(V0):
        s = go(V0); p, v = s.y[:, -1]; V = V0 * math.exp(-lam * p); H2 = (Om + Or + V / 3) / (1 - v * v / 6); return (v * v * H2 / 6 + V / 3) / H2 - ODE
    V0 = brentq(f0, 1e-2, 1e3); S = go(V0)
    def E2(a):
        if a < 1e-4: return Om * a ** -3 + Or * a ** -4
        p, v = S.sol(math.log(a)); V = V0 * math.exp(-lam * p); return (Om * a ** -3 + Or * a ** -4 + V / 3) / (1 - v * v / 6)
    return E2
def DM(E2, h):                    # in units of c/(100 km/s/Mpc)
    f = lambda z: 1 / math.sqrt(E2(1 / (1 + z)))
    return (quad(f, 0, 3, limit=200)[0] + quad(f, 3, 50, limit=200)[0] + quad(f, 50, zs, limit=400)[0]) / h
hL = 0.674; OmL = wm / hL ** 2; E2L = lambda a: OmL * a ** -3 + wr / hL ** 2 * a ** -4 + (1 - OmL - wr / hL ** 2)
target = DM(E2L, hL)
hT = 0.6572 if __name__ != "__main__" else brentq(lambda h: DM(twist_E2(h), h) - target, 0.60, 0.70, xtol=1e-6)
print(f"LCDM: H0 = {100*hL:.2f}, Omega_m = {OmL:.4f}")
print(f"Twist (same omega_m and theta*): H0 = {100*hT:.2f} km/s/Mpc ({100*(hT-hL):+.2f}), Omega_m = {wm/hT**2:.4f}")
print(f"SH0ES-type local value ~73: the Twist moves H0 {'away from' if hT < hL else 'towards'} it")
