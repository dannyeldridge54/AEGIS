"""D360 T2 (locked, PREREG_D360_TESTS): numerical modulus dilution vs D359's estimate. Units: GeV, M_P reduced. AI-assisted.
Variables in N = ln a: phi, dphi/dt, rho_r. Field equation phi'' + (3H+Gamma) phi' + m^2 phi = 0 (Gamma on the oscillating part), rho_r gets Gamma*phi'^2."""
import numpy as np, math
from scipy.integrate import solve_ivp
Mp = 2.435e18; gs = 106.75
def run(m, A):
    G = m ** 3 / (8 * math.pi * Mp ** 2)
    H0 = 10 * m; rho_tot0 = 3 * H0 ** 2 * Mp ** 2
    phi0 = A * Mp; rho_phi0 = 0.5 * m * m * phi0 ** 2
    rr0 = max(rho_tot0 - rho_phi0, 1e-3 * rho_tot0)
    # work in t with rescaled variables; integrate in log-time for stiffness
    def rhs(lt, y):
        t = math.exp(lt); phi, v, lrr = y
        rr = math.exp(lrr); rho = 0.5 * v * v + 0.5 * m * m * phi * phi + rr
        H = math.sqrt(rho / 3) / Mp
        dphi = v; dv = -(3 * H + G) * v - m * m * phi
        drr = -4 * H * rr + G * v * v
        return [t * dphi, t * dv, t * drr / rr]
    t0 = 1 / (2 * H0); tend = 60 / G
    sol = solve_ivp(rhs, [math.log(t0), math.log(tend)], [phi0, 0.0, math.log(rr0)], method="LSODA", rtol=1e-7, atol=[1e-12 * Mp, 1e-12 * Mp * m, 1e-10], max_step=0.01, dense_output=False)
    # entropy comparison: a^3 rho_r^{3/4} at the end vs the no-modulus case; track a via int H dt
    ts = np.exp(sol.t); phi, v, rr = sol.y[0], sol.y[1], np.exp(sol.y[2])
    rho = 0.5 * v * v + 0.5 * m * m * phi * phi + rr; H = np.sqrt(rho / 3) / Mp
    lna = np.concatenate([[0], np.cumsum(0.5 * (H[1:] + H[:-1]) * np.diff(ts))])
    S_end = math.exp(3 * lna[-1]) * rr[-1] ** 0.75; S_0 = rr0 ** 0.75
    return S_end / S_0, sol.success
if __name__ == "__main__":
    est = {(1e9, 1.0): 1.5e9, (1e9, 1e-3): 1.5e3, (1e13, 1.0): 1.5e3, (1e13, 1e-3): 1.0}
    for (m, A), e in est.items():
        try:
            D, ok = run(m, A); print(f"m {m:.0e}, A {A}: numerical dilution {D:.2e} (D359 est {e:.1e}); ratio {D/e:.2f}; ok {ok}", flush=True)
        except Exception as ex:
            print(f"m {m:.0e}, A {A}: FAILED {type(ex).__name__}: {ex}", flush=True)
