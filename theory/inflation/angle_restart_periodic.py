"""D15b/c: angle restart with a periodic (axion-like) angle potential, static phase and inflaton-dependent phase.
Same curved field space and equations as angle_restart_twofield.py. AI-assisted.
  static:  V = V_E(sigma) (1 + EPS cos(theta/F + PH))
  moving:  V = V_E(sigma) (1 + EPS cos(theta/F - D e^{-c sigma}))   (the minimum shifts by ~D*F as sigma falls from the
           plateau to the end of inflation: an Affleck-Dine-type kick)."""
import math, sys
from scipy.integrate import solve_ivp
lam, c = -2 * math.sqrt(2 / 3), math.sqrt(2 / 3)
def run(EPS, F, D=0.0, PH=0.3, s0=5.9):
    ph = lambda s: PH if D == 0 else -D * math.exp(-c * s)
    dph = lambda s: 0.0 if D == 0 else D * c * math.exp(-c * s)
    U = lambda s: (1 - math.exp(-c * s)) ** 2; Us = lambda s: 2 * c * math.exp(-c * s) * (1 - math.exp(-c * s))
    def rhs(N, y):
        s, t, ds, dt = y; g = math.exp(lam * s); e = 0.5 * (ds * ds + g * dt * dt); a = t / F + ph(s)
        v = U(s) * (1 + EPS * math.cos(a))
        vs = Us(s) * (1 + EPS * math.cos(a)) - U(s) * EPS * math.sin(a) * dph(s)
        vt = -U(s) * EPS / F * math.sin(a)
        return [ds, dt, 0.5 * lam * g * dt * dt - (3 - e) * (ds + vs / v), -lam * ds * dt - (3 - e) * (dt + vt / (g * v))]
    end = lambda N, y: 0.5 * (y[2] ** 2 + math.exp(lam * y[0]) * y[3] ** 2) - 1; end.terminal = True; end.direction = 1
    sol = solve_ivp(rhs, [0, 200], [s0, -F * ph(s0), 0, 0], events=end, rtol=1e-10, atol=1e-13)
    s, t, ds, dt = sol.y_events[0][0]; return sol.t_events[0][0], t, math.exp(lam * s / 2) * abs(dt)
if __name__ == "__main__":
    print("static phase (F = 1):", [f"{run(E, 1.0)[2]:.1e}" for E in (1e-3, 1e-2, 5e-2)])
    print("   EPS     F     D      N   r_end")
    for F in (0.3, 1.0, 3.0):
        for EPS in (1e-3, 1e-2, 0.1):
            for D in (1.0, 3.0):
                N, t, r = run(EPS, F, D); print(f"{EPS:6.0e} {F:5.1f} {D:5.1f} {N:6.1f} {r:.2e}")
