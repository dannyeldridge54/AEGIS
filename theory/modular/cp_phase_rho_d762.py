"""D762 (locked PREREG_D762). Postulate P1: delta uniform. AI-assisted."""
import math
P=lambda s:1-2/math.pi*math.asin(s)
print("K4 regression: P(0)=%.3f P(1)=%.3f P(1/sqrt2)=%.3f"%(P(0),P(1),P(1/math.sqrt(2))))
cases=[("c=0.3 MH=1e12 light",0.56),("c=0.3 MH=1e12 heavy",0.12),("c=0.3 MH=1e13",0.01),("c=0.3 MH=5e13",0.01),
       ("c=1 MH=1e12 light",0.12),("c=1 MH=1e12 heavy",0.09),("c=1 MH=1e13",0.01),("c=3 MH=1e12 light",0.08),("c=3 MH=1e12 heavy",0.04)]
ps=[]
for n,s in cases: p=P(s); ps.append(p); print(f"{n}: sin_min={s} P={p:.3f}")
ps2=sorted(ps); med=ps2[len(ps2)//2]
print(f"min P={min(ps):.3f} median P={med:.3f} fraction P>=0.9: {sum(p>=0.9 for p in ps)}/{len(ps)}")
v="NATURAL" if med>=0.8 and min(ps)>=0.5 else ("MARGINAL" if med>=0.8 else "TUNED")
print("VERDICT:",v,"| with gCP imposed: epsilon=0 at rho (theorem), branch needs another baryogenesis")
