import sys; sys.path.insert(0, '.')
from tools.janus_astro import bbn
out = []; f = (10.75/106.75)**(4/3)
for k, g in [('a not populated', 0), ('b U(1)', 2), ('c SU(2)', 6), ('d SU(2)+gaugino', 6 + 6*7/8)]:
    dN = (4/7)*g*f; y, D = bbn.Yp(0.02242, dN), bbn.DH(0.02242, dN)
    out.append(f"{k}: g_h={g:.2f} dN={dN:.4f} inside [-0.04,0.41]: {-0.04 <= dN <= 0.41}; Yp={y:.5f} 1e5DH={D*1e5:.4f}; {dN/0.03:.1f} sigma at CMB-S4 0.03")
open('field_tests/results/b3_taui_darkrad.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
