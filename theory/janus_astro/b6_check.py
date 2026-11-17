import sys; sys.path.insert(0, '.')
from tools.janus_astro import bbn_net as B, bbn
out = []
r0 = B.abundances(0.02242)
T1 = (round(r0['Yp_mass'], 5) == 0.24592 and round(r0['DH']*1e5, 4) == 2.4360 and round(r0['Li7H']*1e10, 3) == 5.699)
out.append(f"T1 base: Yp_mass {r0['Yp_mass']:.5f} DH {r0['DH']*1e5:.4f} Li {r0['Li7H']*1e10:.3f} Neff {r0['Neff_final']:.4f} -> {'PASS' if T1 else 'FAIL'}")
r1 = B.abundances(0.02242, 0.3)
dNf = r1['Neff_final'] - r0['Neff_final']
lY = r1['Yp_mass']-r0['Yp_mass']; lD = r1['DH']-r0['DH']
tY = bbn.Yp_mass(0.02242, dNf)-bbn.Yp_mass(0.02242, 0); tD = bbn.DH(0.02242, dNf)-bbn.DH(0.02242, 0)
T2 = abs(lY/tY-1) <= 0.15 and abs(lD/tD-1) <= 0.15
out.append(f"T2 dN_init 0.3 (dNeff_final {dNf:.4f}): dYp LINX {lY:.5f} table {tY:.5f} ({lY/tY-1:+.3f}); dDH {lD*1e5:.4f} vs {tD*1e5:.4f} ({lD/tD-1:+.3f}) -> {'PASS' if T2 else 'FAIL'}")
r2 = B.abundances(0.0230)
lY = r2['Yp_mass']-r0['Yp_mass']; lD = r2['DH']-r0['DH']
tY = bbn.Yp_mass(0.0230)-bbn.Yp_mass(0.02242); tD = bbn.DH(0.0230)-bbn.DH(0.02242)
T3 = abs(lY/tY-1) <= 0.10 and abs(lD/tD-1) <= 0.10
out.append(f"T3 wb 0.0230: dYp {lY:.5f} vs {tY:.5f} ({lY/tY-1:+.3f}); dDH {lD*1e5:.4f} vs {tD*1e5:.4f} ({lD/tD-1:+.3f}) -> {'PASS' if T3 else 'FAIL'}")
out.append("B6 " + ("VALIDATED" if T1 and T2 and T3 else "NOT VALIDATED"))
open('field_tests/results/b6_bbn_net.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
