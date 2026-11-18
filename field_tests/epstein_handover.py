"""D1293 (locked): Z_L(s) - Z_L*(s) sign change at s = d/4 for non-self-dual champions."""
import sys; sys.path.insert(0,'tools/lattice'); import lattice_lab as LL, numpy as np
print("P4 d=2 s=2: hex", round(LL.epstein('hex',2)['epstein'],6), " square", round(LL.epstein('square',2)['epstein'],6))
for L,D,d in (('FCC','BCC',3),('D5','D5*',5),('E6','E6*',6),('E7','E7*',7),('hex','hex*',2),('D4','D4*',4),('E8','E8*',8)):
    c=d/4; row=[]
    for s in (c-0.4,c-0.1,c,c+0.1,c+0.4,d/2+0.5,d/2+2):
        if abs(s-d/2)<1e-9 or s<=0: continue
        z1=LL.epstein(L,s)['epstein']; z2=LL.epstein(D,s)['epstein']; row.append(f"s={s:.2f}:{z1-z2:+.3e}")
    print(f"{L:4s} vs {D:4s} (d/4={c:.2f}) Z_L - Z_L*: "+'  '.join(row))
