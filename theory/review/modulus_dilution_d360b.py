"""D360 T2 (PREREG_D360_TESTS + D1): averaged modulus + radiation with decay, from H = m. Units GeV, reduced M_P. AI-assisted."""
import math
from scipy.integrate import solve_ivp
Mp = 2.435e18
def run(m, A):
    G = m ** 3 / (8 * math.pi * Mp ** 2)
    rho_tot = 3 * m * m * Mp * Mp; rp0 = min(0.5 * m * m * (A * Mp) ** 2, 0.5 * rho_tot); rr0 = rho_tot - rp0
    def rhs(N, y):
        lp, lr = y; rp, rr = math.exp(lp), math.exp(lr)
        H = math.sqrt((rp + rr) / 3) / Mp; g = G / H
        return [-3 - g, -4 + g * rp / rr]
    ev = lambda N, y: math.exp(y[0]) / math.exp(y[1]) - 1e-12; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, [0, 400], [math.log(rp0), math.log(rr0)], method="LSODA", rtol=1e-9, atol=1e-12, events=ev)
    N = sol.t[-1]; rr = math.exp(sol.y[1][-1])
    return math.exp(3 * N) * rr ** 0.75 / rr0 ** 0.75, sol.status
if __name__ == "__main__":
    est = {(1e9, 1.0): 1.5e9, (1e9, 1e-3): 1.5e3, (1e13, 1.0): 1.5e3, (1e13, 1e-3): 1.0}
    for (m, A), e in est.items():
        D, st = run(m, A)
        print(f"m {m:.0e}, A {A}: numerical dilution {D:.2e} (D359 est {e:.1e}); ratio {D/e:.2f}; status {st}")
