import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
def Jann(rho, r0): return J.J_route_B(rho, r0, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, r0, psi_max_deg=0.5, b_mask_deg=0.0)
Jb = Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178), 8.178)
S1 = abs(Jb/2.5e22 - 1) <= 0.10
out = [f"S1 benchmark J(0.5-3.0 deg) = {Jb:.3e} vs 2.5e22 ({Jb/2.5e22-1:+.3f}) -> {'PASS' if S1 else 'FAIL'}"]
hal = {'IGS benchmark': 1.0, 'McMillan17': Jann(J.normalise(J.nfw(19.60), 0.385, 8.21), 8.21)/Jb, 'MWPotential2014': Jann(J.normalise(J.nfw(16.0), 0.286, 8.0), 8.0)/Jb}
CONV = 0.389379e-27*2.99792458e10; M = 1000.0; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(M, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv0 = 2*s[1]**2*math.pi*N.ALPHA**2/M**2*CONV*k
    for h, jr in hal.items():
        f = [math.sqrt(2.3e-28/(sv0*R*jr)) for R in (0.794, 0.658)]
        v = 'PASS' if f[0] >= 0.26 else ('FAIL' if f[1] < 0.26 else 'BAND-DEPENDENT')
        out.append(f"{lab} {h}: J ratio {jr:.3f}; sv_line(tree-SE) {sv0:.3e}; f_max [{f[0]:.3f}, {f[1]:.3f}] -> {v}")
open('field_tests/results/a2h_igs_J.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
