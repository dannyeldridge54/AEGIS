"""A3d — PREREG_A3d_ns_surface.md"""
import sys; sys.path.insert(0, '.')
from tools.janus_astro import ns, compact
out = []; rel = lambda a, b: abs(a-b)/abs(b)
eos = ns.PPEOS(*ns.TABLE3['SLy'])
def rho_of_P_SI(Psi):
    if Psi <= 0: return 0.0
    return eos.rho_eps(Psi*10.0)[1]*1000.0
def P_SI(rho):
    i = 0
    for j in range(len(eos.p)):
        if rho >= eos.p[j][2]: i = j
    return eos.p[i][0]*rho**eos.p[i][1]*ns.C**2/10.0
ps = P_SI(1e4); ok = True; out.append(f"p_surf(rho=1e4 g/cc) = {ps:.4e} Pa")
for lr in (14.8, 15.0, 15.2):
    M1, R1 = ns.tov_tidal(eos, 10**lr, rho_surf=1e4)[:2]
    R2, M2 = compact.tov(rho_of_P_SI, P_SI(10**lr), r_max=5e4, rtol=1e-11, p_surf=ps); M2 /= 1.98840987e30; R2 /= 1e3
    R0 = ns.tov_tidal(eos, 10**lr, rho_surf=1e-3)[1]
    e1, e2 = rel(M1, M2), rel(R1, R2); ok &= max(e1, e2) <= 1e-7
    out.append(f"N4' log rho_c={lr}: ns M={M1:.8f} R={R1:.7f} | compact M={M2:.8f} R={R2:.7f} | rel {e1:.1e} {e2:.1e} | surface sensitivity R(P->0)-R(1e4) = {(R0-R1)*1e3:.2f} m")
out.append(f"A3d {'VALIDATED' if ok else 'NOT VALIDATED'} (N4' {ok})")
open('field_tests/results/janus_astro_a3d.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
