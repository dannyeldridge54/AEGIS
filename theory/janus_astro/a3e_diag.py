import sys, math; sys.path.insert(0, '.')
from scipy.integrate import solve_ivp
from tools.janus_astro import ns, compact
G, c = compact.G, compact.c
eos = ns.PPEOS(*ns.TABLE3['SLy'])
def rho_of_P_SI(Psi): return 0.0 if Psi <= 0 else eos.rho_eps(Psi*10.0)[1]*1000.0
def P_SI(rho):
    i = 0
    for j in range(len(eos.p)):
        if rho >= eos.p[j][2]: i = j
    return eos.p[i][0]*rho**eos.p[i][1]*ns.C**2/10.0
def tov_tight(P_c, p_surf, rtol=1e-11):
    def rhs(r, y):
        P, m = y; rho = rho_of_P_SI(max(P, 0.0))
        return [-G*(rho + P/c**2)*(m + 4*math.pi*r**3*P/c**2)/(r*r*(1 - 2*G*m/(r*c*c))), 4*math.pi*r*r*rho]
    r0 = 1e-3; ev = lambda r, y: y[0] - p_surf; ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, [r0, 5e4], [P_c, 4/3*math.pi*r0**3*rho_of_P_SI(P_c)], method='DOP853', rtol=rtol, atol=[P_c*1e-30, 1e-30], events=ev)
    return float(s.t_events[0][0]), float(s.y_events[0][0][1])
ps = P_SI(1e4); out = []; ok = True
for lr in (14.8, 15.0, 15.2):
    Pc = P_SI(10**lr); Mn, Rn = ns.tov_tidal(eos, 10**lr, rho_surf=1e4)[:2]
    Rs, Ms = compact.tov(rho_of_P_SI, Pc, r_max=5e4, rtol=1e-11, p_surf=ps); Rt, Mt = tov_tight(Pc, ps)
    es, et = abs(Rs/1e3/Rn - 1), abs(Rt/1e3/Rn - 1)
    ok &= et <= 1e-8 and (lr == 14.8 or es >= 1e-6)
    out.append(f"log rho_c={lr}: P_c={Pc:.3e} Pa atol_P/p_surf={Pc*1e-16/ps:.2f} | R ns {Rn:.8f} km | compact shipped {Rs/1e3:.8f} (rel {es:.1e}) | compact tight {Rt/1e3:.8f} (rel {et:.1e}); M tight {Mt/1.98840987e30:.8f}")
out.append("HYPOTHESIS " + ("CONFIRMED" if ok else "NOT CONFIRMED"))
open('field_tests/results/janus_astro_a3e.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
