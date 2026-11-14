"""PREREG_TWIST_ALP scan (locked 5cfafeb). Spectator axion a in the Twist background: a'' + (3 + dlnH/dN) a' + (m/H)^2 a = 0 (N = ln a_scale).
beta_X = (g/2)(a_0 - a(z_X)); amplitude normalised to beta_rec = 0.30 deg. R = beta_reion/beta_rec. AI-assisted."""
import math, importlib.util, io, contextlib
import numpy as np
from scipy.integrate import solve_ivp
spec = importlib.util.spec_from_file_location("lp", "/home/claude/aegis/theory/observables/late_predictions_d168.py")
lp = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(lp)
H0_eV = 67.4 / 100 * 2.1332e-33                      # H0 in eV
def E(N):
    a = math.exp(N)
    return math.sqrt(lp.E2(a)) if a >= 1.01e-4 else math.sqrt(lp.Om * a ** -3 + lp.Or * a ** -4)
def dlnE(N, h=1e-4): return (math.log(E(N + h)) - math.log(E(N - h))) / (2 * h)
MP_GeV, alpha_em = 2.435e18, 1 / 137.036
for m in (1e-33, 1e-32, 3e-32, 1e-31, 3e-31, 1e-30, 1e-29, 1e-28):
    mu = m / H0_eV
    rhs = lambda N, y: [y[1], -(3 + dlnE(N)) * y[1] - (mu / E(N)) ** 2 * y[0]]
    s = solve_ivp(rhs, [math.log(1e-4), 0], [1.0, 0.0], rtol=1e-9, atol=1e-12, dense_output=True, method="LSODA")
    a0 = s.y[0, -1]; a_rec = s.sol(math.log(1 / 1091))[0]; a_rei = s.sol(math.log(1 / 8.7))[0]
    d_rec, d_rei = a0 - a_rec, a0 - a_rei
    if abs(d_rec) < 1e-14:
        print(f"m {m:.0e} eV: frozen (no rotation)"); continue
    R = d_rei / d_rec
    # energy fraction today for f = 1e16 GeV: theta_ini chosen so that c * alpha/(2pi) * theta_ini * |d_rec| = 0.30 deg with c = 1;
    beta = math.radians(0.30)
    theta_ini = beta / (alpha_em / (2 * math.pi) * abs(d_rec))           # c = 1
    f_eV = 1e16 * 1e9
    rho_a = 0.5 * (m * f_eV * theta_ini * abs(a0)) ** 2 + 0.5 * (f_eV * theta_ini * H0_eV * s.y[1, -1]) ** 2
    rho_de = 0.69 * 3 * (H0_eV * MP_GeV * 1e9) ** 2
    print(f"m {m:.0e} eV: a(0)/a_ini {a0:+.3f}, R = beta_reion/beta_rec = {R:+.3f}, theta_ini (c=1) = {theta_ini:.2f} rad, "
          f"energy fraction (f=1e16 GeV) = {rho_a / rho_de:.1e}", flush=True)
