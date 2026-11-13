"""D19: one no-scale model with a plateau, a kick and a dark-energy tail. Tests T-ROLL and T-DE together. AI-assisted.
V = |F(T)|^2/(4 x^2) (stabiliser model, units m = 1), T = x + i y, x = e^{c phi}, c = sqrt(2/3), g_yy = 3/(2 x^2).
F(T) = T^{3/2} (T + mu)^{-1/2} + delta e^{i gamma} e^{-a T}:
  large x: F ~ T          -> V -> 1/4: the alpha = 1 plateau (V = (1/4)/(1 + mu e^{-c phi}) along y = 0)
  small x: F ~ T^{3/2}/sqrt(mu) -> V ~ x/(4 mu) = e^{c phi}/(4 mu): a tail of slope sqrt(2/3) (KAPPA-ALPHA1's value), no vacuum
  e^{-aT}: the kick near the end (Development 18).
T-ROLL: the angle's mass^2 = V_yy/g_yy follows the potential, not a vacuum; after inflation the kinetic energy dominates
(kination), so m_y/H should collapse. Printed: m_y/H and the angle speed r = sqrt(g_yy)|y'| from inflation into kination."""
import cmath, math
from scipy.integrate import solve_ivp
c = math.sqrt(2 / 3); NSTAR = 55.6


def make(mu, delta, a, gamma=math.pi / 2):
    d = delta * cmath.exp(1j * gamma)
    def V(p, y):
        x = math.exp(c * p); T = complex(x, y)
        return abs(T ** 1.5 / cmath.sqrt(T + mu) + d * cmath.exp(-a * T)) ** 2 / (4 * x * x)
    def d1(p, y, h=1e-6):
        return (V(p + h, y) - V(p - h, y)) / (2 * h), (V(p, y + h) - V(p, y - h)) / (2 * h)
    def vyy(p, y, h=1e-4):
        return (V(p, y + h) - 2 * V(p, y) + V(p, y - h)) / h ** 2
    return V, d1, vyy


def run(mu=1.0, delta=0.1, a=1.0, p0=5.6, after=6.0):
    V, d1, vyy = make(mu, delta, a)
    def rhs(N, z):
        p, y, dp, dy = z; g = 1.5 * math.exp(-2 * c * p); eps = 0.5 * (dp * dp + g * dy * dy)
        v = V(p, y); vp, vy = d1(p, y)
        return [dp, dy, -c * g * dy * dy - (3 - eps) * (dp + vp / v), 2 * c * dp * dy - (3 - eps) * (dy + vy / (g * v))]
    end = lambda N, z: 0.5 * (z[2] ** 2 + 1.5 * math.exp(-2 * c * z[0]) * z[3] ** 2) - 1
    end.direction = 1
    sol = solve_ivp(rhs, [0, 400], [p0, 0, 0, 0], events=end, rtol=1e-10, atol=1e-13, dense_output=True, method="LSODA")
    Ne = sol.t_events[0][0]
    def at(N):
        p, y, dp, dy = sol.sol(N); g = 1.5 * math.exp(-2 * c * p); eps = 0.5 * (dp * dp + g * dy * dy)
        H2 = V(p, y) / (3 - eps)                       # H^2 in units m^2 (M_P = 1)
        return {"eps": eps, "m_over_H": math.sqrt(max(vyy(p, y), 0) / g / H2), "r": math.sqrt(g) * abs(dy), "phi": p}
    e0 = at(Ne - NSTAR)["eps"]; e1 = at(Ne - NSTAR + 0.01)["eps"]
    ns = 1 - 2 * e0 - (math.log(e1) - math.log(e0)) / 0.01
    return Ne, ns, 16 * e0, at, sol


if __name__ == "__main__":
    for mu, delta, a in ((1.0, 0.0, 1.0), (1.0, 0.1, 1.0), (1.0, 0.3, 1.0), (0.1, 0.1, 1.0)):
        Ne, ns, rt, at, sol = run(mu, delta, a)
        print(f"\nmu {mu}, delta {delta}, a {a}: inflation ends at N = {Ne:.1f}; n_s {ns:.4f}, r_tensor {rt:.4f}")
        print("   N - N_end    eps      phi     m_y/H     angle speed r")
        for dN in (-NSTAR, -5, -1, 0, 0.5, 1, 2, 4):
            if Ne + dN > sol.t[-1]:
                break
            o = at(Ne + dN)
            print(f"   {dN:+7.1f}   {o['eps']:6.3f}  {o['phi']:+7.3f}  {o['m_over_H']:8.3f}   {o['r']:.3e}")
