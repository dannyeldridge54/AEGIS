"""D764 (locked PREREG_D764). AI-assisted."""
import cmath, math, statistics
from mpmath import mp, kleinj
mp.dps=30
J=lambda t: complex(kleinj(t))*1728
def reduce(t):
    for _ in range(200):
        t=complex(t.real-round(t.real),t.imag)
        if abs(t)<1-1e-12: t=-1/t
        else: break
    return t
def s(t):
    j=J(reduce(t)); return 0.0 if abs(j)<1e-8 else abs(j.imag)/abs(j)
rho=0.5+1j*math.sqrt(3)/2
print("K4: s(i)=%.2e s(rho): |j|=%.2e s(0.1+1.3i)=%.3f"%(s(1j),abs(J(rho)),s(0.1+1.3j)))
ex=(-3/2)/rho; print("paper example a0=2,b3=-3: U2=",ex,"reduced",reduce(ex),"s_CP=%.3f"%s(ex))
vals=[]; seen=set()
for a in range(1,7):
    for b in range(1,13):
        r=b/a
        if r in seen: continue
        seen.add(r); u=(-r)/rho
        if reduce(u).imag<0.2: continue
        vals.append((r,s(u)))
f=sum(v>0.1 for _,v in vals)/len(vals); med=statistics.median(v for _,v in vals)
for r,v in vals: print(f"|b3/a0|={r:.3f}: s_CP={v:.3f}")
print(f"N ratios={len(vals)} fraction s_CP>0.1: {f:.2f} median s_CP={med:.3f}")
print("VERDICT:", "P1 REPLACED by literature mechanism (P2)" if f>=0.5 and med>=0.3 else "P1 STAYS")
