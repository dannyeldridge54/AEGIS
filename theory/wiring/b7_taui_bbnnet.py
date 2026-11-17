import sys; sys.path.insert(0, '.')
from tools.janus_astro import bbn_net as B, bbn
base = B.abundances(0.02242, 0.0); N0 = base['Neff_final']; out = [f"base Neff_final {N0:.4f}"]; ok = True
for tgt, lab in ((0.054, 'U(1)'), (0.161, 'SU(2)'), (0.301, 'SU(2)+gaugino')):
    x0, x1 = tgt/0.261, tgt/0.261*1.05
    r0 = B.abundances(0.02242, x0); f0 = r0['Neff_final'] - N0 - tgt; r = r0; n = 1
    while abs(f0) > 0.003 and n < 5:
        r1 = B.abundances(0.02242, x1); f1 = r1['Neff_final'] - N0 - tgt; n += 1
        x0, x1, f0, r = x1, x1 - f1*(x1 - x0)/(f1 - f0), f1, r1
    dN = r['Neff_final'] - N0
    yt, dt = bbn.Yp_mass(0.02242, dN), bbn.DH(0.02242, dN)*1e5
    a = abs(r['Yp_mass'] - yt) <= 1e-3 and abs(r['DH']*1e5/dt - 1) <= 0.02; ok &= a
    out.append(f"{lab}: init {x0:.4f} -> dNeff_final {dN:.4f} ({n} evals); Yp {r['Yp_mass']:.5f} (table {yt:.5f}, pull {(r['Yp_mass']-0.2453)/0.0034:+.2f}); 1e5DH {r['DH']*1e5:.4f} (table {dt:.4f}, pull {(r['DH']*1e5-2.527)/0.030:+.2f}); Li {r['Li7H']*1e10:.3f} -> agree {a}")
out.append("B7 " + ("VALIDATED" if ok else "NOT VALIDATED"))
open('field_tests/results/b7_taui_bbnnet.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
