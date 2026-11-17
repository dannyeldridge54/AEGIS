"""S4c2 (locked PREREG_S4c2_kk_pruefer)."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def theta_end(m2, p, w, a, b):
    s = solve_ivp(lambda y, t: [math.cos(t[0])**2/p(y) + m2*w(y)*math.sin(t[0])**2], [a, b], [math.pi/2], method='Radau', rtol=1e-10, atol=1e-12)
    return s.y[0][-1]
def eig(n, p, w, a, b, lo, hi):
    f = lambda m2: theta_end(m2, p, w, a, b) - math.pi/2 - n*math.pi
    # bracket by scanning
    grid = np.geomspace(lo, hi, 60); vals = [f(g) for g in grid]
    for x0, x1, v0, v1 in zip(grid, grid[1:], vals, vals[1:]):
        if v0*v1 < 0: return brentq(f, x0, x1, xtol=1e-14, rtol=1e-12)
    return None
L = []
one = lambda y: 1.0; ok = True
for n in (1, 2, 3):
    m2 = eig(n, one, one, 0.0, 2.0, 1e-3, 1e3); ex = (n*math.pi/2)**2; e = abs(m2/ex - 1); ok &= e <= 1e-6
    L.append(f"V flat L=2 n={n}: m^2 = {m2:.10f} vs {ex:.10f} ({e:.1e})")
L.append(f"V {'PASS' if ok else 'FAIL'}")
D, g = 6, 2.0; gc = 4*math.sqrt(D-1)/(D-2); dl = (g/gc - 1)/2; wq = math.sqrt(-dl*(dl+1)); k = math.sqrt(2*(D-1)/(D-2)); yend = math.pi/2/(wq*k)
A = lambda y: -1/(2*(D-1))*(math.log(math.cos(wq*k*y))/dl - math.log(math.sin(wq*k*y))/(dl+1))
P = lambda y: (D-2)/(4*math.sqrt(D-1))*(math.log(math.cos(wq*k*y))/dl + math.log(math.sin(wq*k*y))/(dl+1))
p = lambda y: math.exp((D-1)*A(y) + g*P(y)/2); w = lambda y: math.exp((D-3)*A(y) - g*P(y)/2)
res = {}
for ef in (1e-3, 1e-4, 1e-5):
    a, b = ef*yend, (1-ef)*yend
    m0 = theta_end(0.0, p, w, a, b) - math.pi/2
    ms = [eig(n, p, w, a, b, 1e-4, 1e4) for n in (1, 2, 3)]; res[ef] = (m0, ms)
    L.append(f"6D eps={ef:g}: theta_end(m^2=0) - pi/2 = {m0:.2e}; m^2_1..3 = {ms}")
    print(L[-1], flush=True)
m1 = [res[e][1][0] for e in res if res[e][1][0] is not None]
T1 = all(abs(res[e][0]) <= 1e-3 for e in res)       # zero mode: theta stays at pi/2 for m^2 = 0
T2 = len(m1) == 3 and (max(m1) - min(m1))/m1[-1] <= 1e-3; T3 = len(m1) == 3 and min(m1) > 0
L.append(f"T1 zero mode (theta_end - pi/2 at m^2=0 small): {'PASS' if T1 else 'FAIL'}; T2 m1^2 converged: {'PASS' if T2 else 'FAIL'}; T3 m1^2 > 0: {'PASS' if T3 else 'FAIL'}")
if ok and T1 and T2 and T3:
    m = res[1e-5][1]; L.append(f"S4c2 VALID: m1 = {math.sqrt(m[0]):.5f} sqrt(alpha_E); m2/m1 = {math.sqrt(m[1]/m[0]):.4f}; m3/m1 = {math.sqrt(m[2]/m[0]):.4f}")
else: L.append("S4c2 NOT VALID")
open('field_tests/results/s4c2_kk.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
