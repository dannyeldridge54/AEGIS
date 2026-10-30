# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 225c68b0377bdccc
import json, numpy as np
from collections import defaultdict
rows=json.load(open("exo_rows.json")); S=defaultdict(list)
for h,p,m in rows: S[h].append(float(p))
pairs=[]
for h,ps in S.items():
    ps=sorted(ps)
    for a,b in zip(ps,ps[1:]):
        r=b/a
        if 1<r<=4: pairs.append((a,r,h))
P=np.array([p for p,_,_ in pairs]); R=np.array([r for _,r,_ in pairs])
print("systems",len(S),"adjacent pairs (ratio<=4)",len(R))
RES=[2/1,3/2,4/3,5/4]
def frac(r): return np.mean([any(x<=r_<=1.01*x for x in RES) for r_ in r]) if len(r) else np.nan
def frac_v(r): return np.mean(np.any([(r>=x)&(r<=1.01*x) for x in RES],axis=0))
obs=frac_v(R)
# smooth null: kernel-smoothed log-ratio distribution (bandwidth 0.08 in ln r, wide compared with 1% windows)
rng=np.random.default_rng(42); lr=np.log(R)
def draw(n,src=lr):
    x=rng.choice(src,n)+rng.normal(0,0.08,n); x=np.abs(x); x=np.minimum(x,np.log(4)); return np.exp(x)
null=np.array([frac_v(draw(len(R))) for _ in range(10000)])
print(f"A: fraction just wide of 2:1,3:2,4:3,5:4 = {obs:.4f}  null mean {null.mean():.4f}  excess x{obs/null.mean():.2f}  p = {(null>=obs).mean():.4f}")
# per resonance
for x,lab in zip(RES,["2:1","3:2","4:3","5:4"]):
    o=np.mean((R>=x)&(R<=1.01*x)); nb=np.mean((R>=0.97*x)&(R<0.99*x)) # just inside (narrow of) resonance
    print(f"  {lab}: {o*len(R):.0f} pairs just wide (1%) vs {nb*len(R)/2:.1f} per 1% just narrow")
# B: compact vs wide
for lab,mask in (("compact (inner P<10 d)",P<10),("wide (inner P>10 d)",P>=10)):
    r=R[mask]; o=frac_v(r); nl=np.array([frac_v(draw(len(r),np.log(r))) for _ in range(3000)])
    print(f"B {lab}: n={len(r)} obs {o:.4f} null {nl.mean():.4f} excess x{o/nl.mean():.2f} p {(nl>=o).mean():.4f}")
# bootstrap difference of excess ratio
diffs=[]
for _ in range(1000):
    i=rng.integers(0,len(R),len(R)); r=R[i]; p=P[i]
    e=[]
    for m in (p<10,p>=10):
        rr=r[m]; e.append(frac_v(rr)-np.mean([frac_v(draw(len(rr),np.log(rr))) for _ in range(20)]))
    diffs.append(e[0]-e[1])
lo,hi=np.percentile(diffs,[2.5,97.5]); print(f"B difference in excess (compact - wide): {np.mean(diffs):.4f}  95% [{lo:.4f}, {hi:.4f}]")
json.dump({"n_pairs":len(R),"obs":obs,"null":null.mean(),"p":float((null>=obs).mean())},open("exo_result.json","w"))
