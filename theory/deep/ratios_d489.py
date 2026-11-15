import math, itertools, random
vals=[0.9736,0.0046,57.2,29.6,135.14,0.0274,0.23,0.3728,0.065,0.081,0.277,1.7,4.1,6.12,242,267,39,43,1.7,4.7,3.04e-7,7.7e-4,1.43e-4,29.36,237/1.5e11]
T={'phi':1.6180339887,'phi^2':2.6180339887,'silver':1+math.sqrt(2),'silver^2':(1+math.sqrt(2))**2}
def hits(v,record=False):
    rs=[(max(a,b)/min(a,b),i,j) for (i,a),(j,b) in itertools.combinations(enumerate(v),2)]+[(a,i,i) for i,a in enumerate(v) if a>1]
    out=[]
    for R,i,j in rs:
        for n,t in T.items():
            if abs(R/t-1)<0.01: out.append((n,R,i,j))
    return out
obs=hits(vals); print(f"observed hits: {len(obs)}")
for n,R,i,j in obs: print(f"  {n}: {vals[i]} / {vals[j]} = {R:.4f}")
rng=random.Random(20261114); lo,hi=math.log(min(vals)),math.log(max(vals)); cnt=[]
for _ in range(2000):
    v=[math.exp(rng.uniform(lo,hi)) for _ in vals]; cnt.append(len(hits(v)))
p=sum(c>=len(obs) for c in cnt)/len(cnt); mean=sum(cnt)/len(cnt)
print(f"random sets: mean hits {mean:.2f}; p(>= observed) = {p:.3f}")
print("VERDICT:", "OVERLAP SIGNIFICANT" if p<0.01 else "NO MORE THAN CHANCE")
