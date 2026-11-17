"""B2 — PREREG_B2_chronos_bbn.md"""
import sys, math; sys.path.insert(0, '.')
from tools.janus_astro import bbn
from tools.janus_lt.background import omega_gamma_h2
WB = 0.02242; DHo, sDHo = 2.527e-5, 0.030e-5; YPo, sYPo = 0.2453, 0.0034; SWB = 0.00014
og = omega_gamma_h2(2.7255); per = (7/8)*(4/11)**(4/3)*og
out = [f"Omega_gamma h2 = {og:.4e}; per-dN GW energy h2 = {per:.3e} (literature check 5.6e-6: rel {per/5.6e-6-1:+.3f})"]
br = {'tau=i TR=1e6': (6.87e-19, 1.71e5, 0.0), 'tau=i TR=3e6': (7.60e-19, 2.42e5, 0.0),
      'rho TR=3.2e8': (6.97e-19, 2.35e5, 0.0), 'rho TR=3.0e9': (6.84e-19, 4.93e5, 0.0)}   # (max listed Omega h2, f_end, dN_DR)
lab = lambda p: 'CONSISTENT' if abs(p) < 2 else ('TENSION' if abs(p) <= 3 else 'EXCLUDED')
T1 = True; T2 = True
for k, (om, fe, ddr) in br.items():
    dgw = om*math.log(fe/1e-18)/per; dN = dgw + ddr
    y, D = bbn.Yp(WB, dN), bbn.DH(WB, dN); T1 &= (y == float(bbn.table().Y_p(WB, dN)) and D == float(bbn.table().DH(WB, dN)))
    sy, sd = bbn.sigma(WB, dN); h = 1e-5
    dYw = (bbn.Yp(WB+h, dN)-bbn.Yp(WB-h, dN))/(2*h); dDw = (bbn.DH(WB+h, dN)-bbn.DH(WB-h, dN))/(2*h)
    py = (y-YPo)/math.sqrt(sYPo**2+sy**2+(dYw*SWB)**2); pd = (D-DHo)/math.sqrt(sDHo**2+sd**2+(dDw*SWB)**2)
    ok = -0.04 <= dN <= 0.41 and abs(py) < 2 and abs(pd) < 2; T2 &= ok
    out.append(f"{k}: dN_GW <= {dgw:.2e} (+DR {ddr}) -> Yp {y:.6f} (d {y-bbn.Yp(WB,0):+.1e}) pull {py:+.2f}; D/H {D:.5e} (d {D-bbn.DH(WB,0):+.1e}) pull {pd:+.2f} -> {lab(max(abs(py),abs(pd)))}")
out.append(f"T1 wiring lossless -> {'PASS' if T1 else 'FAIL'}"); out.append(f"T2 all branches inside window and |pull|<2 -> {'CONSISTENT' if T2 else 'NOT'}")
out.append("B2 VALIDATED" if T1 else "B2 NOT VALIDATED")
open('field_tests/results/b2_chronos_bbn.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
