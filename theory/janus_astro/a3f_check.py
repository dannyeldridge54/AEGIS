import sys; sys.path.insert(0, '.')
from tools.janus_astro import ns, compact
rel = lambda a, b: abs(a-b)/abs(b)
eos = ns.PPEOS(*ns.TABLE3['SLy'])
def rho_of_P_SI(Psi): return 0.0 if Psi <= 0 else eos.rho_eps(Psi*10.0)[1]*1000.0
def P_SI(rho):
    i = 0
    for j in range(len(eos.p)):
        if rho >= eos.p[j][2]: i = j
    return eos.p[i][0]*rho**eos.p[i][1]*ns.C**2/10.0
out = []; f1 = f2 = True
for lr in (14.8, 15.0, 15.2):
    for tag, rs, ps, tol in (('F1', 1e4, P_SI(1e4), 1e-7), ('F2', 1e-3, 0.0, 1e-6)):
        M1, R1 = ns.tov_tidal(eos, 10**lr, rho_surf=rs)[:2]
        R2, M2 = compact.tov(rho_of_P_SI, P_SI(10**lr), r_max=5e4, rtol=1e-11, p_surf=ps); M2 /= 1.98840987e30; R2 /= 1e3
        e = max(rel(M1, M2), rel(R1, R2)); ok = e <= tol
        if tag == 'F1': f1 &= ok
        else: f2 &= ok
        out.append(f"{tag} log rho_c={lr}: ns M={M1:.8f} R={R1:.7f} | compact M={M2:.8f} R={R2:.7f} | worst rel {e:.1e} (tol {tol:g}) {'PASS' if ok else 'FAIL'}")
out.append(f"F1 {f1} F2 {f2}")
open('field_tests/results/janus_astro_a3f.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
