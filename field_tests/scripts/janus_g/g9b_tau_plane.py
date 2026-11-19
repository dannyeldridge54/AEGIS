"""D1653 / Janus genesis G9b: dark thread in the full tau plane (PREREG_D1653_G9B_TAU_PLANE)."""
import json, math, sys
sys.path.insert(0, '.')
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import k0, k1
from scipy.special import zeta as Z
Om, Or, b2, C = 0.31, 9e-5, 2.0, 8e-7
A0, B0 = 2 * Z(3), 4 * Z(2)
PREF = 8 * math.pi ** 1.5 / math.gamma(1.5)
NN = np.arange(1, 41); SIG = np.array([sum(d ** -2.0 for d in range(1, n + 1) if n % d == 0) for n in NN])
CN = PREF * NN * SIG
def EdE(x, y):
    a = 2 * math.pi * NN * y; m = a < 80
    sq = math.sqrt(y); K1, K0 = k1(a[m]), k0(a[m]); c = CN[m]
    cs, sn = np.cos(2 * math.pi * NN[m] * x), np.sin(2 * math.pi * NN[m] * x)
    E = A0 * y ** 1.5 + B0 * y ** -0.5 + np.sum(c * cs * sq * K1)
    Ey = 1.5 * A0 * y ** 0.5 - 0.5 * B0 * y ** -1.5 + np.sum(c * cs * (K1 / (2 * sq) + sq * (-(K0 + K1 / a[m]) * 2 * math.pi * NN[m])))
    Ex = np.sum(c * (-2 * math.pi * NN[m] * sn) * sq * K1)
    return E, Ex, Ey
ER = EdE(0.5, math.sqrt(3) / 2)[0]
def Vfun(x, y):
    E, Ex, Ey = EdE(x, y); return 4 / 9 * y * y * ((Ex / E) ** 2 + (Ey / E) ** 2) * (1 + C * (E - ER))
def gradV(x, y, h=1e-6):
    return ((Vfun(x + h, y) - Vfun(x - h, y)) / (2 * h), (Vfun(x, y * (1 + h)) - Vfun(x, y * (1 - h))) / (2 * h * y))
A = 16 * math.pi ** 2 / 6 / (3 * Z(3))
amp = json.load(open('field_tests/results/D1638_G2_thread_shape.json'))['best']['amp']
y0 = math.sqrt(A / amp)
def rhs_f(VL):
    def rhs(N, s):
        x, y, u, v = s; a = math.exp(N); rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4
        G = 1 / (b2 * y * y); s2 = G * (u * u + v * v)
        V = VL * Vfun(x, y); H2 = (rm + rr + V) / (3 - s2 / 2); eps = (rm + 4 * rr / 3 + H2 * s2) / (2 * H2)
        Vx, Vy = gradV(x, y)
        du = -(3 - eps) * u - (-2 / y) * u * v - b2 * y * y * VL * Vx / H2
        dv = -(3 - eps) * v - (1 / y) * u * u - (-1 / y) * v * v - b2 * y * y * VL * Vy / H2
        return [u, v, du, dv]
    return rhs
def H2today(VL, x0):
    s = solve_ivp(rhs_f(VL), (math.log(1e-3), 0), [x0, y0, 0, 0], rtol=1e-9, atol=1e-12)
    x, y, u, v = s.y[:, -1]; s2 = (u * u + v * v) / (b2 * y * y); return (3 * Om + 3 * Or + VL * Vfun(x, y)) / (3 - s2 / 2)
def fd(x, y):   # map to fundamental domain
    t = complex(x, y)
    for _ in range(200):
        t = complex(t.real - math.floor(t.real + 0.5), t.imag)
        if abs(t) < 1 - 1e-12: t = -1 / t
        else: break
    return t
runs = {}
for dx in (0.0, 1e-6, 1e-3, 1e-2):
    x0 = 0.5 + dx
    grid = [0.5 * 2 ** k for k in range(12)]; vals = [H2today(g, x0) - 1 for g in grid]
    VL = next(brentq(lambda g: H2today(g, x0) - 1, lo, hi, xtol=1e-10) for lo, hi, p, q in zip(grid, grid[1:], vals, vals[1:]) if p < 0 < q)
    sol = solve_ivp(rhs_f(VL), (math.log(1e-3), math.log(50.0)), [x0, y0, 0, 0], rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.004)
    N = np.linspace(0, math.log(50.0), 12001); X, Y, U, Vv = sol.sol(N); a = np.exp(N)
    rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4; Vp = VL * np.array([Vfun(x, y) for x, y in zip(X, Y)])
    s2 = (U * U + Vv * Vv) / (b2 * Y * Y); H2 = (rm + rr + Vp) / (3 - s2 / 2); K = 0.5 * H2 * s2; rt = K + Vp
    w = (K - Vp) / (K + Vp); acc = -(rm + rr + rt + 3 * (rr / 3 + K - Vp))
    i_acc = int(np.argmax((acc < 0) & (N > 0)))
    late = N >= 0.8 * N[-1]; xm, ym = float(np.mean(X[late])), float(np.mean(Y[late]))
    t = fd(xm, ym); di, dr = abs(t - 1j), min(abs(t - complex(0.5, math.sqrt(3) / 2)), abs(t - complex(-0.5, math.sqrt(3) / 2)))
    cls = 'i-class' if di < 0.02 else ('rho-class' if dr < 0.02 else 'other')
    runs[str(dx)] = dict(VL=VL, a_end_acc=float(a[i_acc]), late_tau=[xm, ym], fundamental=[t.real, t.imag], dist_i=di, dist_rho=dr, end_class=cls,
                         max_dx=float(np.max(np.abs(X - 0.5))), late_w=float(np.sum(w[late] * rt[late]) / np.sum(rt[late])))
r0 = runs['0.0']; R0 = abs(r0['a_end_acc'] / 1.232 - 1) < 0.01 and abs(r0['late_tau'][1] / 0.5 - 1) < 0.02
pert = [runs[k] for k in ('1e-06', '0.001', '0.01')]
verdict = 'ROBUST' if all(r['end_class'] == 'i-class' for r in pert) else 'FRAGILE'
out = dict(D='D1653', R0_code_check='PASS' if R0 else 'FAIL', runs=runs, verdict=verdict if R0 else 'INVALID (R0 failed)')
json.dump(out, open('field_tests/results/D1653_G9b_tau_plane.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
