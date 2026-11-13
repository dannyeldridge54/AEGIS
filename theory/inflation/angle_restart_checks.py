"""D16 checks for the moving-minimum restart (angle_restart_periodic.py model). AI-assisted.
At horizon exit of the CMB scale (N* = 55.6 e-folds before the end, TWIST-INFLATION):
 (1) isocurvature: the angle's mass along its valley, m^2/H^2 = 3 g^thth V_thth / V (|cos a| ~ 1 at the minimum).
     m/H >> 3/2 means the angle is heavy: its fluctuations decay and leave no matter-density patches.
 (2) n_s and r: effective single-field values from the exact background, n_s = 1 - 2 eps_H - eta_H, eta_H = d ln eps_H/dN,
     r = 16 eps_H c_s, with the heavy-field sound speed c_s^-2 = 1 + 4 Omega^2/(m^2 - Omega^2... ) ~ 1 + 4 (Omega/H)^2/(m/H)^2,
     Omega = turn rate of the trajectory. Compared with the no-angle-potential case."""
import math, numpy as np
from scipy.integrate import solve_ivp
lam, c = -2 * math.sqrt(2 / 3), math.sqrt(2 / 3); NSTAR = 55.6
def traj(EPS, F, D, s0=6.4):
    ph = lambda s: -D * math.exp(-c * s); dph = lambda s: D * c * math.exp(-c * s)
    U = lambda s: (1 - math.exp(-c * s)) ** 2; Us = lambda s: 2 * c * math.exp(-c * s) * (1 - math.exp(-c * s))
    def parts(y):
        s, t, ds, dt = y; a = t / F + ph(s)
        v = U(s) * (1 + EPS * math.cos(a)); vs = Us(s) * (1 + EPS * math.cos(a)) - U(s) * EPS * math.sin(a) * dph(s)
        vt = -U(s) * EPS / F * math.sin(a); vtt = -U(s) * EPS / F ** 2 * math.cos(a)
        return v, vs, vt, vtt
    def rhs(N, y):
        s, t, ds, dt = y; g = math.exp(lam * s); e = 0.5 * (ds * ds + g * dt * dt); v, vs, vt, _ = parts(y)
        return [ds, dt, 0.5 * lam * g * dt * dt - (3 - e) * (ds + vs / v), -lam * ds * dt - (3 - e) * (dt + vt / (g * v))]
    end = lambda N, y: 0.5 * (y[2] ** 2 + math.exp(lam * y[0]) * y[3] ** 2) - 1; end.terminal = True; end.direction = 1
    sol = solve_ivp(rhs, [0, 300], [s0, -F * ph(s0), 0, 0], events=end, rtol=1e-11, atol=1e-14, dense_output=True)
    Ne = sol.t_events[0][0]
    def at(N):
        y = sol.sol(N); s, t, ds, dt = y; g = math.exp(lam * s); epsH = 0.5 * (ds * ds + g * dt * dt)
        v, vs, vt, vtt = parts(y)
        m2 = 3 * (vtt / (g * v)) if EPS else 0.0
        # turn rate: angle between successive velocity directions (canonical frame), per e-fold
        h = 1e-3; y2 = sol.sol(N + h)
        u1 = np.array([ds, math.sqrt(g) * dt]); u2 = np.array([y2[2], math.exp(lam * y2[0] / 2) * y2[3]])
        om = abs(math.atan2(u1[0] * u2[1] - u1[1] * u2[0], u1 @ u2)) / h
        return epsH, m2, om
    N0 = Ne - NSTAR; e0, m2, om = at(N0); e1, _, _ = at(N0 + 0.01)
    etaH = (math.log(e1) - math.log(e0)) / 0.01
    cs = 1 / math.sqrt(1 + (4 * om * om / m2 if m2 > 0 else 0))
    return {"N_total": Ne, "m_over_H": math.sqrt(m2) if m2 > 0 else 0, "turn": om, "c_s": cs,
            "n_s": 1 - 2 * e0 - etaH, "r": 16 * e0 * cs}
b = traj(0.0, 1.0, 0.0)
print(f"no angle potential: n_s {b['n_s']:.4f}  r {b['r']:.4f}")
print("   EPS    F    D   N_tot   m/H    turn/H    c_s     n_s     r")
for EPS, F, D in ((1e-2, 0.3, 3.0), (0.1, 1.0, 1.0), (0.1, 3.0, 3.0), (1e-2, 1.0, 3.0)):
    o = traj(EPS, F, D)
    print(f"{EPS:6.0e} {F:4.1f} {D:4.1f} {o['N_total']:6.1f} {o['m_over_H']:7.1f} {o['turn']:8.1e} {o['c_s']:7.4f} {o['n_s']:7.4f} {o['r']:.4f}")
