"""J4 (locked PREREG_J4): Janus reheating -> N*, n_s vs D979 exact."""
import sys, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc import models as J
from tools.janus_calc.observe import observe
m = J.serapis_E(1.15e-6); L = []; ok = True
ref = [(1e4, 46.458, 0.96951), (1e6, 47.985, 0.97113), (1e7, 48.749, 0.97191), (1e8, 49.513, 0.97268), (1e10, 51.042, 0.97416)]
for TR, N0, n0 in ref:
    o = observe(m, TR=TR); dN = o['Nstar'] - N0; dn = o['ns'] - n0; good = abs(dN) <= 0.02 and abs(dn) <= 5e-6; ok &= good
    L.append(f"T_R={TR:.0e}: N* {o['Nstar']:.3f} (ref {N0}, d {dN:+.3f}) n_s {o['ns']:.6f}±{o['err']['ns']:.1e} (ref {n0}, d {dn:+.1e}) r {o['r']:.4e} alpha_s {o['alpha_s']:.4e} -> {'PASS' if good else 'FAIL'}")
    print(L[-1], flush=True)
L.append('VALIDATED' if ok else 'NOT VALIDATED'); open('field_tests/results/janus_j4_check.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
