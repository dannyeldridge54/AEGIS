import math, sys, numpy as np
sys.path.insert(0, '.')
from tools.janus_astro import ns, compact
out = []; P = lambda *a: (out.append(' '.join(str(x) for x in a)), print(*a, flush=True))
rel = lambda a, b: abs(a-b)/abs(b)
# N1: single n=1 polytrope, eps = rho (no internal energy term) to match the Newtonian n = 1 problem
class Poly:
    def __init__(self, K): self.p = [[K, 2.0, 0.0]]; self.a = [0.0]; self.pb = [0.0]; self.K = K
    def rho_eps(self, P): rho = (P/ns.C**2/self.K)**0.5; return rho, rho, 2.0
    # (A3b: Poly keeps dyn units; ns.tov_tidal converts Pc with C^2, so K here is given in p/c^2 units)
e = Poly(1e5/ns.C**2); e.pb=[0.0]            # cgs; with rho_c = 1e10 g/cc the compactness is ~1e-6
M, R, k2, Lam, Cc, y = ns.tov_tidal(e, 1e10)
k2N = (15 - math.pi**2)/(2*math.pi**2); yN = (2 - 6*k2N)/(1 + 2*k2N)
ok1 = abs(y - yN) <= 1e-3; P(f'N1 n=1 weak field: C={Cc:.2e} y_R={y:.6f} vs Newtonian {yN:.6f} |dy|={abs(y-yN):.1e}', 'PASS' if ok1 else 'FAIL')
res = {}
ok2 = ok3 = True
for name, (Mt, Rt) in [('SLy', (2.049, 11.736)), ('AP4', (2.213, 11.428))]:
    eos = ns.PPEOS(*ns.TABLE3[name]); Mmax, rhom, _ = ns.max_mass(eos); s = ns.at_mass(eos, 1.4)
    ok = rel(Mmax, Mt) <= 1.5e-2 and rel(s[1], Rt) <= 1.5e-2
    if name == 'SLy': ok2 = ok
    else: ok3 = ok
    res[name] = (eos, s)
    P(f'N{2 if name=="SLy" else 3} {name}: M_max={Mmax:.4f} (vs {Mt}, {rel(Mmax,Mt):.1e}) at rho_c={rhom:.3e}; R_1.4={s[1]:.4f} km (vs {Rt}, {rel(s[1],Rt):.1e}); k2_1.4={s[2]:.4f} Lambda_1.4={s[3]:.1f} C={s[4]:.4f}', 'PASS' if ok else 'FAIL')
eos = res['SLy'][0]; ok4 = True
def rho_of_P_SI(Psi):
    if Psi <= 0: return 0.0
    return eos.rho_eps(Psi*10.0)[1]*1000.0          # Pa -> dyn/cm^2; g/cc -> kg/m^3 (energy density / c^2)
for lr in (14.8, 15.0, 15.2):
    M1, R1 = ns.tov_tidal(eos, 10**lr, rho_surf=1e-3)[:2]   # A3c: common surface (P -> 0)
    i = 0
    for j in range(len(eos.p)):
        if 10**lr >= eos.p[j][2]: i = j
    Pc = eos.p[i][0]*(10**lr)**eos.p[i][1]*ns.C**2/10.0     # dyn/cm^2 -> Pa (A3b units)
    R2, M2 = compact.tov(rho_of_P_SI, Pc, r_max=5e4, rtol=1e-11)
    M2 /= 1.98840987e30; R2 /= 1e3
    e1, e2 = rel(M1, M2), rel(R1, R2); ok4 &= max(e1, e2) <= 1e-5
    P(f'N4 SLy log rho_c={lr}: ns M={M1:.6f} R={R1:.5f} | compact.tov M={M2:.6f} R={R2:.5f} | rel {e1:.1e} {e2:.1e}')
P('A3c', 'VALIDATED' if ok1 and ok2 and ok3 and ok4 else 'NOT VALIDATED', f'(N1 {ok1}, N2 {ok2}, N3 {ok3}, N4 {ok4})')
# A3c data comparisons
P('Reported: GW170817 Lambda_1.4 = 190 (+390/-120, 90%):', ', '.join(f'{n} {res[n][1][3]:.0f}' for n in res))
P('Data comparison (EoS vs measurements; not code validation):')
for n in res:
    eos_n = res[n][0]; Mmax = ns.max_mass(eos_n)[0]
    L = res[n][1][3]; P(f'  {n}: GW170817 Lambda_1.4={L:.0f} in 90% [70, 580]: {70 <= L <= 580}')
    Mt = min(2.08, Mmax - 1e-4); R0740 = ns.at_mass(eos_n, Mt)[1]
    P(f'  {n}: J0740+6620 (M 2.08+-0.07, R 12.92 -1.13/+2.09 at 68%): M_max={Mmax:.3f} >= 2.01: {Mmax >= 2.01}; R({Mt:.3f})={R0740:.2f} km in 68% [11.79, 15.01]: {11.79 <= R0740 <= 15.01}; in 2x68% [10.66, 17.10]: {10.66 <= R0740 <= 17.10}')
    R0614 = ns.at_mass(eos_n, 1.44)[1]
    P(f'  {n}: J0614-3329 (M 1.44, R 10.29 +1.01/-0.86 at 68%): R(1.44)={R0614:.2f} km in 68% [9.43, 11.30]: {9.43 <= R0614 <= 11.30}; in 2x68% [8.57, 12.31]: {8.57 <= R0614 <= 12.31}')
P('M-R (SLy):'); 
for row in ns.mr_curve(res['SLy'][0], 14.5, 15.5, 11): P(f'  log rho_c={row[0]:.2f}: M={row[1]:.3f} R={row[2]:.2f} km Lambda={row[4]:.1f}')
open('field_tests/results/janus_astro_a3c.txt', 'w').write('\n'.join(out) + '\n')
