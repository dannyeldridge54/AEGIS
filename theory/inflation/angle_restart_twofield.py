"""D15: restarting the Twist angle at the end of inflation, solved in the curved two-field space. AI-assisted.
Field space (reduced Planck units): ds^2 = dsigma^2 + e^{lam sigma} dtheta^2, lam = -2 sqrt(2/3) (K = -2/3, alpha = 1).
Potential: E-model plateau along sigma with a small linear tilt eps_t along the angle coordinate:
    V = V0 (1 - e^{-c sigma})^2 (1 + eps_t theta),  c = sqrt(2/3).
Equations in N = ln a:  phi^a'' + Gamma^a_bc phi^b' phi^c' + (3 - eps)(phi^a' + g^ab V_b / V) = 0,  eps = |phi'|^2 / 2,
Gamma^sigma_thetatheta = -(lam/2) e^{lam sigma},  Gamma^theta_sigmatheta = lam/2.
Output: the angle's canonical speed r = e^{lam sigma/2} theta' (= thetadot_can/(H M_P)) at the end of inflation (eps = 1),
the tilt eps_t needed for r = 0.022 (MATTER, T_RH 1e13) and 0.030 (1e15), and whether n_s / N are disturbed."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
lam, c = -2 * math.sqrt(2 / 3), math.sqrt(2 / 3)


def run(eps_t, s0=5.9):
    def V(s, t): return (1 - math.exp(-c * s)) ** 2 * (1 + eps_t * t)
    def Vs(s, t): return 2 * c * math.exp(-c * s) * (1 - math.exp(-c * s)) * (1 + eps_t * t)
    def Vt(s, t): return (1 - math.exp(-c * s)) ** 2 * eps_t
    def rhs(N, y):
        s, t, ds, dt = y; g = math.exp(lam * s)
        eps = 0.5 * (ds * ds + g * dt * dt); v = V(s, t)
        dds = 0.5 * lam * g * dt * dt - (3 - eps) * (ds + Vs(s, t) / v)
        ddt = -lam * ds * dt - (3 - eps) * (dt + Vt(s, t) / (g * v))
        return [ds, dt, dds, ddt]
    def end(N, y): return 0.5 * (y[2] ** 2 + math.exp(lam * y[0]) * y[3] ** 2) - 1
    end.terminal = True; end.direction = 1
    y0 = [s0, 0.0, -Vs(s0, 0) / V(s0, 0) / 3 * 3 / 3, 0.0]
    sol = solve_ivp(rhs, [0, 200], y0, events=end, rtol=1e-10, atol=1e-13, dense_output=True)
    Ne = sol.t_events[0][0]; s, t, ds, dt = sol.y_events[0][0]
    return {"N_total": Ne, "sigma_end": s, "theta_end": t, "r_end": math.exp(lam * s / 2) * abs(dt), "sol": sol}


base = run(0.0)
print(f"no tilt: N = {base['N_total']:.1f}, sigma_end = {base['sigma_end']:.3f}, r_end = {base['r_end']:.1e}")
for eps_t in (1e-4, 1e-3, 3e-3, 1e-2):
    o = run(eps_t)
    print(f"tilt {eps_t:.0e}: N = {o['N_total']:.1f}  theta_end = {o['theta_end']:+.4f}  angle speed r_end = {o['r_end']:.3e}")
for need in (0.022, 0.030):
    e = brentq(lambda x: run(x)["r_end"] - need, 1e-6, 0.5)
    o = run(e)
    # canonical tilt (per M_P of canonical angle) at the end of inflation, and 56 e-folds before
    sol = o["sol"]; Ns = o["N_total"] - 56; s56 = sol.sol(max(Ns, 0))[0]
    print(f"r = {need}: coordinate tilt eps_t = {e:.2e}; canonical tilt at end = {e * math.exp(-lam * o['sigma_end'] / 2):.2e} per M_P,"
          f" 56 e-folds before end = {e * math.exp(-lam * s56 / 2):.2e} per M_P; theta travel {o['theta_end']:+.3f}")
