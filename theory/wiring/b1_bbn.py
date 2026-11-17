"""B1 — PREREG_B1_bbn.md"""
import sys, math; sys.path.insert(0, '.')
import numpy as np
from camb.bbn import BBN_table_interpolator
from tools.janus_astro import bbn
WB, SWB = 0.02242, 0.00014; DHo, sDHo = 2.527e-5, 0.030e-5; YPo, sYPo = 0.2453, 0.0034
out = []
ref = {c: BBN_table_interpolator(f) for c, f in bbn.TABLES.items()}
d = 0.0
for c in ref:
    for w, n in [(0.021, 0), (0.02242, 0), (0.023, 0.5), (0.0224, 1.0), (0.022, -0.5)]:
        d = max(d, abs(bbn.Yp(w, n, c) - ref[c].Y_p(w, n)), abs(bbn.DH(w, n, c) - ref[c].DH(w, n)))
T1 = d == 0; out.append(f"T1 lossless max|diff| = {d:.1e} -> {'PASS' if T1 else 'FAIL'}")
dy = max(abs(bbn.Yp(WB, n, 'primat') - bbn.Yp(WB, n, 'parthenope')) for n in (0, 0.5, 1))
T2 = dy <= 1e-3; out.append(f"T2 max|Yp PRIMAT - PArthENoPE| (dN=0,0.5,1) = {dy:.2e} -> {'PASS' if T2 else 'FAIL'}")
out.append(f"D/H PRIMAT vs PArthENoPE rel diff at Planck wb: {bbn.DH(WB,0,'parthenope')/bbn.DH(WB,0,'primat')-1:+.4f}")
lab = lambda p: 'CONSISTENT' if abs(p) < 2 else ('TENSION' if abs(p) <= 3 else 'EXCLUDED')
for c in ref:
    sy, sd = bbn.sigma(WB, 0, c); h = 1e-5
    dYdw = (bbn.Yp(WB+h, 0, c) - bbn.Yp(WB-h, 0, c))/(2*h); dDdw = (bbn.DH(WB+h, 0, c) - bbn.DH(WB-h, 0, c))/(2*h)
    y, D = bbn.Yp(WB, 0, c), bbn.DH(WB, 0, c)
    py = (y - YPo)/math.sqrt(sYPo**2 + sy**2 + (dYdw*SWB)**2); pd = (D - DHo)/math.sqrt(sDHo**2 + sd**2 + (dDdw*SWB)**2)
    out.append(f"R1 {c}: Yp={y:.5f} (th {sy:.1e}, wb {abs(dYdw*SWB):.1e}) pull {py:+.2f} {lab(py)}; 1e5 D/H={D*1e5:.4f} (th {sd*1e5:.4f}, wb {abs(dDdw*SWB)*1e5:.4f}) pull {pd:+.2f} {lab(pd)}")
def chi2(n):
    sy, sd = bbn.sigma(WB, n); return ((bbn.Yp(WB, n)-YPo)**2/(sYPo**2+sy**2) + (bbn.DH(WB, n)-DHo)**2/(sDHo**2+sd**2))
ns = np.linspace(-1.0, 1.5, 501); c2 = np.array([chi2(n) for n in ns]); ok = ns[c2 - c2.min() < 3.84]
out.append(f"R2 BBN-only dN 95%: [{ok.min():+.3f}, {ok.max():+.3f}], best {ns[c2.argmin()]:+.3f} (chi2min {c2.min():.2f}); SERAPIS dN=0 {'INSIDE' if ok.min()<=0<=ok.max() else 'OUTSIDE'}")
MP, HB, gs = 2.435e18, 6.582119569e-25, 106.75
for T in (1e5, 1e6):
    H = math.sqrt(math.pi**2*gs/90)*T*T/MP; t = HB/(2*H)
    out.append(f"R3 T={T:.0e} GeV: t = {t:.2e} s ({math.log10(1/t):.1f} decades before t_BBN ~ 1 s)")
out.append("B1 VALIDATED" if T1 and T2 else "B1 NOT VALIDATED")
open('field_tests/results/b1_bbn.txt', 'w').write("\n".join(out)+"\n"); print("\n".join(out))
