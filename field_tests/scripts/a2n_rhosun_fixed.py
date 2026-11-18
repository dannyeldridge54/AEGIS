import sys, math; sys.path.insert(0, '.'); sys.path.insert(0, 'tools/janus_astro')
import warnings; warnings.filterwarnings('ignore')
from tools.janus_astro import jfactor as J, sommerfeld_nlo as N
import serapis_inputs as SI
R0 = 8.178
def Jann(rho, r0): return J.J_route_B(rho, r0, psi_max_deg=3.0, b_mask_deg=0.0) - J.J_route_B(rho, r0, psi_max_deg=0.5, b_mask_deg=0.0)
Jb = Jann(J.normalise(J.einasto(20.0, 0.17), 0.39, 8.178), 8.178)
CONV = 0.389379e-27*2.99792458e10; Mx = 1000.0; k = 1 + N.ALPHA2*N.CW2/N.ALPHA
sv = {}
for lab, nlo in (('LO', False), ('NLO', True)):
    s = N.wino_s_nlo(Mx, v=1e-3, nlo=nlo, off_factor=math.sqrt(2)); sv[lab] = 2*s[1]**2*math.pi*N.ALPHA**2/Mx**2*CONV*k
flo, fhi = SI.wino_fraction(1.0)
halos = [('Bur B0/D1', J.burkert(3.37)), ('Bur B0/D2', J.burkert(3.79)), ('Bur B0/D3', J.burkert(2.91)), ('Bur B0/D4', J.burkert(2.87)), ('Bur B1/D2', J.burkert(4.13)),
         ('Ein B0/D1', J.einasto(15.29, 1.01)), ('Ein B0/D2', J.einasto(14.84, 0.45)), ('Ein B0/D3', J.einasto(16.69, 1.35)), ('Ein B0/D4', J.einasto(14.29, 0.74)), ('Ein B1/D2', J.einasto(15.97, 0.43))]
prev = {'Bur B0/D1': 'PASS', 'Bur B0/D2': 'PASS', 'Bur B0/D3': 'BAND-DEP', 'Bur B0/D4': 'BAND-DEP', 'Bur B1/D2': 'PASS'}
rank = {'PASS': 2, 'BAND-DEP': 1, 'FAIL': 0}; out = [f"f_pred(1 TeV) = [{flo:.3f}, {fhi:.3f}]"]; ok = True
for rs in (0.40, 0.30):
    for tag, shape in halos:
        jr = Jann(J.normalise(shape, rs, R0), R0)/Jb; line = f"rho_sun={rs}: {tag}: J/J_bench={jr:.4f}"
        for lab in ('LO', 'NLO'):
            f = [math.sqrt(2.3e-28/(sv[lab]*R*jr)) for R in (0.794, 0.658)]
            v = 'PASS' if f[0] >= fhi else ('FAIL' if f[1] < flo else 'BAND-DEP')
            line += f"; {lab} f_max [{f[0]:.3f},{f[1]:.3f}] {v}"
            if rs == 0.40 and lab == 'LO' and rank[v] < rank[prev.get(tag, 'PASS')]: ok = False
        out.append(line)
out.append(f"E1 (no verdict worse at 0.40 than at fitted rho_sun, LO): {'PASS' if ok else 'FAIL'}")
open('field_tests/results/a2n_rhosun_fixed.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
