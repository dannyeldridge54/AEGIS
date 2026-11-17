"""S4c (locked PREREG_S4c_kk_probe)."""
import math, numpy as np
from scipy.linalg import eigh
D, g = 6, 2.0; gc = 4*math.sqrt(D-1)/(D-2); dl = (g/gc - 1)/2; w = math.sqrt(-dl*(dl+1)); k = math.sqrt(2*(D-1)/(D-2))
yend = math.pi/2/(w*k)
def A(y): xi = k*y; return -1/(2*(D-1))*(math.log(math.cos(w*xi))/dl - math.log(math.sin(w*xi))/(dl+1))
def P(y): xi = k*y; return (D-2)/(4*math.sqrt(D-1))*(math.log(math.cos(w*xi))/dl + math.log(math.sin(w*xi))/(dl+1))
def spectrum(epsf, N):
    a, b = epsf*yend, (1-epsf)*yend; y = np.linspace(a, b, N); h = y[1]-y[0]
    pf = lambda t: math.exp((D-1)*A(t) + g*P(t)/2)          # e^{(D-1)A - B}, B = -g phi/2
    wf = lambda t: math.exp((D-3)*A(t) - g*P(t)/2)           # e^{(D-3)A + B}
    pm = np.array([pf(t + h/2) for t in y[:-1]])              # p at half points
    K = np.zeros((N, N)); M = np.diag([wf(t) for t in y])*h
    for i in range(N-1):
        K[i, i] += pm[i]/h; K[i+1, i+1] += pm[i]/h; K[i, i+1] -= pm[i]/h; K[i+1, i] -= pm[i]/h
    ev = eigh(K, M, eigvals_only=True, subset_by_index=[0, 3])
    return ev
L = [f"6D vacuum: delta = {dl:.6f}, y_end = {yend:.6f}"]; res = {}
for epsf in (1e-3, 2e-4, 4e-5):
    for N in (2000, 4000):
        ev = spectrum(epsf, N); res[(epsf, N)] = ev
        L.append(f"eps={epsf:g} N={N}: m^2 = " + ", ".join(f"{e:.6e}" for e in ev)); print(L[-1], flush=True)
ref = res[(4e-5, 4000)]; m1 = [res[k][1] for k in res]
T1 = abs(ref[0]) <= 1e-8*ref[1]; T2 = (max(m1) - min(m1))/ref[1] <= 1e-3; T3 = all(min(v) >= -1e-10*ref[1] for v in res.values())
L.append(f"T1 zero mode {ref[0]:.2e} vs m1^2 {ref[1]:.4e}: {'PASS' if T1 else 'FAIL'}; T2 m1^2 spread {(max(m1)-min(m1))/ref[1]:.1e}: {'PASS' if T2 else 'FAIL'}; T3 no negative: {'PASS' if T3 else 'FAIL'}")
L.append(f"probe {'VALID' if (T1 and T2 and T3) else 'NOT VALID'}: m1 = {math.sqrt(ref[1]):.5f} sqrt(alpha_E), m2/m1 = {math.sqrt(ref[2]/ref[1]):.4f}, m3/m1 = {math.sqrt(ref[3]/ref[1]):.4f}")
open('field_tests/results/s4c_kk.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-2:]))
