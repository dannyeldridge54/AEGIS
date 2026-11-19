"""D1644 / Janus genesis G9+G2b: future of the exact-shape reverse thread (PREREG_D1644_G9_THREAD_FUTURE)."""
import json, math, sys
sys.path.insert(0, '.')
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
from tools.serapis_calc import p3s
Om, Or, A, b, C = 0.31, 9e-5, 16 * math.pi ** 2 / 6 / (3 * 1.2020569031595942), 2 * math.sqrt(2), 8e-7
phr = math.log(float(p3s.YRHO)) / math.sqrt(2)
ph = np.linspace(math.log(0.45) / math.sqrt(2), math.log(3000.0) / math.sqrt(2), 9000)
fv = p3s.V_np(ph, C, 10); Sp = CubicSpline(ph, fv); dS = Sp.derivative()
f = lambda p: float(Sp(p)); df = lambda p: float(dS(p))
amp = json.load(open('field_tests/results/D1638_G2_thread_shape.json'))['best']['amp']
phii = -math.log(amp / A) / b
def rhs_f(VL):
    def rhs(N, s):
        p, q = s; a = math.exp(N); rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4
        H2 = (rm + rr + VL * f(p)) / (3 - q * q / 2); eps = (rm + 4 * rr / 3 + H2 * q * q) / (2 * H2)
        return [q, -(3 - eps) * q - VL * df(p) / H2]
    return rhs
def H2today(VL):
    s = solve_ivp(rhs_f(VL), (math.log(1e-3), 0), [phii, 0.0], rtol=1e-9, atol=1e-12)
    p, q = s.y[:, -1]; return (3 * Om + 3 * Or + VL * f(p)) / (3 - q * q / 2)
grid = [0.5 * 2 ** k for k in range(15)]; vals = [H2today(v) - 1 for v in grid]
VL = next(brentq(lambda v: H2today(v) - 1, lo, hi, xtol=1e-12) for lo, hi, x, y in zip(grid, grid[1:], vals, vals[1:]) if x < 0 < y)
sol = solve_ivp(rhs_f(VL), (math.log(1e-3), math.log(50.0)), [phii, 0.0], rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.002)
N = np.linspace(-0.0, math.log(50.0), 40001)
P, Q = sol.sol(N)
a = np.exp(N); rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4; Vv = VL * np.array([f(p) for p in P])
H2 = (rm + rr + Vv) / (3 - Q * Q / 2); K = 0.5 * H2 * Q * Q; rho_t = K + Vv; w = (K - Vv) / (K + Vv)
rho_tot = rm + rr + rho_t; p_tot = rr / 3 + (K - Vv)
acc = -(rho_tot + 3 * p_tot)          # sign of a''/a (∝ −(ρ + 3p))
Om_t = rho_t / rho_tot
def first(mask):
    i = np.argmax(mask); return (i if mask[i] else None)
i_acc = first((acc < 0) & (N > 0)); i_rho = first(P <= phr); i_w0 = first((w >= 0) & (N > 0))
pick = lambda i: None if i is None else dict(a=float(a[i]), Omega_thread=float(Om_t[i]))
late = N >= 0.8 * N[-1]; wbar = float(np.sum(w[late] * rho_t[late]) / np.sum(rho_t[late]))
i25 = np.argmin(abs(a - 25)); i50 = len(a) - 1
# a^3 rho averaged over one local window to smooth oscillation
def avg_a3rho(i, half=400): s = slice(max(0, i - half), min(len(a), i + half)); return float(np.mean(a[s] ** 3 * rho_t[s]))
ratio = avg_a3rho(i50 - 400) / avg_a3rho(i25)
n_cross = int(np.sum(np.diff(np.sign(P - phr)) != 0))
R1 = abs(wbar) <= 0.05 and abs(ratio - 1) <= 0.10; R2 = i_acc is not None
out = dict(D='D1644', amp=amp, VL=VL, today=dict(w=float(w[0]), Omega_thread=float(Om_t[0])),
           end_of_acceleration=pick(i_acc), reaches_rho=pick(i_rho), w_first_zero=pick(i_w0),
           late_w_mean=wbar, a3rho_ratio_50_over_25=ratio, Omega_thread_a50=float(Om_t[-1]), rho_crossings=n_cross,
           m_over_H_at_a50=float(math.sqrt(VL / 4) / math.sqrt(H2[-1])), m_over_HLambda=float(math.sqrt(VL / 4) / math.sqrt(VL / 3)),
           R1_matter_like='PASS' if R1 else 'FAIL', R2_acceleration_ends='PASS' if R2 else 'FAIL')
json.dump(out, open('field_tests/results/D1644_G9_thread_future.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
