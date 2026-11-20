"""PREREG_L1_ROBUST (D1742): up rung from SM Yukawas at M_Z (arXiv:2510.01312). Committed copy of the inline run."""
import numpy as np
rng=np.random.default_rng(2026); N=200000
d=lambda v,s: np.abs(rng.normal(v,s,N))
yu,yd,ys,yc,yb,yt=d(7.04e-6,.15e-6),d(1.54e-5,.02e-5),d(3.06e-4,.04e-4),d(3.56e-3,.06e-3),d(1.630e-2,.009e-2),d(0.967,.004)
g=lambda a,b,c: np.sqrt((b/c)*np.sqrt(a/c))
gd,gu=g(yd,ys,yb),g(yu,yc,yt); r=gu/gd; ms=(1+1/16)/r-1/16
print(f"input B (2510.01312 Yukawas at M_Z): g_d={np.median(gd):.4f} g_u={np.median(gu):.5f} g_u/g_d={np.median(r):.4f}±{r.std():.4f} (frozen L1 0.1318: {(np.median(r)-0.1318)/r.std():+.1f}σ; rung9 0.1172: {(np.median(r)-0.1172)/r.std():+.1f}σ)")
print(f"m_u* = {np.median(ms):.2f} ± {ms.std():.2f} -> {'ROBUST (rung 8)' if abs(np.median(ms)-8)<=0.5 else 'SHIFTED'}")
