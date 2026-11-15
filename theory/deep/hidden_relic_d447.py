"""D447 (locked PREREG_D447_HIDDEN_RELIC): hidden-bath freeze-out of the lightest D7-charged scalar. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.special import kve
from scipy.optimize import brentq
gs, gh, g, MPl = 106.75, 10.0, 2.0, 1.22e19
def omega(m, lam, xi):
    sv = lam**4/(16*math.pi*m*m)
    def lnYeq(x):                       # x = m/T
        xh = x/xi; T = m/x
        # n_eq = g m^2 T_h K2(xh)/(2pi^2); K2 = kve*e^{-xh}
        ln_n = math.log(g*m*m*xi*T/(2*math.pi**2)) + math.log(kve(2, xh)) - xh
        return ln_n - math.log(2*math.pi**2/45*gs*T**3)
    lam_c = lambda x: (2*math.pi**2/45*gs*(m/x)**3)*sv/(1.66*math.sqrt(gs)*(m/x)**2/MPl*x)   # s sv/(H x)
    def rhs(x, u):                      # u = ln Y
        Y = math.exp(u[0]); Ye = math.exp(lnYeq(x))
        return [-lam_c(x)*(Y*Y - Ye*Ye)/Y]
    x0 = 0.5*xi                          # x_h = 0.5: relativistic, start at equilibrium
    s = solve_ivp(rhs, [x0, 2000*xi + 50], [lnYeq(x0)], method='Radau', rtol=1e-8, atol=1e-10)
    return 2.74e8*m*math.exp(s.y[0, -1])
for eps in (1e-5, 1e-3):
    xi = (eps*gs/gh)**0.25
    print(f"eps_h={eps:.0e}: xi=T_h/T={xi:.3f}", flush=True)
    for m in (10, 100, 1e3, 1e4, 1e5):
        o1 = omega(m, 1.0, xi); out = []
        for tgt in (0.12, 0.0012):
            fn = lambda L: math.log(omega(m, L, xi)/tgt)
            try: out.append(brentq(fn, 1e-4, 30, xtol=1e-4))
            except ValueError: out.append(float('nan'))
        print(f"  m={m:.0e} GeV: Omega h2(lam=1)={o1:.2e}; lam(100% DM)={out[0]:.3f}; lam(1% DM)={out[1]:.3f}; "
              f"perturbative: 100% {'yes' if out[0]<=3.54 else 'no'}, 1% {'yes' if out[1]<=3.54 else 'no'}", flush=True)
