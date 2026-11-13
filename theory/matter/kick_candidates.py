"""D30: test the two remaining sources for the angle's kick (Development 29). AI-assisted, order of magnitude + toy run.
(b) THERMAL: the angle couples only through d(theta) J5, so the plasma gives friction, not a potential. The only thermal
    potential is from instantons via the anomaly, chi(T) ~ Lambda^4 (Lambda/T)^8 (dilute instanton gas, QCD-like, Lambda =
    0.2 GeV), further suppressed by c_A/M_P. Compared with the potential the kick needs, V_kick ~ r (H M_P)^2 at T = 1e13 GeV.
(a) HIDDEN AXION MIXING: a separate field sigma with V = m^2 sigma^2/2 + L^4 [1 - cos(theta_c/F - sigma/f)], F = 1.559 M_P
    (Nieh-Yan), released when H ~ m in a radiation era. Its potential is not a dilaton instanton (a D-term or sequestered
    sector, so no exp(K) growth). Estimate: r ~ Omega_h M_P/F, Omega_h = hidden potential's energy fraction at release.
    Toy run below checks it (radiation background, dilaton frozen)."""
import math
import numpy as np
from scipy.integrate import solve_ivp
MP, MPL, gs = 2.435e18, 1.221e19, 106.75
T = 1e13; H = 1.66 * math.sqrt(gs) * T * T / MPL; r_need = 0.022
Lq = 0.2; chi = Lq ** 4 * (Lq / T) ** 8; cA = math.sqrt(3 / 8)
V_need = r_need * (H * MP) ** 2
print(f"(b) thermal: instanton potential ~ {chi * cA:.1e} GeV^4 vs needed ~ {V_need:.1e} GeV^4 -> short by 10^{math.log10(V_need / (chi * cA)):.0f}")

F = 1.559
def toy(Omega_h, f=0.1, sig0=1.0):
    # units: M_P = 1, time in 1/m (m = 1); radiation era H = 1/(2t); release at t = 1/2 (H = m)
    L4 = 3 * Omega_h * (0.5 / 0.5) ** 2 / 1.0           # Omega_h = L^4 / (3 H^2) at H = 1
    def rhs(t, z):
        th, sg, dth, dsg = z; Hh = 1 / (2 * t); arg = th / F - sg / f
        dV_th = L4 * math.sin(arg) / F; dV_sg = sg - L4 * math.sin(arg) / f
        return [dth, dsg, -3 * Hh * dth - dV_th, -3 * Hh * dsg - dV_sg]
    t0 = 0.05; sol = solve_ivp(rhs, [t0, 20], [0.0, sig0 * f, 0, 0], rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.01)
    ts = np.linspace(0.5, 20, 400); r = [abs(sol.sol(t)[2]) / (1 / (2 * t)) for t in ts]   # r = thetadot_c / (H M_P)
    return max(r), r[0]
print("(a) hidden axion mixing (toy, radiation era):")
for Om in (0.003, 0.01, 0.03, 0.1):
    rmax, r1 = toy(Om)
    print(f"   hidden energy fraction {Om:5.3f}: peak angle speed r = {rmax:.3f}  (estimate Omega_h M_P/F = {Om / F:.3f}; need ~0.02)")
